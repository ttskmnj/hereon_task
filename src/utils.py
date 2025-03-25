#  from langchain_neo4j import Neo4jGraph
from langchain_community.graphs import Neo4jGraph
import os
from dotenv import load_dotenv

load_dotenv()


kg = Neo4jGraph(
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE"),
    url=os.getenv("NEO4J_URI"),
)


def kill_kg():
    # delete all nodes and relations
    query = """
        MATCH (n)
        DETACH DELETE n;
    """

    kg.query(query)