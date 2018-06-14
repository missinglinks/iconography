import requests
import os
import json
from rdflib import Namespace

class JsonLDContextMapper(object):
    """
    Returns full rdflib URIS for term specified in a JSON-LD context
    
    Use:
    
    #context file as url
    cm = JsonLDContextMapper("http://example.com/context.json")
    
    #local context file
    cm = JsonLDContextMapper("data/context.json")
    
    #get term URIRef object
    uri = cm["part_of"]

    """
       
    def __init__(self, context_file):
        print("consume context {}".format(context_file))
        # load file or raise error
        if context_file.startswith("http"):
            rsp = requests.get(context_file)
            data = json.loads(rsp.text)
        elif os.path.exists(context_file):
            data = json.load(open(context_file))
        else:
            raise TypeError("Invalid context file url or location")
            
        self._namespaces = {}
        self._terms = {}
        
        #build namespace dict
        for term, specification in data["@context"].items():
            if self._is_url(specification):
                self._namespaces[term] = Namespace(specification)
                
        #build terms dict
        for term, specification in data["@context"].items():
            if type(specification) == dict:
                uri = self._build_uri(specification)
                if uri:
                    self._terms[term] = uri

    def __getitem__(self, item):
        return self._terms[item]

    def _is_url(self, obj):
        """
        Checks if :obj: is url
        """
        if type(obj) == str:
            if obj.startswith("http"):
                return True
        return False
    
    def _build_uri(self, specification):
        """
        Builds full uri from the JsonLD context specification for a term.
        Return reflib URIRef object.
        """
        if "@id" in specification:
            if ":" in specification["@id"]:
                parts = specification["@id"].split(":")
                #skip if namespace not defined
                if parts[0] not in self._namespaces:
                    return None
                ns = self._namespaces[parts[0]]
                term = parts[1]
                return ns[term]
        return None