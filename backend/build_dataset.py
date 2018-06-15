import requests
import json
import os
from rdflib import Graph, RDFS, Namespace, URIRef, RDF
from tqdm import tqdm

from jsonld_utils import JsonLDContextMapper

# Wikipedia API
WIKIPEDIA = "https://de.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={title}"

# Wikidata Element URL
WIKIDATA = "https://www.wikidata.org/wiki/Special:EntityData/{wkp}.rdf"

# Files
RDF_DATASET = "../data/rdf/altenburg_keramik.json"
RDF_WIKI = "../data/rdf/wikidata.json"
ASSET_DIR = "../assets/rdf"

OBJECTS_DATASET = "../data/json/objects.json"
CONCEPTS_DATASET = "../data/json/concepts.json"

WDT = Namespace("http://www.wikidata.org/prop/direct/")
SCHEMA = Namespace("http://schema.org/")

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)




# # Wikidata queries
# RELATION_QUERY = """
# SELECT distinct ?item
# #P451 partner
# #P3373 sibling
# #P26 spouse
# #P40 child
# #P460 said to be the same as
# #P25 mother
# #P22 father
# WHERE 
# {{
#   wd:{wkp} wdt:P451|wdt:P3373|wdt:P26|wdt:P40|wdt:P460|wdt:P25|wdt:P22 ?item.
# }}
# """

def load_rdf_file(filepath):

    data = json.dumps(json.load(open(filepath)))
    g = Graph()
    return  g.parse(data=data, format="json-ld")

def load_datasets():
    g = Graph()
    for filename in tqdm(os.listdir(ASSET_DIR)):
        filepath = os.path.join(ASSET_DIR, filename)
        g += load_rdf_file(filepath)
    return g


def url_to_entity (url):
    wkp = url.split("/")[-1]
    entity = "http://www.wikidata.org/entity/{}".format(wkp)
    return URIRef(entity)


def fetch_wikipedia_summary(title):
    rsp = requests.get(WIKIPEDIA.format(title=title))

    data = json.loads(rsp.text)["query"]
    for page, info in data["pages"].items():
        return info["extract"]
    

def fetch_wikidata(url):
    g = Graph()
    
    rsp = requests.get(WIKIDATA.format(wkp=url.split("/")[-1]))
    wiki = g.parse(data=rsp.text)

    wkp = url_to_entity(url)

    data = {}
    data["images"] = []

    # get german label
    for res in wiki.triples((wkp, RDFS.label, None)):
        label = res[2]
        if label.language == "de":
            data["label"] = str(label)    

    # get german wiki link
    for res in wiki.triples((None, RDF.type, SCHEMA.Article)):
        if "de." in res[0]:
            data["wikipedia_link"] = str(res[0])
        
    for res in wiki.triples( (wkp, WDT.P18, None) ):
        data["images"].append(str(res[2]))

    data["wikipedia_summary"] = fetch_wikipedia_summary(data["wikipedia_link"].split("/")[-1])

    return data

def build_dataset():

    wiki = {}
    dataset = {}

    g = load_datasets()
    objects = [ x[0] for x in g.triples( (None, RDF.type, LA["ManMadeObject"]) ) ]
    for obj in objects:
        print(obj)

        #random_obj = random.choice(objects)
        label = [ g.value(obj, RDFS.label) ]
        vis_item = [ x[2] for x in g.triples( (obj, LA["shows"], None) ) ]
        description = g.value(vis_item[0], RDFS.comment)
        print(description)
        elements = [ str(x[2]) for x in g.triples( (vis_item[0], LA["represents"], None) )]

        dataset[obj] = {
            "label": label,
            "elements": elements,
            "description": description
        }

        for element in elements:
            print("\t"+element)
            if element not in wiki:
                wiki[element] = fetch_wikidata(element)
        

    with open(OBJECTS_DATASET, "w") as f:
        json.dump(dataset, f, indent=4)

    with open(CONCEPTS_DATASET, "w") as f:
        json.dump(wiki, f, indent=4 )
    


if __name__ == "__main__":
    build_dataset()
    #fetch_wikidata("https://www.wikidata.org/wiki/Q34201")