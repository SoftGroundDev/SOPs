#!/usr/bin/env python3
"""
Simple HTTP server to serve the SOPs Knowledge Base with proper markdown rendering
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from pathlib import Path
from urllib.parse import unquote
import datetime
import markdown
from markdown.extensions import codehilite, toc, tables, fenced_code
import mimetypes

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
        elif self.path.startswith('/images/'):
            # Serve image files from images directory
            self.serve_image()
            return
        elif self.path.startswith('/vault/') and self.is_image_file(self.path):
            # Serve images from within vault folders
            self.serve_vault_image()
            return
        
        return super().do_GET()
    
    def is_image_file(self, path):
        """Check if the file is an image based on its extension"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.tiff', '.ico'}
        return Path(path).suffix.lower() in image_extensions
    
    def serve_image(self):
        """Serve image files from the images directory"""
        # URL decode the path and remove the /images/ prefix
        decoded_path = unquote(self.path)
        
        if decoded_path.startswith('/images/'):
            # Remove /images/ prefix to get the relative path within the images directory
            relative_path = decoded_path[8:]  # Remove '/images/'
            file_path = Path('images') / relative_path
        else:
            self.send_error(404, f"Invalid image path: {decoded_path}")
            return
        
        if file_path.exists() and self.is_image_file(str(file_path)):
            try:
                # Guess the content type
                content_type, _ = mimetypes.guess_type(str(file_path))
                if not content_type:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Cache-Control', 'public, max-age=86400')  # Cache for 1 day
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, f"Error serving image: {e}")
        else:
            self.send_error(404, f"Image not found: {file_path}")
    
    def serve_vault_image(self):
        """Serve image files from within vault folders"""
        # URL decode the path and remove the /vault/ prefix
        decoded_path = unquote(self.path)
        
        if decoded_path.startswith('/vault/'):
            # Remove /vault/ prefix to get the relative path within the vault
            relative_path = decoded_path[7:]  # Remove '/vault/'
            file_path = Path('vault') / relative_path
        else:
            self.send_error(404, f"Invalid vault image path: {decoded_path}")
            return
        
        if file_path.exists() and self.is_image_file(str(file_path)):
            try:
                # Guess the content type
                content_type, _ = mimetypes.guess_type(str(file_path))
                if not content_type:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Cache-Control', 'public, max-age=86400')  # Cache for 1 day
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, f"Error serving vault image: {e}")
        else:
            self.send_error(404, f"Vault image not found: {file_path}")
    
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

    def get_vault_navigation(self):
        """Generate navigation HTML for the sidebar"""
        vault_path = Path('vault')
        categories = {}
        
        for root, dirs, filenames in os.walk(vault_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = Path(root) / filename
                    rel_path = file_path.relative_to(vault_path)
                    folder = str(rel_path.parent) if rel_path.parent != Path('.') else 'Root'
                    
                    if folder not in categories:
                        categories[folder] = []
                    categories[folder].append(rel_path)
        
        # Sort categories and files within each category
        for category in categories:
            categories[category].sort()
        
        # Get category icons
        category_info = {
            'Operations': {'icon': '⚙️'},
            'Emergency': {'icon': '🚨'},
            'templates': {'icon': '📝'},
            'Root': {'icon': '📋'}
        }
        
        nav_html = ''
        for category_name, files in categories.items():
            info = category_info.get(category_name, {'icon': '📁'})
            nav_html += f'''
            <div class="nav-category">
                <div class="nav-category-header" onclick="toggleCategory('{category_name}')">
                    <span class="nav-icon">{info['icon']}</span>
                    <span class="nav-title">{category_name}</span>
                    <span class="nav-toggle">▼</span>
                </div>
                <ul class="nav-files" id="nav-{category_name}">'''
            
            for file_path in files:
                file_url = f"/vault/{file_path}"
                file_name = file_path.stem
                
                # Determine file icon
                if 'emergency' in file_name.lower() or 'incident' in file_name.lower():
                    file_icon = '🚨'
                elif 'template' in file_name.lower():
                    file_icon = '📝'
                elif 'backup' in file_name.lower() or 'database' in file_name.lower():
                    file_icon = '💾'
                elif 'health' in file_name.lower() or 'check' in file_name.lower():
                    file_icon = '🏥'
                else:
                    file_icon = '📄'
                
                nav_html += f'''
                    <li>
                        <a href="{file_url}" class="nav-file-link">
                            <span class="nav-file-icon">{file_icon}</span>
                            <span class="nav-file-name">{file_name}</span>
                        </a>
                    </li>'''
            
            nav_html += '</ul></div>'
        
        return nav_html

    def markdown_to_html(self, content, file_path):
        """Convert markdown to richly formatted HTML using the markdown library"""
        # Configure markdown with useful extensions
        md = markdown.Markdown(extensions=[
            'extra',          # Includes tables, fenced_code, footnotes, attr_list, def_list, abbr
            'codehilite',     # Syntax highlighting
            'toc',           # Table of contents
            'nl2br',         # New line to break
            'smarty'         # Smart quotes and dashes
        ], extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': True,  # Inline styles instead of CSS classes
            },
            'toc': {
                'permalink': True,
                'permalink_title': 'Permanent link',
            }
        })
        
        # Convert markdown to HTML
        html_content = md.convert(content)
        
        # Generate breadcrumbs
        parts = file_path.parts
        breadcrumb_items = []
        breadcrumb_items.append('<a href="/">🏠 Home</a>')
        breadcrumb_items.append('<a href="/vault/">📁 Vault</a>')
        
        if len(parts) > 1:
            # Add intermediate folders
            current_path = []
            for part in parts[:-1]:  # Exclude the filename
                current_path.append(part)
                folder_url = '/vault/' + '/'.join(current_path) + '/'
                breadcrumb_items.append(f'<a href="{folder_url}">📂 {part}</a>')
        
        # Add current file (no link)
        breadcrumb_items.append(f'<span>📄 {file_path.stem}</span>')
        breadcrumb = ' → '.join(breadcrumb_items)
        
        # Get file metadata
        try:
            file_stat = Path('vault') / file_path
            modified_time = file_stat.stat().st_mtime
            modified_date = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M')
            file_size = self.format_file_size(file_stat.stat().st_size)
        except:
            modified_date = "Unknown"
            file_size = "Unknown"

        # Get navigation HTML
        nav_html = self.get_vault_navigation()

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_path.stem} - SOPs</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif; 
            margin: 0; padding: 0; line-height: 1.7; 
            background: #f8fafc; color: #334155;
            display: flex; height: 100vh;
        }}
        
        /* Sidebar Navigation Styles */
        .sidebar {{
            width: 280px; background: #1e293b; color: white;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            overflow-y: auto; flex-shrink: 0;
            border-right: 1px solid #334155;
        }}
        
        .sidebar-header {{
            padding: 20px; background: #0f172a; border-bottom: 1px solid #334155;
            text-align: center;
        }}
        
        .sidebar-title {{
            font-size: 1.2rem; font-weight: 700; margin: 0;
            color: #e2e8f0;
        }}
        
        .sidebar-subtitle {{
            font-size: 0.8rem; color: #94a3b8; margin: 5px 0 0;
        }}
        
        .nav-category {{
            margin: 8px 0; border-bottom: 1px solid #334155;
        }}
        
        .nav-category-header {{
            padding: 12px 20px; cursor: pointer; display: flex;
            align-items: center; background: #1e293b;
            transition: background-color 0.2s;
        }}
        
        .nav-category-header:hover {{
            background: #334155;
        }}
        
        .nav-icon {{
            margin-right: 8px; font-size: 1.1rem;
        }}
        
        .nav-title {{
            flex: 1; font-weight: 600; font-size: 0.9rem;
        }}
        
        .nav-toggle {{
            font-size: 0.8rem; transition: transform 0.2s;
        }}
        
        .nav-toggle.expanded {{
            transform: rotate(180deg);
        }}
        
        .nav-files {{
            list-style: none; padding: 0; margin: 0;
            max-height: 0; overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .nav-files.expanded {{
            max-height: 500px;
        }}
        
        .nav-files li {{
            border-bottom: 1px solid #2d3748;
        }}
        
        .nav-file-link {{
            display: flex; align-items: center; padding: 10px 20px 10px 40px;
            color: #cbd5e1; text-decoration: none; font-size: 0.85rem;
            transition: all 0.2s;
        }}
        
        .nav-file-link:hover {{
            background: #334155; color: #f1f5f9;
            padding-left: 45px;
        }}
        
        .nav-file-link.active {{
            background: #3b82f6; color: white;
            font-weight: 600;
        }}
        
        .nav-file-icon {{
            margin-right: 8px; font-size: 1rem;
        }}
        
        .nav-file-name {{
            flex: 1; white-space: nowrap; overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* Main Content Area */
        .main-content {{
            flex: 1; display: flex; flex-direction: column;
            overflow: hidden;
        }}
        
        .content-wrapper {{
            flex: 1; overflow-y: auto; padding: 20px;
        }}
        
        .container {{ 
            max-width: 900px; margin: 0 auto;
        }}
        
        .header {{ 
            background: white; border-radius: 12px; padding: 24px; 
            margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
        }}
        
        /* Mobile Toggle Button */
        .sidebar-toggle {{
            display: none; position: fixed; top: 15px; left: 15px;
            z-index: 1000; background: #1e293b; color: white;
            border: none; padding: 10px; border-radius: 6px;
            cursor: pointer; font-size: 1.2rem;
        }}
        
        .breadcrumb {{ 
            color: #64748b; margin-bottom: 16px; font-size: 0.875rem;
            font-weight: 500;
        }}
        .breadcrumb a {{ 
            color: #3b82f6; text-decoration: none; transition: color 0.2s;
        }}
        .breadcrumb a:hover {{ 
            color: #1d4ed8; text-decoration: underline;
        }}
        
        .document-meta {{
            background: #f1f5f9; border-left: 4px solid #3b82f6;
            padding: 16px; margin: 16px 0; border-radius: 0 8px 8px 0;
            font-size: 0.875rem; line-height: 1.6;
        }}
        
        .content {{ 
            background: white; border-radius: 12px; padding: 32px; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0; margin-bottom: 24px;
        }}
        
        .actions {{
            background: white; border-radius: 12px; padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0; text-align: center;
        }}
        
        .action-btn {{
            display: inline-block; margin: 6px; padding: 10px 20px;
            background: #3b82f6; color: white; text-decoration: none;
            border-radius: 8px; font-weight: 500; font-size: 0.875rem;
            transition: all 0.2s; border: none;
        }}
        .action-btn:hover {{ 
            background: #2563eb; transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
        }}
        .action-btn.secondary {{ 
            background: #6b7280; 
        }}
        .action-btn.secondary:hover {{ 
            background: #4b5563;
            box-shadow: 0 4px 8px rgba(107, 114, 128, 0.3);
        }}
        
        /* Markdown Content Styling */
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{ 
            color: #1e293b; margin-top: 32px; margin-bottom: 16px;
            font-weight: 700; line-height: 1.25;
        }}
        
        .content h1 {{ 
            font-size: 2.25rem; border-bottom: 3px solid #3b82f6; 
            padding-bottom: 12px; margin-top: 0;
        }}
        .content h2 {{ 
            font-size: 1.875rem; border-bottom: 2px solid #e2e8f0; 
            padding-bottom: 8px;
        }}
        .content h3 {{ font-size: 1.5rem; }}
        .content h4 {{ font-size: 1.25rem; }}
        .content h5 {{ font-size: 1.125rem; }}
        .content h6 {{ font-size: 1rem; }}
        
        .content p {{ margin: 16px 0; }}
        
        .content a {{ 
            color: #3b82f6; text-decoration: underline;
            text-decoration-color: #93c5fd; transition: all 0.2s;
        }}
        .content a:hover {{ 
            color: #1d4ed8; text-decoration-color: #3b82f6;
        }}
        
        .content pre {{
            background: #1e293b; color: #e2e8f0; padding: 20px;
            border-radius: 8px; overflow-x: auto; margin: 20px 0;
            font-family: 'Fira Code', 'Monaco', 'Consolas', 'Ubuntu Mono', monospace;
            font-size: 0.875rem; line-height: 1.5;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .content code {{
            background: #f1f5f9; color: #1e293b; padding: 3px 6px;
            border-radius: 4px; font-size: 0.875rem;
            font-family: 'Fira Code', 'Monaco', 'Consolas', 'Ubuntu Mono', monospace;
        }}
        
        .content pre code {{
            background: transparent; color: inherit; padding: 0;
            border-radius: 0;
        }}
        
        .content blockquote {{
            border-left: 4px solid #3b82f6; margin: 20px 0; padding: 16px 20px;
            background: #f8fafc; color: #64748b; font-style: italic;
            border-radius: 0 8px 8px 0;
        }}
        
        .content ul, .content ol {{
            margin: 16px 0; padding-left: 24px;
        }}
        .content li {{
            margin: 8px 0; line-height: 1.6;
        }}
        
        .content table {{
            width: 100%; border-collapse: collapse; margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); border-radius: 8px;
            overflow: hidden;
        }}
        .content th {{
            background: #f1f5f9; color: #374151; font-weight: 600;
            padding: 12px 16px; text-align: left; border-bottom: 2px solid #e5e7eb;
        }}
        .content td {{
            padding: 12px 16px; border-bottom: 1px solid #e5e7eb;
        }}
        .content tr:hover {{
            background: #f9fafb;
        }}
        
        .content hr {{
            border: none; height: 2px; background: linear-gradient(90deg, #3b82f6, #06b6d4);
            margin: 32px 0; border-radius: 1px;
        }}
        
        .content img {{
            max-width: 100%; height: auto; border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        /* Task lists */
        .content input[type="checkbox"] {{
            margin-right: 8px; transform: scale(1.2);
        }}
        
        /* Table of contents */
        .toc {{
            background: #f8fafc; border: 1px solid #e2e8f0;
            border-radius: 8px; padding: 20px; margin: 20px 0;
        }}
        .toc ul {{
            margin: 8px 0; list-style: none; padding-left: 0;
        }}
        .toc li {{
            margin: 4px 0;
        }}
        .toc a {{
            text-decoration: none; color: #64748b;
        }}
        .toc a:hover {{
            color: #3b82f6;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .sidebar {{
                position: fixed; top: 0; left: -280px; height: 100vh;
                z-index: 999; transition: left 0.3s ease;
            }}
            .sidebar.mobile-open {{
                left: 0;
            }}
            .sidebar-toggle {{
                display: block !important;
            }}
            .main-content {{
                margin-left: 0;
            }}
            .container {{ 
                margin: 0; padding: 12px; 
            }}
            .content {{ 
                padding: 20px; margin-bottom: 16px;
            }}
            .header {{
                padding: 16px; margin-bottom: 16px;
            }}
            .content h1 {{ font-size: 1.75rem; }}
            .content h2 {{ font-size: 1.5rem; }}
            .content pre {{
                padding: 16px; font-size: 0.8rem;
            }}
            .action-btn {{
                display: block; margin: 8px 0;
            }}
        }}
        
        /* Overlay for mobile sidebar */
        .sidebar-overlay {{
            display: none; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5);
            z-index: 998;
        }}
        .sidebar-overlay.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <button class="sidebar-toggle" onclick="toggleMobileSidebar()">☰</button>
    <div class="sidebar-overlay" onclick="closeMobileSidebar()"></div>
    
    <div class="sidebar">
        <div class="sidebar-header">
            <h1 class="sidebar-title">📚 SOPs</h1>
            <p class="sidebar-subtitle">Knowledge Base</p>
        </div>
        <nav class="sidebar-nav">
            {nav_html}
        </nav>
    </div>
    
    <div class="main-content">
        <div class="content-wrapper">
            <div class="container">
                <div class="header">
                    <div class="breadcrumb">
                        {breadcrumb}
                    </div>
                    <div class="document-meta">
                        <strong>📄 Document:</strong> {file_path.stem}<br>
                        <strong>📂 Category:</strong> {file_path.parent if file_path.parent != Path('.') else 'Root'}<br>
                        <strong>🕒 Last Modified:</strong> {modified_date}<br>
                        <strong>📏 Size:</strong> {file_size}
                    </div>
                </div>
                
                <div class="content">
                    {html_content}
                </div>
                
                <div class="actions">
                    <a href="/vault" class="action-btn">← Back to Vault</a>
                    <a href="javascript:window.print()" class="action-btn secondary">🖨️ Print</a>
                    <a href="javascript:copyLink()" class="action-btn secondary">🔗 Copy Link</a>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function toggleCategory(categoryName) {{
            const toggle = document.querySelector(`#nav-${{categoryName}}`).previousElementSibling.querySelector('.nav-toggle');
            const files = document.querySelector(`#nav-${{categoryName}}`);
            
            if (files.classList.contains('expanded')) {{
                files.classList.remove('expanded');
                toggle.classList.remove('expanded');
            }} else {{
                files.classList.add('expanded');
                toggle.classList.add('expanded');
            }}
        }}
        
        function toggleMobileSidebar() {{
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.toggle('mobile-open');
            overlay.classList.toggle('active');
        }}
        
        function closeMobileSidebar() {{
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.remove('mobile-open');
            overlay.classList.remove('active');
        }}
        
        function copyLink() {{
            navigator.clipboard.writeText(window.location.href).then(() => {{
                alert('Link copied to clipboard!');
            }});
        }}
        
        // Highlight current file in navigation
        document.addEventListener('DOMContentLoaded', function() {{
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.nav-file-link');
            
            navLinks.forEach(link => {{
                if (link.getAttribute('href') === currentPath) {{
                    link.classList.add('active');
                    // Expand the parent category
                    const category = link.closest('.nav-files');
                    const toggle = category.previousElementSibling.querySelector('.nav-toggle');
                    category.classList.add('expanded');
                    toggle.classList.add('expanded');
                }}
            }});
        }});
        
        // Auto-scroll to fragment if present
        if (window.location.hash) {{
            setTimeout(() => {{
                const element = document.querySelector(window.location.hash);
                if (element) {{
                    element.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }}, 100);
        }}
        
        // Add smooth scrolling to all internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
    </script>
</body>
</html>"""

    def generate_vault_html(self, vault_path):
        """Generate HTML for the vault index with enhanced navigation and sidebar"""
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
                    folder = str(rel_path.parent) if rel_path.parent != Path('.') else 'Root'
                    
                    if folder not in categories:
                        categories[folder] = []
                    categories[folder].append(rel_path)
                    file_count += 1
        
        # Sort categories and files within each category
        for category in categories:
            categories[category].sort()
        
        # Get navigation HTML
        nav_html = self.get_vault_navigation()
        
        # Get category icons and descriptions
        category_info = {
            'Operations': {'icon': '⚙️', 'color': '#3498db', 'desc': 'Daily operational procedures'},
            'Emergency': {'icon': '🚨', 'color': '#e74c3c', 'desc': 'Critical incident response'},
            'templates': {'icon': '📝', 'color': '#9b59b6', 'desc': 'Templates for creating new SOPs'},
            'Root': {'icon': '📋', 'color': '#2c3e50', 'desc': 'General documentation'}
        }
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOPs Knowledge Base</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif; 
            margin: 0; padding: 0; line-height: 1.6; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex;
        }}
        
        /* Sidebar Navigation Styles */
        .sidebar {{
            width: 280px; background: #1e293b; color: white;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            overflow-y: auto; flex-shrink: 0;
            border-right: 1px solid #334155;
        }}
        
        .sidebar-header {{
            padding: 20px; background: #0f172a; border-bottom: 1px solid #334155;
            text-align: center;
        }}
        
        .sidebar-title {{
            font-size: 1.2rem; font-weight: 700; margin: 0;
            color: #e2e8f0;
        }}
        
        .sidebar-subtitle {{
            font-size: 0.8rem; color: #94a3b8; margin: 5px 0 0;
        }}
        
        .nav-category {{
            margin: 8px 0; border-bottom: 1px solid #334155;
        }}
        
        .nav-category-header {{
            padding: 12px 20px; cursor: pointer; display: flex;
            align-items: center; background: #1e293b;
            transition: background-color 0.2s;
        }}
        
        .nav-category-header:hover {{
            background: #334155;
        }}
        
        .nav-icon {{
            margin-right: 8px; font-size: 1.1rem;
        }}
        
        .nav-title {{
            flex: 1; font-weight: 600; font-size: 0.9rem;
        }}
        
        .nav-toggle {{
            font-size: 0.8rem; transition: transform 0.2s;
        }}
        
        .nav-toggle.expanded {{
            transform: rotate(180deg);
        }}
        
        .nav-files {{
            list-style: none; padding: 0; margin: 0;
            max-height: 0; overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .nav-files.expanded {{
            max-height: 500px;
        }}
        
        .nav-files li {{
            border-bottom: 1px solid #2d3748;
        }}
        
        .nav-file-link {{
            display: flex; align-items: center; padding: 10px 20px 10px 40px;
            color: #cbd5e1; text-decoration: none; font-size: 0.85rem;
            transition: all 0.2s;
        }}
        
        .nav-file-link:hover {{
            background: #334155; color: #f1f5f9;
            padding-left: 45px;
        }}
        
        .nav-file-icon {{
            margin-right: 8px; font-size: 1rem;
        }}
        
        .nav-file-name {{
            flex: 1; white-space: nowrap; overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* Main Content Area */
        .main-content {{
            flex: 1; overflow-y: auto;
        }}
        
        .container {{
            max-width: 1200px; margin: 0 auto; padding: 20px;
        }}
        
        /* Mobile Toggle Button */
        .sidebar-toggle {{
            display: none; position: fixed; top: 15px; left: 15px;
            z-index: 1000; background: #1e293b; color: white;
            border: none; padding: 10px; border-radius: 6px;
            cursor: pointer; font-size: 1.2rem;
        }}
        
        .header {{ 
            color: white; padding: 40px 20px; margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{ 
            margin: 0; font-size: 3rem; font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{ 
            margin: 15px 0 0; opacity: 0.9; font-size: 1.2rem;
        }}
        .stats {{ 
            background: white; border-radius: 12px; padding: 24px; 
            margin: 0 auto 30px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            display: flex; gap: 40px; align-items: center; justify-content: center;
            max-width: 600px;
        }}
        .stat {{ text-align: center; }}
        .stat-number {{ 
            font-size: 2.5rem; font-weight: bold; 
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .stat-label {{ color: #666; font-size: 0.9rem; font-weight: 500; }}
        
        .categories {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 24px; 
        }}
        .category {{ 
            background: white; border-radius: 16px; padding: 28px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.15); 
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .category:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 16px 40px rgba(0,0,0,0.2);
        }}
        .category-header {{ 
            display: flex; align-items: center; margin-bottom: 16px; 
        }}
        .category-icon {{ 
            font-size: 1.8rem; margin-right: 12px; 
        }}
        .category-title {{ 
            font-size: 1.4rem; font-weight: bold; margin: 0; 
            color: #2c3e50;
        }}
        .category-desc {{ 
            color: #7f8c8d; font-size: 0.95rem; margin-bottom: 20px; 
            line-height: 1.5;
        }}
        .file-list {{ 
            list-style: none; padding: 0; margin: 0; 
        }}
        .file-list li {{ 
            margin: 10px 0; 
        }}
        .file-list a {{ 
            text-decoration: none; color: #3498db; font-weight: 500;
            display: flex; align-items: center; padding: 8px 12px;
            border-radius: 8px; transition: all 0.2s;
        }}
        .file-list a:hover {{ 
            background: #f8f9fa; color: #2980b9;
            transform: translateX(4px);
        }}
        .file-icon {{
            margin-right: 8px; font-size: 1.1rem;
        }}
        .file-count {{
            background: #ecf0f1; color: #7f8c8d; padding: 4px 8px;
            border-radius: 12px; font-size: 0.8rem; margin-left: auto;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center; color: white; margin-top: 40px;
            opacity: 0.8; font-size: 0.9rem;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .sidebar {{
                position: fixed; top: 0; left: -280px; height: 100vh;
                z-index: 999; transition: left 0.3s ease;
            }}
            .sidebar.mobile-open {{
                left: 0;
            }}
            .sidebar-toggle {{
                display: block !important;
            }}
            body {{ padding: 10px; }}
            .header h1 {{ font-size: 2rem; }}
            .header p {{ font-size: 1rem; }}
            .stats {{ 
                flex-direction: column; gap: 20px; padding: 20px;
            }}
            .categories {{
                grid-template-columns: 1fr;
            }}
            .category {{ padding: 20px; }}
        }}
        
        /* Overlay for mobile sidebar */
        .sidebar-overlay {{
            display: none; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5);
            z-index: 998;
        }}
        .sidebar-overlay.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <button class="sidebar-toggle" onclick="toggleMobileSidebar()">☰</button>
    <div class="sidebar-overlay" onclick="closeMobileSidebar()"></div>
    
    <div class="sidebar">
        <div class="sidebar-header">
            <h1 class="sidebar-title">📚 SOPs</h1>
            <p class="sidebar-subtitle">Knowledge Base</p>
        </div>
        <nav class="sidebar-nav">
            {nav_html}
        </nav>
    </div>
    
    <div class="main-content">
        <div class="container">
            <div class="header">
                <h1>📚 SOPs Knowledge Base</h1>
                <p>Standard Operating Procedures & Documentation</p>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{file_count}</div>
                    <div class="stat-label">Documents</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(categories)}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
            
            <div class="categories">"""

        # Generate category sections
        for category_name, files in categories.items():
            info = category_info.get(category_name, {'icon': '📁', 'color': '#95a5a6', 'desc': 'Documentation files'})
            
            html += f'''
            <div class="category">
                <div class="category-header">
                    <span class="category-icon">{info['icon']}</span>
                    <h2 class="category-title">{category_name}</h2>
                    <span class="file-count">{len(files)}</span>
                </div>
                <p class="category-desc">{info['desc']}</p>
                <ul class="file-list">'''
            
            for file_path in files:
                file_url = f"/vault/{file_path}"
                file_name = file_path.stem
                
                # Determine file icon based on name or category
                if 'emergency' in file_name.lower() or 'incident' in file_name.lower():
                    file_icon = '🚨'
                elif 'template' in file_name.lower():
                    file_icon = '📝'
                elif 'backup' in file_name.lower() or 'database' in file_name.lower():
                    file_icon = '💾'
                elif 'health' in file_name.lower() or 'check' in file_name.lower():
                    file_icon = '🏥'
                else:
                    file_icon = '📄'
                
                html += f'''
                    <li>
                        <a href="{file_url}">
                            <span class="file-icon">{file_icon}</span>
                            {file_name}
                        </a>
                    </li>'''
            
            html += '''
                </ul>
            </div>'''
        
        html += '''
            </div>
            
            <div class="footer">
                <p>🔧 Powered by Python HTTP Server | 📝 Markdown Support Enabled</p>
            </div>
        </div>
    </div>
    
    <script>
        function toggleCategory(categoryName) {
            const toggle = document.querySelector(`#nav-${categoryName}`).previousElementSibling.querySelector('.nav-toggle');
            const files = document.querySelector(`#nav-${categoryName}`);
            
            if (files.classList.contains('expanded')) {
                files.classList.remove('expanded');
                toggle.classList.remove('expanded');
            } else {
                files.classList.add('expanded');
                toggle.classList.add('expanded');
            }
        }
        
        function toggleMobileSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.toggle('mobile-open');
            overlay.classList.toggle('active');
        }
        
        function closeMobileSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.remove('mobile-open');
            overlay.classList.remove('active');
        }
        
        // Expand all categories by default on the index page
        document.addEventListener('DOMContentLoaded', function() {
            const allFiles = document.querySelectorAll('.nav-files');
            const allToggles = document.querySelectorAll('.nav-toggle');
            
            allFiles.forEach(files => files.classList.add('expanded'));
            allToggles.forEach(toggle => toggle.classList.add('expanded'));
        });
    </script>
</body>
</html>'''
        
        return html

    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        try:
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"

def main():
    port = 8000
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
