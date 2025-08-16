# SOPs Knowledge Base

A clean, simple Standard Operating Procedures knowledge base using Obsidian vault served via Python.

## 🚀 Quick Start

```bash
# Start the server
./sops.sh start

# Or directly with Python
python3 serve.py
```

Visit http://localhost:8000 to browse your SOPs vault.

## 📋 Features

- **Pure Python** - No Node.js required, uses Python standard library
- **Obsidian Compatible** - Works with your existing Obsidian vault
- **Web Interface** - Browse and read SOPs in any web browser
- **Markdown Rendering** - Converts markdown to HTML with proper formatting
- **Internal Links** - Supports Obsidian-style `[[links]]` between documents
- **File Organization** - Maintains your folder structure (Operations, Emergency, etc.)

## 🛠️ Requirements

- Python 3.6+ (uses standard library only)

## 📁 Project Structure

```
SOPs/
├── vault/                    # Your Obsidian vault
│   ├── Operations/          # Operational procedures
│   ├── Emergency/           # Emergency protocols  
│   └── templates/           # SOP templates
├── serve.py                 # Python web server
├── sops.sh                  # Management script
└── README.md               # This file
```

## 🎯 Usage

### Start the Server
```bash
./sops.sh start              # Recommended
# OR
python3 serve.py             # Direct Python
```

### Stop the Server  
```bash
./sops.sh stop
```

### Open in Browser
```bash
./sops.sh open
```

## 🌐 Endpoints

- `/` - Vault index (lists all SOPs)
- `/vault/[file].md` - Individual SOP rendered as HTML  

## ✨ Why This Setup?

- **Simple**: Pure Python, no complex build processes
- **Fast**: Lightweight HTTP server starts instantly
- **Compatible**: Works with any Obsidian vault
- **Portable**: Self-contained, easy to deploy
- **Netlify Ready**: Static site generation for easy web deployment

## 🌐 Deploy to Netlify

This project is configured for easy deployment to Netlify as a static site:

```bash
# Build static site for deployment
python3 build_static.py

# Or use npm script
npm run build
```

The build generates a complete static site in the `dist/` directory that can be deployed to Netlify, GitHub Pages, or any static hosting service.

**Quick Netlify Setup:**
1. Push this repo to GitHub/GitLab
2. Connect to Netlify
3. Build command: `python3 build_static.py`
4. Publish directory: `dist`

See [NETLIFY.md](NETLIFY.md) for detailed deployment instructions.

## 🔧 Development

The server automatically converts markdown to HTML with:
- Headers, lists, and formatting
- Obsidian-style `[[internal links]]`
- Code blocks and syntax highlighting
- Clean, readable styling
