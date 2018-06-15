import os
import sys
import time
import json
import random
from rdflib import Graph,RDF
from tqdm import tqdm 
from PIL import Image

from jsonld_utils import JsonLDContextMapper

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
PORT = 6660

# Linked art context file
CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LA = JsonLDContextMapper(CONTEXT)

OBJECT_DATASET = "../data/json/objects.json"
CONCEPTS_DATASET = "../data/json/concepts.json"

OBJECTS = json.load(open(OBJECT_DATASET))
CONCEPTS = json.load(open(CONCEPTS_DATASET))


@app.route('/object')
def object():
    
    while True:
        rnd = random.choice(list(OBJECTS.items()))
        if len(rnd[1]["elements"]) > 0:
            break
    id_ = rnd[0]
    data = rnd[1]

    elements = []
    for element in data["elements"]:
        elements.append(CONCEPTS[element])
    #for element in data["elements"]
    
    im = Image.open("../../iconography-frontend/public/assets/{} Lindenau-Museum Altenburg.jpg".format(id_.split("/")[-1]),)
    width, height = im.size
    print(width, height)


    return jsonify({
        "id": id_,
        "title": data["label"],
        "description": data["description"],
        "image": "./assets/{} Lindenau-Museum Altenburg.jpg".format(id_.split("/")[-1]),
        "image_s": "./assets/s/{} Lindenau-Museum Altenburg.jpg".format(id_.split("/")[-1]),
        "rdf_file": "./assets/rdf/{}.jsonld".format(id_.split("/")[-1]),
        "width": width,
        "height": height,
        "elements": elements
    })




def start_backend(debug=True):
    app.run(debug=debug, port=PORT, use_reloader=False)

if __name__ == "__main__":
    start_backend()