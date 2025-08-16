# Adding Images to Your SOP Documentation

This guide explains how to add pictures, diagrams, screenshots, and other visual content to your SOP documentation.

## 📁 Image Directory Structure

Your SOP system supports images in two main locations:

### 1. Global Images Directory (`/images/`)
```
images/
├── diagrams/          # System diagrams, architecture charts
├── screenshots/       # Application screenshots, UI elements  
├── flowcharts/        # Process flowcharts
└── [other-folders]/   # Custom categories
```

### 2. Vault Images Directory (`/vault/images/`)
```
vault/
├── images/            # Images specific to vault content
├── Operations/
├── Emergency/
└── templates/
```

## 🖼️ How to Add Images

### Method 1: Using Global Images Directory

1. **Add your image file** to the appropriate subfolder in `/images/`:
   ```
   images/screenshots/login-screen.png
   images/diagrams/network-topology.jpg
   images/flowcharts/incident-response.svg
   ```

2. **Reference in markdown** using:
   ```markdown
   ![Alt Text](/images/screenshots/login-screen.png)
   ![Network Diagram](/images/diagrams/network-topology.jpg)
   ![Process Flow](/images/flowcharts/incident-response.svg)
   ```

### Method 2: Using Vault Images Directory

1. **Add your image file** to `/vault/images/`:
   ```
   vault/images/emergency-contacts.png
   vault/images/server-room-layout.jpg
   ```

2. **Reference in markdown** using:
   ```markdown
   ![Emergency Contacts](/vault/images/emergency-contacts.png)
   ![Server Room](/vault/images/server-room-layout.jpg)
   ```

### Method 3: Co-located Images

You can also place images directly in the same folder as your markdown files:

```
vault/Operations/
├── Daily System Health Check.md
└── server-status-example.png
```

Then reference with:
```markdown
![Server Status Example](server-status-example.png)
```

## 🎨 Supported Image Formats

- **JPEG/JPG** (`.jpg`, `.jpeg`) - Best for photographs
- **PNG** (`.png`) - Best for screenshots, diagrams with transparency
- **SVG** (`.svg`) - Best for scalable graphics, logos
- **GIF** (`.gif`) - For simple animations
- **WebP** (`.webp`) - Modern format with better compression
- **BMP** (`.bmp`) - Basic bitmap format
- **TIFF** (`.tiff`) - High quality format

## 📝 Markdown Image Syntax

### Basic Image
```markdown
![Alt Text](path/to/image.png)
```

### Image with Title (tooltip)
```markdown
![Alt Text](path/to/image.png "This shows on hover")
```

### Image with Custom Size (HTML)
```html
<img src="/images/diagrams/architecture.png" alt="System Architecture" width="600" height="400">
```

### Image with Caption
```markdown
![System Dashboard](/images/screenshots/dashboard.png)
*Figure 1: Main system dashboard showing key metrics*
```

### Linked Image
```markdown
[![Clickable Image](/images/thumb.png)](/images/full-size.png)
```

## 🎯 Best Practices

### File Organization
- Use **descriptive filenames**: `login-process-flowchart.png` instead of `image1.png`
- Create **logical folders** based on content type or SOP category
- Keep **consistent naming** conventions across your documentation

### Image Optimization
- **Compress images** to reduce file sizes and improve loading times
- Use **appropriate formats**:
  - PNG for screenshots and images with text
  - JPEG for photographs
  - SVG for diagrams and icons
- Consider **image dimensions** - most SOPs work well with 800px width max

### Accessibility
- Always include **meaningful alt text** describing the image content
- Use **descriptive captions** for complex diagrams
- Ensure **sufficient contrast** in screenshots and diagrams

### File Size Guidelines
- **Screenshots**: Keep under 500KB
- **Diagrams**: Keep under 200KB  
- **Photos**: Keep under 1MB
- **Icons**: Keep under 50KB

## 📋 Example Usage in SOPs

### Emergency Procedures
```markdown
# Server Room Fire Emergency

## Evacuation Route
![Evacuation Route](/images/diagrams/server-room-evacuation.png)
*Follow the highlighted path to the nearest emergency exit*

## Fire Suppression Controls
![Fire Control Panel](/images/screenshots/fire-panel.jpg "Fire suppression control panel")
```

### System Operations
```markdown
# Database Backup Verification

## Step 1: Access Backup Dashboard
![Backup Dashboard](/images/screenshots/backup-dashboard.png)

## Step 2: Verify Backup Status
Look for the green checkmarks as shown below:
<img src="/images/screenshots/backup-status.png" alt="Backup Status" width="400">
```

### Process Flowcharts
```markdown
# Incident Response Protocol

## Decision Flow
![Incident Response Flow](/images/flowcharts/incident-response.svg)
*This flowchart guides you through the complete incident response process*
```

## 🔧 Technical Details

### Image Caching
- Images are cached for 24 hours to improve performance
- Clear browser cache if you update an image and don't see changes

### Image URLs
- Global images: `http://localhost:8000/images/[subfolder]/[filename]`
- Vault images: `http://localhost:8000/vault/images/[filename]`
- Co-located images: Relative path from the markdown file

### Troubleshooting

**Image not showing?**
1. Check the file path is correct
2. Verify the file exists in the expected location
3. Ensure the file extension is supported
4. Check browser console for any errors

**Image too large?**
1. Use HTML `<img>` tag with width/height attributes
2. Optimize the image file size
3. Consider using thumbnails that link to full-size images

## 📚 Quick Reference

| Task | Markdown Syntax | Example |
|------|----------------|---------|
| Basic image | `![Alt](path)` | `![Logo](/images/logo.png)` |
| Image with title | `![Alt](path "title")` | `![Logo](/images/logo.png "Company Logo")` |
| Sized image | `<img src="path" width="300">` | `<img src="/images/diagram.png" width="300">` |
| Linked image | `[![Alt](thumb)](full)` | `[![Thumb](/images/thumb.jpg)](/images/full.jpg)` |

---

*💡 Tip: Start with screenshots and simple diagrams, then expand to more complex visual content as your SOP library grows.*
