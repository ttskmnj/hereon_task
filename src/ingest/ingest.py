import os
import json
from src.utils import kg, kill_kg
import logging
from typing import List, Dict


DATA = './data/'
BATCH_SIZE = 25

logging.basicConfig(level=logging.INFO)


def escape_quotation(text):
    return text.replace('"', '\\"') if isinstance(text, str) else text


def extract() -> List[Dict]:
    pkgs = []

    try:
        for parent in os.listdir(DATA):
            for pkg in os.listdir(DATA+parent):
                with open(f"{DATA}{parent}/{pkg}/elm.json", 'r') as f:
                    data = json.load(f)
                    pkgs.append(data)
    except Exception as e:
        logging.error(f"Error during extraction: {e}")
    return pkgs


def load(pkgs):
    for batch_index in range(0, len(pkgs), BATCH_SIZE):
        batch = pkgs[batch_index:batch_index+BATCH_SIZE]
        query = ""

        try:
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
        except Exception as e:
            logging.error(f"Error during loading batch {batch_index}: {e}")


def start():
    logging.info("Starting the ingestion ...")

    try:
        # delete all nodes and relatioships
        kill_kg()
        logging.info("Cleared existing nodes and relationships.")

        # extract packages from the data directory
        pkgs = extract()
        logging.info(f"Extracted {len(pkgs)} packages.")

        # load packages into the knowledge graph
        load(pkgs)
        logging.info("Ingestion completed.")
    except Exception as e:
        logging.error(f"Error in the ingestion process: {e}")
