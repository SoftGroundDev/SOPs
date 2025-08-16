# Netlify Deployment Guide

## 🌐 Deploy to Netlify

This SOPs Knowledge Base is now configured for easy deployment to Netlify as a static site.

### Prerequisites

- A [Netlify account](https://netlify.com) (free tier works fine)
- Your repository pushed to GitHub, GitLab, or Bitbucket

### Deployment Methods

#### Method 1: Git-based Deployment (Recommended)

1. **Connect Repository**: 
   - Log into Netlify Dashboard
   - Click "Add new site" → "Import an existing project"
   - Choose your Git provider and select this repository

2. **Configure Build Settings**:
   ```
   Build command: python3 build_static.py
   Publish directory: dist
   ```

3. **Environment Variables** (if needed):
   ```
   PYTHON_VERSION = 3.8
   ```

4. **Deploy**: 
   - Click "Deploy site"
   - Netlify will automatically build and deploy your site
   - You'll get a URL like `https://amazing-name-123456.netlify.app`

#### Method 2: Manual Deployment

1. **Build Locally**:
   ```bash
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Generate static site
   python3 build_static.py
   ```

2. **Deploy to Netlify**:
   - In Netlify Dashboard, drag and drop the `dist/` folder
   - Or use Netlify CLI: `netlify deploy --dir=dist --prod`

### Build Process

The build script (`build_static.py`) does the following:

1. **Scans Vault**: Reads all `.md` files in the `vault/` directory
2. **Converts Markdown**: Transforms markdown to HTML with:
   - Syntax highlighting
   - Table of contents
   - Obsidian-style `[[links]]` conversion
   - Clean, responsive styling
3. **Generates Navigation**: Creates an index page with organized file listings
4. **Copies Assets**: Includes images and other static files
5. **Outputs Static Site**: Creates a complete HTML site in `dist/`

### Features After Deployment

✅ **Fast Loading**: Static HTML files load instantly  
✅ **Mobile Responsive**: Works on all devices  
✅ **Search Friendly**: SEO optimized  
✅ **Internal Links**: Obsidian-style `[[links]]` work perfectly  
✅ **Organized Navigation**: Folder-based organization preserved  
✅ **Custom Domain**: Use your own domain (Pro plan)  
✅ **Free Hosting**: Netlify free tier is sufficient for most SOPs  

### Custom Domain (Optional)

1. In Netlify Dashboard → Domain settings
2. Add your custom domain
3. Configure DNS settings as instructed
4. SSL certificate is automatically provided

### Updating Content

**Automatic Updates** (Git-based deployment):
- Push changes to your repository
- Netlify automatically rebuilds and deploys

**Manual Updates**:
- Update vault files locally
- Run `python3 build_static.py`
- Upload the new `dist/` folder

### Troubleshooting

**Build Fails**:
- Check that `requirements.txt` includes all dependencies
- Ensure Python 3.6+ is available
- Verify all markdown files are valid

**Links Not Working**:
- Internal links are converted from `[[Page Name]]` format
- Make sure referenced pages exist in the vault
- Check for typos in link names

**Images Not Displaying**:
- Ensure images are in `images/` or `vault/images/` directories
- Use relative paths in markdown: `![alt text](images/photo.jpg)`

### Local Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run development server (original Python server)
python3 serve.py

# Build and preview static site
python3 build_static.py
cd dist && python3 -m http.server 8080
```

---

🎉 **Your SOPs Knowledge Base is now ready for the world!**
