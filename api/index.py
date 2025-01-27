import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = self.path.split('?')[-1]  # Extract query string
        params = dict(q.split('=') for q in query.split('&'))  # Convert query to dict

        try:
            # Load JSON data
            with open(os.path.join(os.path.dirname(__file__), '../q-vercel-python.json')) as f:
                data = json.load(f)
            
            # Extract names from query
            names = params.get('name', '').split(',')

            # Filter marks for the given names
            result = [entry['marks'] for entry in data if entry['name'] in names]

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"marks": result}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
