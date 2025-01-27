import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Set CORS headers to allow requests from any origin
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')

        # Load the JSON data
        dir_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(dir_path, "../q-vercel-python.json")
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get('name', [])

        # If no name was provided
        if not names:
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Please provide a 'name' query parameter"}).encode('utf-8'))
            return

        # Collect the marks in the same order as the requested names
        marks = []
        for name in names:
            found = False
            for entry in data:
                if entry['name'] == name:
                    marks.append(entry['marks'])
                    found = True
                    break
            if not found:
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Name '{name}' not found"}).encode('utf-8'))
                return

        self.end_headers()

        # Respond with the marks
        response = {"marks": marks}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
