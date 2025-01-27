import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Load JSON data from file
        dir_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(dir_path, "../q-vercel-python.json")
        
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Parse query parameters
        query_string = self.path.split('?')[-1]
        params = {k: v for k, v in (param.split('=') for param in query_string.split('&') if '=' in param)}

        # Check for required 'name' parameter
        if 'name' not in params:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Please provide a 'name' query parameter"}).encode('utf-8'))
            return

        # Find the requested name in the data
        name = params['name']
        result = [entry['marks'] for entry in data if entry['name'] == name]

        # Send response based on search results
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if result:
            response = {"name": name, "marks": result[0]}
        else:
            response = {"error": "Name not found"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
