# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Markdown-based presentation system that converts Markdown files to interactive web presentations using Reveal.js. The system allows creating presentations locally or hosting them on a web server.

## Core Architecture

### File Structure
- `generate.py` - Generates the main `index.html` file that lists all available presentations
- `presentacion.html` - The main presentation viewer that renders Markdown content using Reveal.js
- `server.py` - Production web server that serves presentations with proper MIME types
- `server_dev.py` - Development server with auto-reload and cache-busting for live development
- Each presentation is a directory containing:
  - `contenidos.md` - Main presentation content with YAML metadata
  - `images/` - Directory for presentation images
  - `template.webp` - Optional background image (16:9 ratio recommended)

### Presentation Content Structure
Presentations use special Markdown comments for structuring:
- `<!-- SLIDE -->` - Marks the start of a new slide
- `<!-- NOTES -->` - Marks speaker notes (only visible in presenter view)
- YAML frontmatter for configuration (colors, fonts, theme, fontSize)
- Special layout syntax: `$COLUMNS$`, `$COL$`, `$GRID$`, `$ROW$`, `$CELL$`, `$END$`

### Key Components
1. **Presentation Parser** - JavaScript in `presentacion.html` that:
   - Parses YAML frontmatter with robust comment handling
   - Converts Markdown to HTML slides
   - Applies custom colors and styling
   - Handles local file loading via sessionStorage
   - Supports both server-hosted and local presentations

2. **Server Architecture** - Two server modes:
   - Production (`server.py`): Finds free ports (3000-3010), serves static files
   - Development (`server_dev.py`): Fixed port 8000, auto-reload, cache-busting

## Common Development Commands

### Build and Serve
```bash
# Generate index.html and start production server
./start.sh

# Start development server with auto-reload
./startdev.sh

# Generate index.html only
python3 generate.py
```

### Development Workflow
1. Use `./startdev.sh` for active development - provides auto-reload when `contenidos.md` changes
2. Access presentations at `http://localhost:8000/presentacion.html?presentacion=local_<folder-name>`
3. Development mode ignores sessionStorage and always reads fresh content from disk

### Production Deployment
1. Run `./start.sh` to generate index.html and start the server
2. Server automatically finds available port between 3000-3010
3. Presentations can be hosted on any static web server

## Important Implementation Details

### YAML Parser
The system includes a robust YAML parser in JavaScript that:
- Handles end-of-line comments correctly
- Supports nested objects (like the `colors` configuration)
- Preserves quoted strings and special characters

### Local File Handling
- Presentations can be loaded from local directories via file input
- Files are stored in sessionStorage with `local_` prefix
- Images are converted to data URLs for local presentation

### Styling System
- Uses CSS custom properties for dynamic theming
- Background images use `cover`, `center`, `no-repeat`, `fixed` positioning
- Transparent slide backgrounds to show template images and colors

### Development vs Production
- **Development**: Always reads from disk, disables caching, auto-reload enabled
- **Production**: Can use sessionStorage for performance, normal caching

## Testing
This project doesn't have automated tests. Testing is done by:
1. Running presentations in browser
2. Checking different themes and color configurations
3. Testing both local and server-hosted presentations
4. Verifying auto-reload functionality in development mode