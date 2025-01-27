import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get the directory of the current script
            dir_path = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(dir_path, "../q-vercel-python.json")

            # Load JSON data
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            # Parse query parameters
            query_string = self.path.split('?')[-1]
            params = dict(qc.split('=') for qc in query_string.split('&') if '=' in qc)

            # Check if 'name' query parameter is present
            if 'name' in params:
                names = params['name'].split(',')
                result = {name: data.get(name, "Not Found") for name in names}
            else:
                result = {"error": "Please provide a 'name' query parameter"}

            # Send JSON response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Data file not found"}).encode('utf-8'))
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
