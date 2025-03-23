# Hereon Task
## Requirements
You need Docker, Docker-compose and Python to be installed on your machine to run this application.

## How to start application
1. clone this repository
```
$ git clone git@github.com:ttskmnj/hereon_task.git
$ cd hereon_task

```
2. prepare python virtual environment
```
$ python -m venv .venv # this command is for MacOS. it can be different depends on OS.
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3. set environment variables 
create `.env` file in root directory of this repo and set following values.
```
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<NEO4J_PASSWORD_SHOULD_BE _LONGER_THAN_8>
NEO4J_URI=bolt://localhost:7687
NEO4J_DATABASE=neo4j
```
4. Start containers
```
$ docker-compose up -d
```
This command start neo4j and app containers and ingest Elm packages to knowledge graph.<br>
Now Flask endpoints are ready and you can send GET request.

## How to check data in Knowledge Graph
1. open `http://localhost:7474` with browser and login to dashboard with username `neo4j` and password you set in `.env`
2. run following command in neo4j prompt to show all nodes and relationships
```
neo4j$ MATCH (n) RETURN n
```

## How to get direct and indirect dependencies for package
open `http://localhost:5001/dependencies/<PAKCGE NAME>` with browser. it will return list of packages which given package is directly or indirectly depend on them.<br>
You can get package names by opening `http://localhost:5001/package_names`. this endpoint will return all package names.
