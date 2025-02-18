from flask import Flask, jsonify, request
import psycopg2
import yaml
import os

app = Flask(__name__)

# Load configuration from YAML.
# The file path is specified via the environment variable QUERY_MAPPING_FILE.
CONFIG_PATH = os.environ.get("QUERY_MAPPING_FILE", "query_mappings.yaml")
try:
    with open(CONFIG_PATH, 'r') as file:
        mappings = yaml.safe_load(file)
except Exception as e:
    mappings = []
    app.logger.error(f"Error loading config: {e}")

# Database connection details are injected via environment variables.
db_config = {
    'user': os.environ.get('DB_USER', 'postgres'),
    'host': os.environ.get('DB_HOST', 'postgres-service'),
    'database': os.environ.get('DB_NAME', 'mydb'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'port': int(os.environ.get('DB_PORT', 5432))
}

def get_mapping_for_endpoint(request_path):
    """Find a configuration mapping matching the requested path."""
    for mapping in mappings:
        # Match full path (assuming leading slash)
        if mapping.get('api_endpoint') == request_path:
            return mapping
    return None

def transform_data(data, mapping):
    """
    Transform query result rows based on the column mapping.
    'mapping' is a dict mapping database column names to response keys.
    """
    columns_mapping = mapping.get('columns', {})
    result = []
    for row in data:
        row_dict = {}
        # This simplistic implementation assumes the order of the columns in the query
        # matches the order of keys in the mapping.
        for idx, (db_col, resp_field) in enumerate(columns_mapping.items()):
            row_dict[resp_field] = row[idx]
        result.append(row_dict)
    return result

@app.route('/<path:endpoint>', methods=['GET'])
def query_endpoint(endpoint):
    full_path = "/" + endpoint
    mapping = get_mapping_for_endpoint(full_path)
    if not mapping:
        return jsonify({'error': f'Endpoint {full_path} not found'}), 404

    query = mapping.get('query')
    if not query:
        return jsonify({'error': 'No query defined for endpoint'}), 500

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        # For production, implement parameterized queries to avoid SQL injection.
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        transformed = transform_data(data, mapping)
        return jsonify(transformed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
