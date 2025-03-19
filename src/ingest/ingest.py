import os
import json
from src.utils import kg, kill_kg

DATA = './data/'
BATCH_SIZE = 25


def escape_quotation(text):
    return text.replace('"', '\\"') if isinstance(text, str) else text


def extract():
    pkgs = []

    for parent in os.listdir(DATA):
        for pkg in os.listdir(DATA+parent):
            with open(f"{DATA}{parent}/{pkg}/elm.json", 'r') as f:
                data = json.load(f)
                pkgs.append(data)

    return pkgs


def load(pkgs):
    for batch_index in range(0, len(pkgs), BATCH_SIZE):
        batch = pkgs[batch_index:batch_index+BATCH_SIZE]
        query = ""

        for i, pkg in enumerate(batch):
            query += f"""
            MERGE (p_{i}:Package {{name: "{pkg['name']}"}})
            ON CREATE
                SET
                    p_{i}.version = "{pkg['version']}",
                    p_{i}.summary = "{escape_quotation(pkg['summary'])}",
                    p_{i}.license = "{pkg['license']}"
            ON MATCH
                SET
                    p_{i}.version = "{pkg['version']}",
                    p_{i}.summary = "{escape_quotation(pkg['summary'])}",
                    p_{i}.license = "{pkg['license']}"
            """

            for j, dep in enumerate(pkg['dependencies'].keys()):
                query += f"""
                    MERGE (d_{i}_{j}:Package {{name: "{dep}"}})
                    MERGE (p_{i})-[:DEPENDS_ON]->(d_{i}_{j})
                """

        kg.query(query)


def start():
    # delete all nodes and relatioships
    kill_kg()

    pkgs = extract()
    load(pkgs)
