import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Load the JSON data
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

        # Collect the marks for provided names
        marks = []
        for entry in data:
            if entry['name'] in names:
                marks.extend(entry['marks'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if marks:
            response = {"marks": sorted(marks)}  # Sort the marks
        else:
            response = {"error": "Name not found"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
