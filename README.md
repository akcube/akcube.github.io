# [Kishore Kumar](https://akcube.github.io)

[![Deploy Hugo site to Pages](https://github.com/akcube/akcube.github.io/actions/workflows/hugo.yml/badge.svg)](https://github.com/akcube/akcube.github.io/actions/workflows/hugo.yml)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fakcube.github.io&label=akcube.github.io)](https://akcube.github.io)
[![Hugo](https://img.shields.io/badge/Hugo-v0.124.1+-blue?logo=hugo)](https://gohugo.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/akcube/akcube.github.io)](https://github.com/akcube/akcube.github.io/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/akcube/akcube.github.io)](https://github.com/akcube/akcube.github.io)

Personal blog and portfolio site built with Hugo, featuring automatic publishing from Obsidian vault with hierarchical tags and optimized images.

## Prerequisites

- **Hugo Extended** v0.124.1+ (required for SCSS processing)
- **Go** 1.19+ (required for `hugo-obsidian` tool)
- **Python** 3.10+
- **Node.js** 18+ and npm
- **Git**

## First-Time Setup

### 1. Clone the repository

```bash
git clone --recurse-submodules https://github.com/akcube/akcube.github.io.git
cd akcube.github.io
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

### 2. Install theme dependencies

```bash
cd themes/obsidian-hugo-texify3
npm install
cd ../..
```

### 3. Install the Obsidian Publisher

```bash
pip install obsidian-publisher
```

This installs the `obsidian-publish` CLI tool. See [obsidian-publisher on PyPI](https://pypi.org/project/obsidian-publisher/).

### 4. Install hugo-obsidian for link graph generation

```bash
go install github.com/jackyzha0/hugo-obsidian@latest
```

Verify installation:

```bash
hugo-obsidian --help
```

## Running the Site Locally

### Start the Hugo development server

```bash
hugo server -D
```

This will:
- Build the site with draft posts included (`-D` flag)
- Start a local server at `http://localhost:1313`
- Watch for file changes and auto-reload
- Enable live browser reload

**Additional useful flags:**
- `--bind 0.0.0.0` - Allow external connections (useful for testing on mobile)
- `--port 1313` - Specify custom port
- `--navigateToChanged` - Navigate to changed content on live reload

### Build for production

```bash
hugo --minify
```

Output will be in the `public/` directory.

## Publishing from Obsidian Vault

### Workflow Overview

The publisher automatically discovers and publishes notes tagged with `status/evergreen` from your Obsidian vault:

1. Run the publisher to convert Obsidian markdown to Hugo format
2. Run `hugo-obsidian` to generate link indices for the graph visualization
3. Review changes locally with `hugo server -D`
4. Commit and push to deploy

### Quick Workflow

```bash
# 1. Publish from vault
obsidian-publish republish -c publisher-config.yaml

# 2. Generate link indices for graph
hugo-obsidian -input=content -output=assets/indices -index -root=.

# 3. Test locally
hugo server -D
```

### What the Publisher Does

- **Auto-discovers** notes with `status/evergreen` tag in `Zettelkasten/`
- **Converts hierarchical tags** like `domain/cs/algorithms` to URL-safe format (`domain-cs-algorithms`)
- **Processes wikilinks** (`[[Note Title]]` → `[Note Title](/blog/note-title)`)
- **Optimizes images** to WebP with PNG fallback
- **Cleans up orphaned** images no longer referenced

### Dry Run

To see what would be published without making changes:

```bash
obsidian-publish republish -c publisher-config.yaml --dry-run
```

### Other Commands

```bash
# Publish a specific note
obsidian-publish add "My Note Title" -c publisher-config.yaml

# Remove a published note
obsidian-publish delete "My Note Title" -c publisher-config.yaml

# List all publishable notes
obsidian-publish list-notes -c publisher-config.yaml
```

## Obsidian Vault Structure

The publisher expects notes in your vault to follow this structure:

```yaml
---
title: "My Note Title"
tags:
  - domain/cs/algorithms/analysis   # Hierarchical domain tags
  - type/zettelkasten               # Note type
  - status/evergreen                # Required for publishing
created: 2024-01-15
---

Your note content with [[wikilinks]] and ![[images.png]]...
```

### Tag System

- **`status/evergreen`** - Required for publishing
- **`status/seed`** or **`status/sapling`** - Excluded from publishing
- **`domain/*`** - Converted to display tags (e.g., `domain/cs/algorithms` → `domain-cs-algorithms`)

## Project Structure

```
.
├── content/              # Hugo content
│   ├── blog/            # Published blog posts (auto-generated)
│   └── ...
├── static/              # Static assets
│   ├── images/          # Optimized blog images (WebP + PNG)
│   ├── css/             # Custom CSS
│   └── js/              # Custom JavaScript
├── assets/
│   └── indices/         # Link indices from hugo-obsidian
├── layouts/             # Hugo layout overrides
│   ├── _default/
│   │   ├── list.html    # Blog list with tag display
│   │   ├── single.html  # Blog post with tags
│   │   └── _markup/     # Custom markdown rendering
│   └── tags/            # Tag taxonomy pages
├── themes/              # Hugo themes
│   └── obsidian-hugo-texify3/  # Custom theme (git submodule)
├── publisher-config.yaml # Publisher configuration
├── hugo.toml            # Hugo configuration
└── .gitignore
```

## Image Optimization

All images are automatically optimized during publishing:
- **Display size**: Max 1920px width
- **Format**: WebP with PNG fallback for browser compatibility
- **Compression**: 85% WebP quality, optimized PNG
- **Zoom**: Click any image to view full-size with smooth animation

## Configuration

Publisher settings are in `publisher-config.yaml`:

```yaml
# Path to your Obsidian vault
vault_path: ~/Kishore-Brain

# Path to your Hugo site
output_path: ~/akcube.github.io

# Subdirectory within vault to scan for notes
source_dir: Zettelkasten

# Output directories within the Hugo site
content_dir: content/blog
image_dir: static/images

# Directories within vault to search for images
image_sources:
  - Files
  - Zettelkasten

# Tags for filtering notes
required_tags:
  - status/evergreen
excluded_tags:
  - status/seed
  - status/sapling
  - status/draft

# Image optimization settings
optimize_images: true
max_image_width: 1920
webp_quality: 85
image_path_prefix: /images

# Link transform: absolute links with /blog prefix
link_transform:
  type: absolute
  prefix: /blog

# Tag transform: filter domain tags only and replace / with -
tag_transform:
  prefixes:
    - domain
  replace_separator:
    - "/"
    - "-"

# Hugo frontmatter settings
frontmatter:
  hugo: true
  author: Kishore Kumar
```

## License

Content is © Kishore Kumar. Theme based on [Obsidian TeXify3](https://github.com/akcube/obsidian-hugo-texify3).
