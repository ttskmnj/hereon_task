from flask import Flask, jsonify
from typing import List
from ..utils import kg
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def get_package_names() -> List[str]:
    """Returns all package names."""
    query = "MATCH (pkg:Package) RETURN pkg.name"
    pkg_names = \
        [pkg['pkg.name'] for pkg in kg.query(query)]

    return pkg_names


def get_all_dependencies(pkg_name: str) -> List[str]:
    """Returns all dependencies for given package."""
    query = f"""
        MATCH
            (pkg:Package {{name: '{pkg_name}'}})-[:DEPENDS_ON*]->(dep:Package)
        RETURN
            DISTINCT dep.name"""
    deps = kg.query(query)
    dep_names = [dep['dep.name'] for dep in deps]

    return dep_names


@app.errorhandler(Exception)
def handle_error(e: Exception) -> tuple:
    """Handle uncaught exceptions."""
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error"}), 500


@app.route('/package_names', methods=['GET'])
def get_packages() -> tuple:
    """Returns all package names."""
    try:
        return jsonify(get_package_names())
    except Exception as e:
        logging.error(f"Error in /package_names endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/dependencies/<path:pkg_name>', methods=['GET'])
def get_dependencies(pkg_name: str) -> tuple:
    """Returns all dependencies for given package."""
    try:
        if pkg_name not in get_package_names():
            logging.warning(f"Package not found: {pkg_name}")
            return jsonify({"error": "Package not found"}), 404

        return jsonify(get_all_dependencies(pkg_name))
    except Exception as e:
        logging.error(f"Error in /dependencies endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
