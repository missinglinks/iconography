import requests
import json
from rdflib import Graph, RDF

from jsonld_utils import JsonLDContextMapper


# Files
RDF_DATASET = "../data/rdf/altenburg_keramik.json"
RDF_WIKI = "../data/rdf/wikidata.json"

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)

def generate_web_dataset():

    #load rdf dataset
    data = json.dumps(json.load(open(RDF_DATASET)))
    g = Graph()
    dataset = g.parse(data=data, format="json-ld")

    

