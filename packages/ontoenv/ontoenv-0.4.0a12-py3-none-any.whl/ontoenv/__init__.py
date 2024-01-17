"""
"""
import time
import sys
import fnmatch
import json
from pathlib import Path
import os
import glob
import shutil
import logging
import rdflib
import networkx as nx
from rdflib import RDF, OWL
from typing import Optional, Set, Generator, Union, Tuple, Dict, List
from filelock import FileLock

FILE_EXTENSIONS = [".ttl", ".rdf", ".owl", ".n3", ".ntriples"]
ONLINE_PREFIXES = ["http://", "https://"]

# TODO: track dependencies in a graph and render it

OntologyLocation = Union[Path, str]
FileOrGraph = Union[OntologyLocation, rdflib.Graph]


class OntoEnv:
    # stores the dependency graph
    _dependencies: nx.DiGraph
    # stores the mapping of filename => graph
    _graph_cache: Dict[str, rdflib.Graph]
    # keeps track of what URIs to skip
    _to_skip: Set[str]
    # mapping of URI => filename
    mapping: Dict[str, str]

    def __init__(
        self,
        oe_dir: Optional[Path] = None,
        initialize: bool = False,
        strict: bool = False,
        offline: bool = False,
        ignore_patterns: Optional[List[str]] = None,
        recursive_limit: int = -1,
        search_dirs: Optional[List[str]] = None,
    ):
        self._dependencies = nx.DiGraph()
        self._to_skip = set()
        self.recursive_limit = recursive_limit
        self._offline = offline
        self._graph_cache = {}
        self.mapping = {}
        self._strict = strict
        self._seen: Set[str] = set()

        # track which files to ignore
        self._ignore_patterns = ignore_patterns or []
        logging.info(f"Ignoring files matching {self._ignore_patterns}")

        # setup the .ontoenv directory
        if oe_dir is None:
            oe_dir = find_root_file()
            if oe_dir is None:
                oe_dir = Path(os.getcwd())
        self.oedir = Path(oe_dir)
        logging.info(f"Using {self.oedir} as .ontoenv directory")
        if os.path.basename(oe_dir) != ".ontoenv":
            oe_dir = oe_dir / ".ontoenv"
        self.oedir = oe_dir.resolve()
        self.cachedir = self.oedir / "cache"

        # create the .ontoenv directory if it doesn't exist
        if initialize:
            logging.info(f"Create .ontoenv at {self.oedir.resolve()}")
            os.makedirs(self.oedir, exist_ok=True)
            os.makedirs(self.cachedir, exist_ok=True)

        # track which directories to search for ontologies
        self.search_dirs = list(map(Path, search_dirs)) if search_dirs else [self.oedir.parent]
        logging.info(f"Searching for ontologies in {self.search_dirs}")

        # read or create state file
        state_file = self.oedir / "state.json"
        lock_file = self.oedir / "state.json.lock"
        self.lock = FileLock(str(lock_file))
        if os.path.exists(state_file):
            self.from_state()

        if initialize:
            # Serialize all internal state to a single JSON file
            self.save_state()
            self.refresh()


    @classmethod
    def from_state_file(cls, state_file: Path) -> "OntoEnv":
        """
        Create an OntoEnv from a state file.
        """
        state = json.load(open(state_file))
        oe_dir = state.get('oe_dir')
        if not oe_dir:
            raise Exception(f"Could not find oe_dir in {state_file}")
        return cls(oe_dir=oe_dir)

    def save_state(self):
        state = {
            'oe_dir': str(self.oedir),
            'strict': self._strict,
            'offline': self._offline,
            'ignore_patterns': self._ignore_patterns,
            'search_dirs': [str(dir) for dir in self.search_dirs],
            'mapping': self.mapping,
            'dependencies': nx.readwrite.json_graph.node_link_data(self._dependencies),
            'to_skip': list(self._to_skip)
        }
        with self.lock:
            with open(self.oedir / "state.json", "w") as f:
                json.dump(state, f)

    def from_state(self) -> None:
        """
        Repopulate all of the OntoEnv fields from state.json.
        """
        state_file = self.oedir / "state.json"
        if not os.path.exists(state_file):
            raise Exception(
                f"No .ontoenv directory at {self.oedir}. Be sure to run 'ontoenv init'"
            )
        state = json.load(open(state_file))
        self.mapping = state.get('mapping', {})
        self._ignore_patterns = state.get('ignore_patterns', [])
        self.search_dirs = [Path(dir) for dir in state.get('search_dirs', [])]
        self._to_skip = set(state.get('to_skip', []))
        if state.get('dependencies'):
            self._dependencies = nx.readwrite.json_graph.node_link_graph(state.get('dependencies'))
        else:
            self._dependencies = nx.DiGraph()

    def refresh(self, recursive_limit: int = -1) -> None:
        """
        Ensure the ontoenv environment is up to date with the current set of imports.
        Does not currently re-fetch remote ontologies.
        """
        self.recursive_limit = recursive_limit
        self.from_state()
        search_dirs = self.search_dirs if self.search_dirs else [self.oedir.parent]
        # find all ontology files in the search directories. We will eventually want to
        # visit all of these
        for search_dir in search_dirs:
            logging.info(f"Searching for RDF files in {search_dir}")
            for filename in find_ontology_files(search_dir, self._ignore_patterns):
                # load the file into cache
                self._cache_file(filename)
                self._get_ontology_definition(filename=filename)
        for search_dir in search_dirs:
            for filename in find_ontology_files(search_dir, self._ignore_patterns):
                self._resolve_imports_from_uri(filename, recursive_limit)

        # remove old imports/files that are no longer in the mapping
        mapping_tmp = list(self.mapping.items())
        for uri, filename in mapping_tmp:
            if not os.path.exists(filename):
                del self.mapping[uri]
                self._dependencies.remove_node(uri)
                logging.info(f"Removed {uri} from mapping")
        # print # of mappings
        logging.info(f"Found {len(self.mapping)} mappings")
        self.save_state()

    def _cache_file(self, filename: Path) -> Optional[rdflib.Graph]:
        # if the file is already in the cache, then we don't need to do anything
        if filename in self._graph_cache:
            return self._graph_cache.get(str(filename))
        if self.cachedir not in filename.parents:
            shutil.copy(filename, self.cachedir)
        g = rdflib.Graph()
        try:
            g.parse(filename, format=rdflib.util.guess_format(str(filename)))
        except Exception as e:
            self._to_skip.add(str(filename))
            if self._strict:
                logging.fatal(f"Could not parse {filename}: {e}")
                sys.exit(1)
            else:
                logging.error(f"Could not parse {filename}: {e}")
                return
        self._graph_cache[str(filename)] = g
        return g

    def import_graph(self, dest: rdflib.Graph, src: FileOrGraph) -> None:
        """
        Imports the src graph into the dest graph and makes the following transformations:
        - rewrites all sh:prefixes and sh:declare statements to hang off of the ontology declaration of the provided (dest) graph
        - removes all import statements from the src graph
        """
        # get base URI of dest graph
        uri = dest.value(predicate=rdflib.RDF.type, object=rdflib.OWL.Ontology)
        # remove all import statements from src
        if uri is None:
            raise Exception("No owl:Ontology found in graph")

        if isinstance(src, (Path, str)):
            src = Path(src)
            if not os.path.exists(src):
                raise Exception(f"Could not find {src}")
            src_graph = self._cache_file(src)
            assert src_graph is not None
            src_graph.remove((None, rdflib.OWL.imports, None))
            src = src_graph
            # remove any imports for the src graph

        # get ontology name of src graph
        src_ontology_name = src.value(predicate=rdflib.RDF.type, object=rdflib.OWL.Ontology)
        if src_ontology_name is None:
            raise Exception("No owl:Ontology found in graph")
        # remove all imports of src_ontology_name
        dest.remove((None, rdflib.OWL.imports, src_ontology_name))
        src.remove((None, rdflib.OWL.imports, None))
        # remove src ontology declaration
        src.remove((src_ontology_name, None, None))

        dest += src

        # change all triples of form <x> <sh:prefixes> <uri1> to <x> <sh:prefixes> <uri>, where
        # <uri> is our base URI above
        for s, p, o in dest.triples((None, rdflib.SH.prefixes, None)):
            dest.remove((s, p, o))
            dest.add((s, p, uri))
        # change all triples of form <x> <sh:declare> <uri1> to <uri> <sh:declare> <uri1>, where
        # <uri> is our base URI above
        for s, p, o in dest.triples((None, rdflib.SH.declare, None)):
            dest.remove((s, p, o))
            dest.add((uri, p, o))

    def resolve_uri(
        self, uri: OntologyLocation
    ) -> Optional[Tuple[rdflib.Graph, OntologyLocation]]:
        """
        Returns an rdflib.Graph which the provided uri resolves to. Prioritizes
        local files (including those in the cache), then remote URIs (which are
        then cached)

        :param uri: URI of the graph to return
        :return: Tuple of the RDF Graph and the physical filename where it was found
        :raises Exception: [TODO:description]
        """
        uri = str(uri)

        # attempt to resolve locally
        print(uri, self.mapping.keys())
        if uri in self.mapping:
            filename = self.mapping[uri]
            # check if the graph is in the cache
            if uri in self._graph_cache:
                return self._graph_cache[uri], filename
            # if not in the cache, parse the graph
            graph = rdflib.Graph()
            graph.parse(filename, format=rdflib.util.guess_format(filename) or "xml")
            # store the parsed graph in the cache
            self._graph_cache[uri] = graph
            return graph, filename
        if uri in self._graph_cache:
            return self._graph_cache[uri], uri
        # create graph object to hold the remote graph
        graph = rdflib.Graph()
        logging.info(
            f"URI {uri} did not have a cached definition. Trying to fetch from local file or remote, if not in offline mode"
        )
        if self._offline and not _is_online(uri):
            logging.error(f"Offline mode is enabled. Cannot download {uri}")
            return None
        try:
            graph.parse(uri, format=rdflib.util.guess_format(uri) or "xml")
            filename = uri
        except Exception as e:
            self._to_skip.add(uri)
            raise Exception(f"No definition for {uri}: {e}")

        # if the filename does not exist locally, then serialize the graph into the cache
        # and upate the mapping
        if not os.path.exists(filename):
            filename = str(filename) + ".ttl"
            new_filename = self.cachedir / Path(
                filename.replace("/", "_").replace(":", "_")
            )
            graph.serialize(str(new_filename), format="ttl")
            self.mapping[str(uri)] = str(filename)
        else:
            self.mapping[str(uri)] = str(filename)
        print(len(self.mapping), uri)
        return graph, filename

    def _get_ontology_definition(self, graph: Optional[rdflib.Graph] = None, filename: Optional[OntologyLocation] = None) -> None:
        """
        If the filename is not already in the mapping, it parses the file and updates the mapping.

        :param filename: The filename of the ontology
        """
        # if the filename is already in the mapping, then we don't need to do anything
        # or, if the filename is in the list of files to skip, then we don't need to do anything
        if (
            str(filename) in self.mapping.values()
            or str(filename) in self._to_skip
        ):
            return
        # if the graph is not provided, then we need to pull it from cache
        graph = graph or self._graph_cache.get(str(filename))
        if graph is None:
            raise Exception(f"Could not find {filename} in cache")
        ontology_name = graph.value(predicate=RDF.type, object=OWL.Ontology)
        if ontology_name is None:
            if self._strict:
                raise Exception(f"No owl:Ontology found in {filename}")
            else:
                logging.error(f"No owl:Ontology found in {filename}")
        self.mapping[str(ontology_name)] = str(filename)
        self.save_state()

    def _resolve_imports_from_uri(self, uri: OntologyLocation, recursive_limit: int = None) -> None:
        if recursive_limit is None:
            recursive_limit = self.recursive_limit
        if recursive_limit == 0:
            return
        recursive_limit -= 1
        """
        Resolves the imports from the given URI.

        :param uri: The URI to resolve imports from
        """
        if str(uri) in self._seen:
            return
        logging.info(f"{time.time()} Resolving imports from {uri}")
        self._seen.add(str(uri))
        try:
            resolved = self.resolve_uri(uri)
            if resolved is None:
                return
            graph, filename = resolved
            self._get_ontology_definition(graph, filename)
            for importURI in graph.objects(predicate=rdflib.OWL.imports):
                self._dependencies.add_edge(str(uri), str(importURI))
                self._resolve_imports_from_uri(str(importURI))
        except Exception as e:
            self._to_skip.add(str(uri))
            if self._strict:
                logging.fatal(f"Could not resolve {uri} ({e})")
                sys.exit(1)
            else:
                logging.error(f"Could not resolve {uri} ({e})")
                return

    def print_dependency_graph(self, root_uri: Optional[str] = None) -> None:
        """
        Prints the dependency graph.

        :param root_uri: The root URI to start from. If None, it starts from all nodes with no incoming edges.
        """
        print(
            "\033[1mBolded\033[0m values are duplicate imports whose deps are listed elsewhere in the tree"
        )
        if root_uri is None or root_uri == "":
            root_uris = [n for n, d in self._dependencies.in_degree() if d == 0]
        elif root_uri not in self._dependencies:
            root_uris = [self.mapping[root_uri]]
        else:
            root_uris = [root_uri]
        seen: Set[str] = set()
        for root in root_uris:
            print(f"{root}")
            for _, dep in self._dependencies.edges([root]):
                self._print_dep_graph(dep, 1, seen)

    def _print_dep_graph(
        self, uri: str, indent: int, seen: Set[str], last: bool = False
    ) -> None:
        char = "┕" if last else "┝"
        if uri in seen:
            print(f"{'|  '*indent}{char} \033[1m{uri}\033[0m")
            return
        print(f"{'|  '*indent}{char} {uri}")
        seen.add(uri)
        num_deps = len(self._dependencies.edges([uri]))
        for i, (_, dep) in enumerate(self._dependencies.edges([uri])):
            self._print_dep_graph(dep, indent + 1, seen, last=i == num_deps - 1)

    def import_dependencies(
        self, graph: rdflib.Graph, recursive: bool = True, remove_import_statements: bool = True
    ) -> None:
        """
        Imports all dependencies of the given graph. Rewrites sh:prefixes and sh:declare statements to
        hang off of the ontology declaration of the provided graph

        :param graph: The RDF graph to import dependencies for
        :param recursive: Whether to recursively import dependencies
        :param recursive_limit: The maximum depth to recursively import dependencies. -1 means no limit.
        :param remove_import_statements: Whether to remove the import statements from the graph after importing them
        """
        # get the base URI of this graph (subject of owl:Ontology)
        uri = graph.value(predicate=rdflib.RDF.type, object=rdflib.OWL.Ontology)
        if uri is None:
            raise Exception("No owl:Ontology found in graph")
        # import all dependencies
        self._import_dependencies(
            graph, recursive=recursive, recursive_limit=self.recursive_limit
        )
        # change all triples of form <x> <sh:prefixes> <uri1> to <x> <sh:prefixes> <uri>, where
        # <uri> is our base URI above
        for s, p, o in graph.triples((None, rdflib.SH.prefixes, None)):
            graph.remove((s, p, o))
            graph.add((s, p, uri))
        # change all triples of form <x> <sh:declare> <uri1> to <uri> <sh:declare> <uri1>, where
        # <uri> is our base URI above
        for s, p, o in graph.triples((None, rdflib.SH.declare, None)):
            graph.remove((s, p, o))
            graph.add((uri, p, o))
        # remove all import statements
        if remove_import_statements:
            graph.remove((None, rdflib.OWL.imports, None))

    def _import_dependencies(
        self,
        graph: rdflib.Graph,
        cache: Optional[set] = None,
        recursive: bool = True,
        recursive_limit: int = None,
    ) -> None:
        if recursive_limit is None:
            recursive_limit = self.recursive_limit
        if recursive_limit == 0:
            return
        recursive_limit -= 1
        if recursive_limit > 0:
            recursive = False
        elif recursive_limit == 0:
            return
        if cache is None:
            cache = set()
        new_imports = False
        for importURI in graph.objects(predicate=rdflib.OWL.imports):
            uri = str(importURI)
            if uri in cache:
                continue
            new_imports = True
            filename = self.mapping.get(uri)
            if filename is None:
                if self._strict:
                    self._to_skip.add(uri)
                    raise Exception(f"Could not load {uri} (no definition found)")
                logging.error(f"Could not load {uri} (no definition found)")
                cache.add(uri)
                continue
            logging.info(f"Importing {uri} from {filename}")
            graph.parse(filename, format=rdflib.util.guess_format(filename))
            cache.add(uri)
        if (recursive or recursive_limit > 0) and new_imports:
            self._import_dependencies(
                graph,
                cache=cache,
                recursive=recursive,
                recursive_limit=recursive_limit - 1,
            )


def find_root_file(start: Optional[OntologyLocation] = None) -> Optional[Path]:
    """
    Starting at the current directory, traverse upwards until it finds a .ontoenv directory

    :param start: The directory to start from. If None, it starts from the current directory.
    :return: The path to the .ontoenv directory, or None if not found.
    """
    if start is None:
        start = Path(os.getcwd())
    start = Path(start)

    oe_dir = start / ".ontoenv"

    # if '.ontoenv' exists and is a directory
    if os.path.exists(oe_dir):
        if not oe_dir.is_dir():
            raise Exception(f".ontoenv ({oe_dir}) must be a directory")
        return oe_dir

    if len(start.parts) == 1:
        return None

    return find_root_file(start.parent)


def find_ontology_files(search_dir: Path, ignore_patterns: Optional[List[str]] = None) -> Generator[Path, None, None]:
    """
    Starting at the given directories, explore all subtrees and gather all ontology
    files, as identified by their file extension (see FILE_EXTENSIONS).
    Returns a generator which yields all files matching one of the FILE_EXTENSIONS

    :param search_dirs: The directories to start from.
    :return: A generator yielding all ontology files.
    """
    # use parent of the .ontoenv directory
    for filename in search_dir.iterdir():
        if ignore_patterns and any(fnmatch.fnmatch(str(filename), pattern) for pattern in ignore_patterns):
            continue
        full_suffix = ".".join(filename.suffixes)
        matches_extension = (
            filename.suffix in FILE_EXTENSIONS or full_suffix in FILE_EXTENSIONS
        )
        if matches_extension and not filename.is_dir():
            yield filename
        if not filename.is_dir():
            continue
        for newfn in find_ontology_files(filename, ignore_patterns):
            yield newfn


def _is_online(uri: str) -> bool:
    """
    Returns True if the URI is online (starts with http:// or https://)

    :param uri: The URI to check
    :return: True if the URI is online, False otherwise
    """
    return any(uri.startswith(prefix) for prefix in ONLINE_PREFIXES)
