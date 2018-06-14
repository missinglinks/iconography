import requests
import json
from rdflib import Graph, RDF

from jsonld_utils import JsonLDContextMapper

# Wikidata Element URL
WIKIDATA = "https://www.wikidata.org/wiki/Special:EntityData/{wkp}.rdf"

# Files
RDF_DATASET = "../data/rdf/altenburg_keramik.json"
RDF_WIKI = "../data/rdf/wikidata.json"

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)

# Wikidata queries
RELATION_QUERY = """
SELECT distinct ?item
#P451 partner
#P3373 sibling
#P26 spouse
#P40 child
#P460 said to be the same as
#P25 mother
#P22 father
WHERE 
{{
  wd:{wkp} wdt:P451|wdt:P3373|wdt:P26|wdt:P40|wdt:P460|wdt:P25|wdt:P22 ?item.
}}
"""

def fetch_wikidata():

    #load rdf dataset
    data = json.dumps(json.load(open(RDF_DATASET)))
    g = Graph()
    dataset = g.parse(data=data, format="json-ld")

    wiki_ids = set()
    for s, p, o in dataset.triples( (None, LA["represents"], None) ):
        wiki_ids.add(str(o))

    # get wikidata rdfs
    wiki = Graph()
    for url in wiki_ids:
        rsp = requests.get(WIKIDATA.format(wkp=url.split("/")[-1]))
        wiki += g.parse(data=rsp.text)

    # get related rdfs


    wiki.serialize(RDF_WIKI, format="json-ld")
    
    #print(wiki_ids)

fetch_wikidata()