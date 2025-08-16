#!/usr/bin/env python3
"""
Simple HTTP server to serve the SOPs Knowledge Base
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from pathlib import Path

class SOPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to the current working directory (where the script is run from)
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/web/index.html'
        elif self.path.startswith('/vault/') and self.path.endswith('.md'):
            # Serve markdown files with proper content type
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            file_path = Path(self.path[1:])  # Remove leading '/'
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_error(404, "File not found")
            return
        
        return super().do_GET()

def main():
    port = 8000  # Changed from 8080 to 8000
    server_address = ('localhost', port)
    
    print(f"SOPs Knowledge Base Server")
    print(f"Starting server on http://localhost:{port}")
    print(f"Serving from: {os.getcwd()}")
    print(f"Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        httpd = HTTPServer(server_address, SOPHandler)
        
        # Try to open the browser automatically
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            pass
        
        print(f"Server running at http://localhost:{port}")
        print(f"Obsidian Vault: http://localhost:{port}/vault/")
        print(f"Templates: http://localhost:{port}/vault/templates/")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
