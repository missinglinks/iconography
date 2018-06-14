import requests
import json
from rdflib import Graph, RDF

from jsonld_utils import JsonLDContextMapper

# Wikidata Element URL
WIKIDATA = "https://www.wikidata.org/wiki/Special:EntityData/{wkp}.rdf"

# Files
RDF_DATASET = "../data/rdf/altenburg_keramik.json"
RDF_WIKI = "../data/rdf/wikidata.json"
ASSET_DIR = "../assets"

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

def load_rdf_file(filepath):
    data = json.dumps(json.load(open(RDF_DATASET)))
    g = Graph()
    return  g.parse(data=data, format="json-ld")

def load_datasets():
    g = Graph()
    for filename in tqdm(os.listdir(ASSET_DIR)):
        filepath = os.path.join(ASSET_DIR, filename)
        g += load_rdf_file(filepath)
    return g

def fetch_wikidata(url):
    rsp = requests.get(WIKIDATA.format(wkp=url.split("/")[-1]))
    wiki += g.parse(data=rsp.text)
    return url

def build_dataset()
    g = load_datasets()

    wiki = {}
    


if __name__ == "__main__":
    build_dataset()