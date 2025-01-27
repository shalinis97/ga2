import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(dir_path, "../q-vercel-python.json")
        
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get('name', [])

        if not names:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Please provide a 'name' query parameter"}).encode('utf-8'))
            return

        # Look up marks for provided names
        result = {name: entry['marks'] for entry in data for name in names if entry['name'] == name}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if result:
            response = {"marks": result}
        else:
            response = {"error": "Name(s) not found"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
