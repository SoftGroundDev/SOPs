# SOPs Knowledge Base

A Standard Operating Procedures knowledge base powered by Obsidian and served with a custom web interface.

## Features

- 📝 **Obsidian Vault**: Full-featured markdown-based knowledge management
- 🌐 **Web Interface**: Clean, responsive web UI for browsing procedures
- 🔍 **Search Functionality**: Quick search through all procedures
- 📋 **Templates**: Standardized SOP templates
- 🔗 **Linking**: Cross-referenced procedures with backlinks
- 📱 **Mobile Friendly**: Responsive design for all devices

## Quick Start

### Option 1: Using the Management Script (Recommended)
```bash
# Start the server
./sops.sh start

# Open in browser
./sops.sh open

# Check status
./sops.sh status

# Stop the server
./sops.sh stop
```

### Option 2: Using Python Directly
```bash
# Start the server
python3 serve.py
# or
npm run serve
```

### Option 3: Using Node.js
```bash
npm run start
```

The server will start on `http://localhost:8000` and the management script can automatically open it in your browser.

## Project Structure

```
SOPs/
├── vault/                 # Obsidian vault directory
│   ├── .obsidian/        # Obsidian configuration
│   ├── templates/        # SOP templates
│   ├── README.md         # Vault homepage
│   └── *.md             # Individual SOPs
├── web/                  # Web interface
│   └── index.html       # Main web interface
├── sops.sh              # Management script (start/stop/status)
├── serve.py             # Python HTTP server
├── package.json         # NPM configuration
└── README.md           # This file
```

## Using the Obsidian Vault

1. **Install Obsidian**: Download from [obsidian.md](https://obsidian.md)
2. **Open Vault**: Open the `vault/` folder as an Obsidian vault
3. **Start Creating**: Use templates from `vault/templates/` to create new SOPs

## Creating New SOPs

1. Open the Obsidian vault
2. Use the SOP template from `vault/templates/SOP Template.md`
3. Fill in all sections:
   - Purpose and scope
   - Prerequisites
   - Step-by-step instructions
   - Verification steps
   - Troubleshooting guide
4. Link to related procedures using `[[Page Name]]` syntax
5. Add relevant tags like `#sop #operations #emergency`

## Web Interface

The web interface provides:
- Overview of all procedure categories
- Quick navigation and search
- Direct links to vault content
- Mobile-friendly responsive design

## Development

### Adding New Categories
1. Update the navigation in `web/index.html`
2. Create corresponding folders in the vault
3. Add category templates if needed

### Customizing the Web Interface
Edit `web/index.html` to modify:
- Styling and layout
- Navigation structure
- Search functionality
- Grid layout and cards

## Best Practices

### Writing SOPs
- Use clear, action-oriented language
- Include prerequisites and verification steps
- Add troubleshooting sections
- Link to related procedures
- Use consistent formatting

### Organization
- Group related procedures in folders
- Use meaningful filenames
- Maintain a consistent tagging system
- Keep templates up to date
- Regular review and updates

## Server Options

### Python Server (serve.py)
- Lightweight and fast
- CORS enabled for development
- Markdown file serving
- Auto-opens browser

### Alternative Servers
```bash
# Simple HTTP server
python3 -m http.server 8080

# Node.js http-server
npx http-server -p 8080 -o

# PHP built-in server
php -S localhost:8080
```

## Contributing

1. Create new SOPs using the provided templates
2. Follow the established naming conventions
3. Link related procedures
4. Test procedures before committing
5. Update this README if needed

## License

MIT License - see LICENSE file for details.

---

**Getting Started:**
1. Run `python3 serve.py` or `npm run serve`
2. Open `http://localhost:8080` in your browser
3. Click "Open Obsidian Vault" to start editing
4. Use templates to create new SOPs
