#!/usr/bin/env python3
"""
Static site generator for SOPs Knowledge Base
Converts the Obsidian vault to static HTML files for Netlify deployment
"""
import os
import sys
import shutil
from pathlib import Path
import markdown
from markdown.extensions import codehilite, toc, tables, fenced_code
import json
import re

class StaticSiteGenerator:
    def __init__(self, vault_dir="vault", output_dir="dist"):
        self.vault_dir = Path(vault_dir)
        self.output_dir = Path(output_dir)
        self.markdown_processor = markdown.Markdown(
            extensions=[
                'codehilite',
                'toc',
                'tables', 
                'fenced_code',
                'attr_list',
                'def_list',
                'footnotes'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )
        
    def clean_output_dir(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def get_html_template(self, title="SOPs Knowledge Base", content="", nav_links=None):
        """Generate HTML template with navigation"""
        nav_html = ""
        if nav_links:
            nav_items = []
            for link in nav_links:
                nav_items.append(f'<a href="{link["url"]}" class="nav-link">{link["title"]}</a>')
            nav_html = f'<nav class="main-nav">{"".join(nav_items)}</nav>'
            
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #fafafa;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            color: #7f8c8d;
            font-size: 1.1rem;
        }}
        
        .main-nav {{
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .nav-link {{
            display: inline-block;
            margin: 0 1rem;
            padding: 0.5rem 1rem;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        
        .nav-link:hover {{
            background-color: #2980b9;
        }}
        
        .content {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .vault-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .vault-section {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        
        .vault-section h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        
        .file-list li {{
            margin: 0.5rem 0;
        }}
        
        .file-list a {{
            color: #3498db;
            text-decoration: none;
            padding: 0.25rem 0;
            display: block;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        
        .file-list a:hover {{
            background-color: #ecf0f1;
            padding-left: 0.5rem;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        /* Markdown content styling */
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
            color: #2c3e50;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        .content h1 {{
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }}
        
        .content code {{
            background-color: #f1f2f6;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}
        
        .content pre {{
            background-color: #2f3542;
            color: #f1f2f6;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        .content pre code {{
            background: none;
            padding: 0;
        }}
        
        .content blockquote {{
            border-left: 4px solid #3498db;
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background-color: #f8f9fa;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        .content th, .content td {{
            border: 1px solid #ddd;
            padding: 0.75rem;
            text-align: left;
        }}
        
        .content th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        
        /* Obsidian-style internal links */
        .internal-link {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .internal-link:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .vault-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav-link {{
                display: block;
                margin: 0.5rem 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SOPs Knowledge Base</h1>
        <p>Standard Operating Procedures & Documentation</p>
    </div>
    
    {nav_html}
    
    <div class="content">
        {content}
    </div>
</body>
</html>"""
    
    def process_markdown_links(self, content):
        """Convert Obsidian-style [[links]] to HTML links"""
        def replace_link(match):
            link_text = match.group(1)
            # Convert to URL-friendly format
            url_path = link_text.replace(' ', '-').lower()
            return f'<a href="/vault/{url_path}.html" class="internal-link">{link_text}</a>'
        
        # Replace [[Link Text]] with proper HTML links
        content = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
        return content
    
    def generate_vault_index(self):
        """Generate the main vault index page"""
        vault_structure = {}
        
        # Scan vault directory for markdown files
        for md_file in self.vault_dir.rglob("*.md"):
            relative_path = md_file.relative_to(self.vault_dir)
            folder = relative_path.parent.name if relative_path.parent.name != "." else "Root"
            
            if folder not in vault_structure:
                vault_structure[folder] = []
                
            # Convert filename to URL-friendly format
            filename_base = md_file.stem
            url_path = filename_base.replace(' ', '-').lower()
            
            vault_structure[folder].append({
                "title": filename_base.replace('-', ' ').title(),
                "url": f"/vault/{url_path}.html",
                "file_path": str(relative_path)
            })
        
        # Generate HTML content
        content = "<h1>📚 Knowledge Base Index</h1>"
        content += "<p>Browse the complete collection of Standard Operating Procedures and documentation.</p>"
        
        if vault_structure:
            content += '<div class="vault-grid">'
            for folder, files in vault_structure.items():
                if folder == "Root":
                    continue  # Skip root files for now
                    
                content += f'<div class="vault-section">'
                content += f'<h3>📁 {folder}</h3>'
                content += '<ul class="file-list">'
                
                for file_info in files:
                    content += f'<li><a href="{file_info["url"]}">{file_info["title"]}</a></li>'
                
                content += '</ul></div>'
            
            # Add root files if any
            if "Root" in vault_structure:
                content += f'<div class="vault-section">'
                content += f'<h3>📄 Documents</h3>'
                content += '<ul class="file-list">'
                for file_info in vault_structure["Root"]:
                    content += f'<li><a href="{file_info["url"]}">{file_info["title"]}</a></li>'
                content += '</ul></div>'
            
            content += '</div>'
        else:
            content += "<p>No documents found in the vault.</p>"
        
        # Generate the index HTML file
        html_content = self.get_html_template(
            title="SOPs Knowledge Base - Index",
            content=content
        )
        
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Generated index: {index_file}")
    
    def generate_markdown_pages(self):
        """Convert all markdown files to HTML"""
        vault_output_dir = self.output_dir / "vault"
        vault_output_dir.mkdir(exist_ok=True)
        
        for md_file in self.vault_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Process Obsidian-style links
                content = self.process_markdown_links(content)
                
                # Convert markdown to HTML
                html_content = self.markdown_processor.convert(content)
                
                # Get title from first header or filename
                title = md_file.stem.replace('-', ' ').title()
                first_line = content.split('\n')[0] if content else ""
                if first_line.startswith('#'):
                    title = first_line.lstrip('#').strip()
                
                # Add back link
                back_link = '<a href="/" class="back-link">← Back to Index</a>'
                full_content = back_link + html_content
                
                # Generate complete HTML page
                html_page = self.get_html_template(
                    title=f"{title} - SOPs Knowledge Base",
                    content=full_content,
                    nav_links=[
                        {"title": "🏠 Home", "url": "/"},
                        {"title": "📚 Browse All", "url": "/"}
                    ]
                )
                
                # Convert filename to URL-friendly format
                filename_base = md_file.stem.replace(' ', '-').lower()
                output_file = vault_output_dir / f"{filename_base}.html"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_page)
                
                print(f"✅ Generated: {md_file.name} -> {output_file.name}")
                
            except Exception as e:
                print(f"❌ Error processing {md_file}: {str(e)}")
    
    def copy_assets(self):
        """Copy images and other assets"""
        # Copy images directory if it exists
        images_src = Path("images")
        if images_src.exists():
            images_dest = self.output_dir / "images"
            shutil.copytree(images_src, images_dest, dirs_exist_ok=True)
            print(f"✅ Copied assets: {images_src} -> {images_dest}")
        
        # Copy vault images if they exist
        vault_images = self.vault_dir / "images"
        if vault_images.exists():
            vault_images_dest = self.output_dir / "vault" / "images"
            shutil.copytree(vault_images, vault_images_dest, dirs_exist_ok=True)
            print(f"✅ Copied vault assets: {vault_images} -> {vault_images_dest}")
    
    def generate_site(self):
        """Generate the complete static site"""
        print("🚀 Generating static site for Netlify...")
        
        # Clean and prepare output directory
        self.clean_output_dir()
        
        # Generate pages
        self.generate_vault_index()
        self.generate_markdown_pages()
        
        # Copy assets
        self.copy_assets()
        
        print(f"✅ Static site generated successfully in '{self.output_dir}' directory!")
        print("🌐 Ready for Netlify deployment!")

if __name__ == "__main__":
    generator = StaticSiteGenerator()
    generator.generate_site()
