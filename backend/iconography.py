import os
import sys
import time
import json
import random
from rdflib import Graph,RDF
from tqdm import tqdm 

from jsonld_utils import JsonLDContextMapper

from flask import Flask, jsonify
app = Flask(__name__)
PORT = 6660

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)

RDF_DATASET = "../data/rdf/altenburg_keramik.jsonld"
ASSET_DIR = "../assets"

def load_rdf_file():
    data = json.dumps(json.load(open(RDF_DATASET)))
    g = Graph()
    return  g.parse(data=data, format="json-ld")

# def load_dataset():
#     g = Graph()
#     for filename in tqdm(os.listdir(ASSET_DIR)):
#         filepath = os.path.join(ASSET_DIR, filename)
#         g += load_rdf_file(filepath)
#     return g


DATASET = load_rdf_file()

@app.route('/object')
def object():

    objects = [ x[0] for x in DATASET.triples( (None, RDF.type, LA["ManMadeObject"]) ) ]
    random_obj = random.choice(objects)
    vis_item = [ x[2] for x in DATASET.triples( (random_obj, LA["shows"], None) ) ]
    elements = [ x[2] for x in DATASET.triples( (vis_item[0], LA["represents"], None) )]

    return jsonify({
        "id": random_obj,
        "elements": elements
    })




def start_backend(debug=False):
    app.run(debug=debug, port=PORT, use_reloader=False)

if __name__ == "__main__":
    start_backend()