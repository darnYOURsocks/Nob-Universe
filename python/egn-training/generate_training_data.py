"""
Simple training data generator for Emotional Gravity Node (EGN)
Generates synthetic pairs of emotional nodes and computes the ground-truth gravity
saves CSV to `python/egn-training/training_data.csv`.
"""
import json
import csv
import math
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / 'databases' / 'emotional-nodes.json'
OUT_PATH = Path(__file__).resolve().parent / 'training_data.csv'

try:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
        nodes = db.get('egn_nodes', [])
except Exception:
    nodes = []

if not nodes:
    # fallback random nodes
    nodes = [
        { 'id':'EGN-A', 'position':{'x':0,'y':0,'z':0}, 'intensity':0.8, 'clarity':0.6, 'stability':0.4 },
        { 'id':'EGN-B', 'position':{'x':1.5,'y':0.5,'z':-0.5}, 'intensity':0.7, 'clarity':0.55, 'stability':0.6 }
    ]

# generator function matching engine formula
G_e = 0.87

def dist(a,b):
    return math.sqrt((a['position']['x']-b['position']['x'])**2 + (a['position']['y']-b['position']['y'])**2 + (a['position']['z']-b['position']['z'])**2)

with open(OUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id_a','id_b','intensity_a','intensity_b','clarity_a','clarity_b','stability_a','stability_b','distance','force','wellDepth','acceleration'])

    # produce combinations and random samples
    pairs = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            pairs.append((nodes[i], nodes[j]))

    # add random synthetic pairs
    for _ in range(100):
        a = random.choice(nodes)
        bpos = { 'x': random.uniform(-3,3), 'y': random.uniform(-1,1), 'z': random.uniform(-3,3) }
        b = {
            'id': f'RAND-{random.randint(1000,9999)}',
            'position': bpos,
            'intensity': random.random(),
            'clarity': random.random(),
            'stability': random.random()
        }
        pairs.append((a,b))

    for a,b in pairs:
        d = max(dist(a,b), 0.01)
        I1 = max(0, min(1, a.get('intensity',0)))
        I2 = max(0, min(1, b.get('intensity',0)))
        C1 = max(0, min(1, a.get('clarity',0)))
        C2 = max(0, min(1, b.get('clarity',0)))
        force = (G_e * (I1 * I2 * C1 * C2)) / (d*d)
        wellDepth = force * (1 - ((C1 + C2)/2))
        emotionalMass = max(0.01, a.get('stability',0.5) + b.get('stability',0.5) + 0.1)
        acc = force / emotionalMass
        writer.writerow([a.get('id'), b.get('id'), I1, I2, C1, C2, a.get('stability',0.5), b.get('stability',0.5), d, force, wellDepth, acc])

print(f"Wrote training data to {OUT_PATH}")
