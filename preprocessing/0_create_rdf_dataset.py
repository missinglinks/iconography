import json
import os
import spacy
import pandas as pd
from pit.prov import Provenance
from rdflib import Graph, Namespace, URIRef, Literal, RDF

from jsonld_utils import JsonLDContextMapper

# Files
METADATA = "../data/csv/vasen_altenburg.csv"
CONCEPTS = "../data/csv/concepts.csv"
EXPORT_RDF = "../data/rdf/altenburg_keramik.jsonld"

# NLP Setup
nlp = spacy.load("de")

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)

# Graph Namespaces
ALTENBURG = Namespace("https://www.lindenau-museum.de/antike/")
VISUAL_ITEM = Namespace("https://www.lindenau-museum.de/antike/VisualItem/")

def nn_norm_tokens(s):
    """
    Return as a list of the normalized forms of the nouns in string :s:
    """
    nn = set()

    processed = nlp(s)
    for sent in processed.sents:
        for token in sent:
            if token.tag_ == "NN":
                nn.add(token.norm_)
    return list(nn)
        
def main():

    # load object mateadata
    metadata = pd.read_csv(METADATA, sep=";")
    metadata = json.loads(metadata.to_json(orient="records"))

    # load concept list
    concepts = pd.read_csv(CONCEPTS)
    concepts = json.loads(concepts.to_json(orient="records"))
    concept_dict = { x["concept"]: x for x in concepts if x["wkp"] }


    # build rdf dataset
    graph = Graph()
    for obj in metadata:

        if obj["Ikonographie"]:
            id_ = obj["Inventarnummer"].replace(" ", "_")
            obj_uri = ALTENBURG[id_]
            graph.add( (obj_uri, LA["label"], Literal(obj["Titel"])) )
            graph.add( (obj_uri, RDF.type, LA["ManMadeObject"]))


            #add visualItem
            graph.add( (obj_uri, LA["shows"], VISUAL_ITEM[id_] ) )
            graph.add( (VISUAL_ITEM[id_], RDF.type, LA["VisualItem"]) )

            # add inconographic subjects to graph
            for token in nn_norm_tokens(obj["Ikonographie"]):
                if token in concept_dict:
                    
                    wkp_uri = URIRef(concept_dict[token]["wkp"])

                    graph.add( (VISUAL_ITEM[id_], LA["represents"], wkp_uri) )

        #filepath = os.path.join("..","assets","{}.jsonld".format(id_))
    graph.serialize(destination=EXPORT_RDF, format='json-ld', context=CONTEXT)



if __name__ == "__main__":
    main()