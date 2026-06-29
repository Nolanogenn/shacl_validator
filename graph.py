import re
import logging

logger = logging.getLogger(__name__)

pattern = r'[^ ;]+'
def getNamespace(uri, prefixes):
    if uri == 'a':
        return prefixes['rdf']
    name, _ = uri.split(':')
    try:
        return prefixes[name]
    except Exception as e:
        raise e

class Resource():
    def __init__(self, uri):
        self.uri = uri
    def __repr__(self):
        return self.uri

class Graph():
    def __init__(self, graph_str):
        self.graph_str = graph_str
        logging.basicConfig(filename='graphParser.log', level=logging.DEBUG)
        self.prefixes = {}
        self.resources = set()
        self.shortForms = {}
        self.properties = {}
        self.edges = {}

    def parse_prefix_line(self,line):
        _, name, url, _ = line.split(' ')
        if name in self.prefixes:
            raise Exception(f"overlap for name {name}, already present with val {self.prefixes[name]}")
        self.prefixes[name[:-1]] = url[1:-1]
    
    def getFullUri(self, uri):
        if uri.startswith('<') and uri.endswith('>'):
            return uri[1:-1]
        namespace = getNamespace(uri, self.prefixes)
        name = uri.split(':')[1]
        return f"{namespace}{name}"

    def parse(self):
        currSubj = None
        pred = None
        obj = None
        for line in self.graph_str:
            try:
                if line.startswith("#"):
                    continue
                if line.startswith("@"):
                    self.parse_prefix_line(line)
                else:
                    resources = re.findall(pattern, line)
                    resources = [self.getFullUri(u) for u in resources]
                    nRes = len(resources)
                    if resources:
                        if nRes == 1:
                            currSubj = resources[0]
                        elif nRes == 3:
                            currSubj, pred, obj = resources
                        else:
                            pred, obj = resources
                    else:
                        currSubj = pred = obj = None
                    if pred and obj:
                        print(currSubj, pred, obj) 
            except Exception as e:
                logger.error(e)


         


