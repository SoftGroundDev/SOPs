#!/bin/bash

# Netlify Deployment Script for SOPs Knowledge Base

echo "🚀 Starting Netlify deployment build..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

# Generate static site
echo "🔧 Generating static site..."
python3 build_static.py

# Verify build output
if [ -d "dist" ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Generated files:"
    ls -la dist/
    if [ -d "dist/vault" ]; then
        echo "📚 Vault files:"
        ls -la dist/vault/ | head -10
    fi
else
    echo "❌ Build failed - dist directory not found"
    exit 1
fi

echo "🌐 Ready for Netlify deployment!"
