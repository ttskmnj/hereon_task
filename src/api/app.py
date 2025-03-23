from flask import Flask, jsonify
from ..utils import kg


app = Flask(__name__)


def get_package_names():
    """Returns all package names."""
    query = "MATCH (pkg:Package) RETURN pkg.name"
    pkg_names = \
        [pkg['pkg.name'] for pkg in kg.query(query)]

    return pkg_names


def get_all_dependencies(pkg_name):
    """Returns all dependencies for given package."""
    query = f"""
        MATCH
            (pkg:Package {{name: '{pkg_name}'}})-[:DEPENDS_ON*]->(dep:Package)
        RETURN
            DISTINCT dep.name"""
    deps = kg.query(query)
    dep_names = [dep['dep.name'] for dep in deps]

    return (dep_names)


@app.route('/package_names', methods=['GET'])
def get_packages():
    """Returns all package names."""
    return jsonify(get_package_names())


@app.route('/dependencies/<path:pkg_name>', methods=['GET'])
def get_dependencies(pkg_name):
    """Returns all dependencies for given package."""
    if pkg_name not in get_package_names():
        return jsonify({"error": "Package not found"}), 404

    return jsonify(get_all_dependencies(pkg_name))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
