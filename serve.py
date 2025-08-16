#!/usr/bin/env python3
"""
Simple HTTP server to serve the SOPs Knowledge Base
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from pathlib import Path
from urllib.parse import unquote

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
            # Serve the vault index
            self.serve_vault_index()
            return
        elif self.path.startswith('/vault/') and self.path.endswith('.md'):
            # Serve markdown files as HTML
            self.serve_markdown_as_html()
            return
        elif self.path == '/vault' or self.path == '/vault/':
            self.serve_vault_index()
            return
        
        return super().do_GET()
    
    def serve_vault_index(self):
        """Generate an index page for the vault"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Files are in the vault/ subdirectory
        vault_path = Path('vault')
        html = self.generate_vault_html(vault_path)
        self.wfile.write(html.encode('utf-8'))
    
    def serve_markdown_as_html(self):
        """Serve markdown files as HTML"""
        # URL decode the path and remove the /vault/ prefix
        decoded_path = unquote(self.path)  # Keep the leading '/' for now
        
        if decoded_path.startswith('/vault/'):
            # Remove /vault/ prefix to get the relative path within the vault
            relative_path = decoded_path[7:]  # Remove '/vault/'
            file_path = Path('vault') / relative_path
        else:
            self.send_error(404, f"Invalid path: {decoded_path}")
            return
        
        if file_path.exists() and file_path.suffix == '.md':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert markdown to basic HTML (pass relative path for breadcrumbs)
            relative_file_path = Path(relative_path)
            html = self.markdown_to_html(content, relative_file_path)
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, f"File not found: {file_path}")
    
    def generate_vault_html(self, vault_path):
        """Generate HTML for the vault index with enhanced navigation"""
        # Organize files by category
        categories = {}
        file_count = 0
        
        for root, dirs, filenames in os.walk(vault_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = Path(root) / filename
                    rel_path = file_path.relative_to(vault_path)
                    folder = rel_path.parent if rel_path.parent != Path('.') else 'Root'
                    
                    if folder not in categories:
                        categories[folder] = []
                    categories[folder].append(rel_path)
                    file_count += 1
        
        # Sort categories and files within each category
        for category in categories:
            categories[category].sort()
        
        # Get category icons and descriptions
        category_info = {
            'Operations': {'icon': '⚙️', 'color': '#3498db', 'desc': 'Daily operational procedures'},
            'Emergency': {'icon': '🚨', 'color': '#e74c3c', 'desc': 'Critical incident response'},
            'templates': {'icon': '📝', 'color': '#9b59b6', 'desc': 'Templates for creating new SOPs'},
            'Root': {'icon': '📋', 'color': '#2c3e50', 'desc': 'General documentation'}
        }
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOPs Knowledge Base</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            margin: 0; padding: 20px; line-height: 1.6; 
            background: #f8f9fa;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 40px 20px; margin: -20px -20px 30px;
            border-radius: 0 0 10px 10px;
        }
        .header h1 { margin: 0; font-size: 2.5em; }
        .header p { margin: 10px 0 0; opacity: 0.9; }
        .stats { 
            background: white; border-radius: 8px; padding: 20px; 
            margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex; gap: 30px; align-items: center;
        }
        .stat { text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; color: #3498db; }
        .stat-label { color: #666; font-size: 0.9em; }
        .categories { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .category { 
            background: white; border-radius: 10px; padding: 25px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;
        }
        .category:hover { transform: translateY(-2px); }
        .category-header { display: flex; align-items: center; margin-bottom: 15px; }
        .category-icon { font-size: 1.5em; margin-right: 10px; }
        .category-title { font-size: 1.3em; font-weight: bold; margin: 0; }
        .category-desc { color: #666; font-size: 0.9em; margin-bottom: 15px; }
        .file-list { list-style: none; padding: 0; margin: 0; }
        .file-list li { margin: 8px 0; }
        .file-list a { 
            text-decoration: none; color: #3498db; font-weight: 500;
            display: block; padding: 8px 12px; border-radius: 5px;
            transition: background 0.2s;
        }
        .file-list a:hover { background: #f8f9fa; color: #2980b9; }
        .search-box { 
            background: white; border-radius: 8px; padding: 15px; 
            margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .search-input { 
            width: 100%; padding: 12px; border: 2px solid #ddd; 
            border-radius: 6px; font-size: 1em;
            box-sizing: border-box;
        }
        .search-input:focus { outline: none; border-color: #3498db; }
        .quick-actions {
            background: white; border-radius: 8px; padding: 20px;
            margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .quick-actions h3 { margin: 0 0 15px; color: #2c3e50; }
        .action-buttons { display: flex; gap: 10px; flex-wrap: wrap; }
        .action-btn {
            padding: 8px 16px; border: none; border-radius: 5px;
            background: #3498db; color: white; text-decoration: none;
            font-weight: 500; transition: background 0.2s;
        }
        .action-btn:hover { background: #2980b9; }
        .action-btn.secondary { background: #95a5a6; }
        .action-btn.secondary:hover { background: #7f8c8d; }
        @media (max-width: 768px) {
            .categories { grid-template-columns: 1fr; }
            .stats { flex-direction: column; gap: 15px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 SOPs Knowledge Base</h1>
        <p>Your dynamic Standard Operating Procedures vault • Last updated: """ + self.get_last_modified_time(vault_path) + """</p>
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-number">""" + str(file_count) + """</div>
            <div class="stat-label">Total SOPs</div>
        </div>
        <div class="stat">
            <div class="stat-number">""" + str(len(categories)) + """</div>
            <div class="stat-label">Categories</div>
        </div>
        <div class="stat">
            <div class="stat-number">""" + str(self.get_recent_updates_count(vault_path)) + """</div>
            <div class="stat-label">Recent Updates</div>
        </div>
    </div>
    
    <div class="search-box">
        <input type="text" class="search-input" placeholder="🔍 Search SOPs..." 
               onkeyup="filterSOPs(this.value)">
    </div>
    
    <div class="quick-actions">
        <h3>⚡ Quick Actions</h3>
        <div class="action-buttons">
            <a href="/vault/Creating%20New%20SOPs.md" class="action-btn">📝 How to Create SOPs</a>
            <a href="/vault/templates/SOP%20Template.md" class="action-btn">📄 SOP Template</a>
            <a href="javascript:window.print()" class="action-btn secondary">🖨️ Print Index</a>
        </div>
    </div>
    
    <div class="categories" id="categories">"""
        
        # Generate category sections
        for category, files in categories.items():
            info = category_info.get(category, {'icon': '📁', 'color': '#34495e', 'desc': 'Documentation files'})
            
            html += f"""
        <div class="category" data-category="{category}">
            <div class="category-header">
                <span class="category-icon">{info['icon']}</span>
                <h2 class="category-title" style="color: {info['color']}">{category}</h2>
            </div>
            <p class="category-desc">{info['desc']}</p>
            <ul class="file-list">"""
            
            for file_path in files:
                file_url = f'/vault/{file_path}'
                file_name = file_path.stem
                # Add file modification indicator
                full_path = vault_path / file_path
                mod_time = self.get_file_age(full_path)
                html += f'<li><a href="{file_url}" data-filename="{file_name.lower()}">{file_name} {mod_time}</a></li>'
            
            html += """
            </ul>
        </div>"""
        
        html += """
    </div>
    
    <script>
        function filterSOPs(searchTerm) {
            const categories = document.querySelectorAll('.category');
            const term = searchTerm.toLowerCase();
            
            categories.forEach(category => {
                const links = category.querySelectorAll('.file-list a');
                let hasVisibleItems = false;
                
                links.forEach(link => {
                    const filename = link.getAttribute('data-filename');
                    const text = link.textContent.toLowerCase();
                    
                    if (filename.includes(term) || text.includes(term)) {
                        link.parentElement.style.display = '';
                        hasVisibleItems = true;
                    } else {
                        link.parentElement.style.display = 'none';
                    }
                });
                
                // Hide category if no visible items
                category.style.display = hasVisibleItems || term === '' ? '' : 'none';
            });
        }
    </script>
</body>
</html>"""
        return html
    
    def get_last_modified_time(self, vault_path):
        """Get the last modification time of the most recently updated file"""
        import datetime
        latest_time = 0
        
        for root, dirs, filenames in os.walk(vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = Path(root) / filename
                    try:
                        mod_time = file_path.stat().st_mtime
                        if mod_time > latest_time:
                            latest_time = mod_time
                    except:
                        continue
        
        if latest_time > 0:
            return datetime.datetime.fromtimestamp(latest_time).strftime("%B %d, %Y")
        return "Unknown"
    
    def get_recent_updates_count(self, vault_path):
        """Count files updated in the last 7 days"""
        import datetime, time
        
        week_ago = time.time() - (7 * 24 * 60 * 60)  # 7 days in seconds
        count = 0
        
        for root, dirs, filenames in os.walk(vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = Path(root) / filename
                    try:
                        if file_path.stat().st_mtime > week_ago:
                            count += 1
                    except:
                        continue
        
        return count
    
    def get_file_age(self, file_path):
        """Get a human-readable file age indicator"""
        import datetime, time
        
        try:
            mod_time = file_path.stat().st_mtime
            now = time.time()
            age_days = (now - mod_time) / (24 * 60 * 60)
            
            if age_days < 1:
                return "🆕"
            elif age_days < 7:
                return "📅"
            elif age_days < 30:
                return ""
            else:
                return ""
        except:
            return ""
    
    def get_breadcrumb_path(self, file_path):
        """Generate breadcrumb path for a file"""
        parts = []
        if file_path.parent != Path('.'):
            parts.append(file_path.parent.name)
        parts.append(file_path.stem)
        return ' › '.join(parts)
    
    def get_file_modification_date(self, file_path):
        """Get formatted modification date for a file"""
        import datetime
        try:
            # file_path is already relative to vault, make it absolute
            vault_path = Path('vault')
            full_path = vault_path / file_path
            mod_time = full_path.stat().st_mtime
            return datetime.datetime.fromtimestamp(mod_time).strftime("%B %d, %Y at %I:%M %p")
        except:
            return "Unknown"
    
    def get_file_size(self, file_path):
        """Get human-readable file size"""
        try:
            vault_path = Path('vault')
            full_path = vault_path / file_path
            size_bytes = full_path.stat().st_size
            
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"
    
    def markdown_to_html(self, content, file_path):
        """Convert markdown to basic HTML"""
        # Basic markdown conversion
        lines = content.split('\n')
        html_lines = []
        in_code_block = False
        
        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    html_lines.append('</pre>')
                    in_code_block = False
                else:
                    html_lines.append('<pre><code>')
                    in_code_block = True
                continue
            
            if in_code_block:
                html_lines.append(line)
                continue
            
            # Headers
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('#### '):
                html_lines.append(f'<h4>{line[5:]}</h4>')
            elif line.startswith('- ') or line.startswith('* '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.strip() == '':
                html_lines.append('<br>')
            else:
                # Process links [[filename]] -> <a href="/vault/filename.md">filename</a>
                import re
                link_pattern = r'\[\[([^\]]+)\]\]'
                line = re.sub(link_pattern, r'<a href="/vault/\1.md">\1</a>', line)
                html_lines.append(f'<p>{line}</p>')
        
        if in_code_block:
            html_lines.append('</pre>')
        
        content_html = '\n'.join(html_lines)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_path.stem} - SOPs</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            margin: 0; padding: 20px; line-height: 1.6; background: #f8f9fa;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ 
            background: white; border-radius: 8px; padding: 20px; 
            margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .breadcrumb {{ 
            color: #666; margin-bottom: 15px; font-size: 0.9em;
        }}
        .breadcrumb a {{ color: #3498db; text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .document-meta {{
            background: #f8f9fa; border-left: 4px solid #3498db;
            padding: 15px; margin: 20px 0; border-radius: 0 5px 5px 0;
        }}
        .content {{ 
            background: white; border-radius: 8px; padding: 30px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .actions {{
            background: white; border-radius: 8px; padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;
        }}
        .action-btn {{
            display: inline-block; margin: 5px; padding: 8px 16px;
            background: #3498db; color: white; text-decoration: none;
            border-radius: 5px; font-weight: 500; transition: background 0.2s;
        }}
        .action-btn:hover {{ background: #2980b9; }}
        .action-btn.secondary {{ background: #95a5a6; }}
        .action-btn.secondary:hover {{ background: #7f8c8d; }}
        h1, h2, h3, h4 {{ color: #2c3e50; }}
        h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        a {{ color: #3498db; }}
        a:hover {{ color: #2980b9; }}
        pre {{ 
            background: #2d3748; color: #e2e8f0; padding: 15px; 
            border-radius: 5px; overflow-x: auto; 
        }}
        code {{ 
            background: #f1f5f9; color: #1e293b; padding: 2px 5px; 
            border-radius: 3px; font-family: 'Monaco', 'Consolas', monospace;
        }}
        li {{ margin: 5px 0; }}
        .checkbox {{ margin-right: 8px; }}
        blockquote {{
            border-left: 4px solid #3498db; margin: 0; padding-left: 20px;
            color: #666; font-style: italic;
        }}
        @media (max-width: 768px) {{
            .container {{ margin: 10px; }}
            .content {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="breadcrumb">
                <a href="/">🏠 Home</a> › 
                <a href="/vault">📚 SOPs Vault</a> › 
                <span>{self.get_breadcrumb_path(file_path)}</span>
            </div>
            <div class="document-meta">
                <strong>📄 Document:</strong> {file_path.stem}<br>
                <strong>📂 Category:</strong> {file_path.parent if file_path.parent != Path('.') else 'Root'}<br>
                <strong>🕒 Last Modified:</strong> {self.get_file_modification_date(file_path)}<br>
                <strong>📏 Size:</strong> {self.get_file_size(file_path)}
            </div>
        </div>
        
        <div class="content">
            {content_html}
        </div>
        
        <div class="actions">
            <a href="/vault" class="action-btn">← Back to Vault</a>
            <a href="javascript:window.print()" class="action-btn secondary">🖨️ Print</a>
            <a href="javascript:copyLink()" class="action-btn secondary">🔗 Copy Link</a>
        </div>
    </div>
    
    <script>
        function copyLink() {{
            navigator.clipboard.writeText(window.location.href).then(() => {{
                alert('Link copied to clipboard!');
            }});
        }}
        
        // Auto-scroll to fragment if present
        if (window.location.hash) {{
            setTimeout(() => {{
                document.querySelector(window.location.hash)?.scrollIntoView();
            }}, 100);
        }}
    </script>
</body>
</html>"""

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
