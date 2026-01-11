# Obsidian to Hugo Publisher v2

Automatically publishes evergreen notes from your Obsidian vault to Hugo website with hierarchical tag support, wikilink processing, and image optimization.

## Features

- **Auto-Discovery** - Finds notes with `status/evergreen` tag
- **Hierarchical Tags** - Converts `domain/cs/algorithms` to URL-safe format for Hugo
- **Wikilink Processing** - Converts `[[Note]]` to Hugo-compatible links
- **Image Optimization** - Auto-converts images to WebP with PNG fallback
- **Related Reading** - Generates related notes section from frontmatter
- **Orphan Cleanup** - Removes posts and images no longer in vault

## Architecture

```
publisher-v2/
├── publisher.py           # Main orchestrator
├── discovery.py           # Auto-scans vault for publishable notes
├── tag_converter.py       # Hierarchical tag processing
├── link_processor.py      # Wikilinks, images, related reading
├── config.yaml            # Configuration
└── requirements.txt       # Python dependencies
```

## Installation

```bash
cd publisher-v2
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml`:

```yaml
vault_path: "/home/akcube/Kishore-Brain"
website_path: "/home/akcube/akcube.github.io-worktree"
source_dir: "Zettelkasten"
dest_dir: "content/blog"
image_dest: "static/images"

filters:
  required_tags:
    - "status/evergreen"
  excluded_tags:
    - "status/seed"
    - "status/sapling"

features:
  enable_related_reading: true
  optimize_images: true

images:
  max_width: 1920
  webp_quality: 85
  png_optimize: true
```

## Usage

### Publish all evergreen notes

```bash
python publisher.py
```

This will:
1. Scan `Zettelkasten/` for markdown files
2. Filter for notes with `status/evergreen` tag
3. Convert and publish all matching notes
4. Optimize images to WebP
5. Clean up orphaned posts and images

### Dry run (preview without changes)

```bash
python publisher.py --dry-run
```

### After publishing

Run hugo-obsidian to generate link indices:

```bash
cd ..
hugo-obsidian -input=content -output=assets/indices -index -root=.
```

## Tag System

The publisher uses a simplified tag system with only the `tags` taxonomy.

### Input (Obsidian frontmatter)

```yaml
tags:
  - domain/cs/algorithms/analysis
  - domain/cs/algorithms/complexity
  - type/zettelkasten
  - status/evergreen
```

### Output (Hugo frontmatter)

```yaml
tags:
  - domain-cs-algorithms-analysis
  - domain-cs-algorithms-complexity
```

- Only `domain/*` tags are published
- Slashes are converted to hyphens for URL safety
- Hugo templates convert hyphens back to slashes for display (`#domain/cs/algorithms/analysis`)
- `type/*` and `status/*` tags are used for filtering only

## Link Processing

### Wikilinks

```markdown
# Input (Obsidian)
See [[Deep Dive into Knapsack Problem]] for more.
Also check [[Complex Note Title|simpler alias]].

# Output (Hugo)
See [Deep Dive into Knapsack Problem](/blog/deep-dive-into-knapsack-problem) for more.
Also check [simpler alias](/blog/complex-note-title).
```

### Images

```markdown
# Input
![[diagram.png]]

# Output
![diagram](/images/diagram.webp)
```

Images are automatically:
- Resized to max 1920px width
- Converted to WebP (85% quality)
- PNG fallback generated
- Copied to `static/images/`

## Related Reading

The publisher generates a "Related Reading" section from the `related` field, excluding notes already linked in content:

```yaml
# Frontmatter
related:
  - "[[Linear Regression]]"
  - "[[Neural Networks]]"
```

Output (appended to post):

```markdown
---

## Related Reading

- [Linear Regression](/blog/linear-regression)
- [Neural Networks](/blog/neural-networks)
```

## Orphan Cleanup

The publisher automatically removes:
- **Posts** in `content/blog/` without a matching evergreen source
- **Images** in `static/images/` not referenced by any published post

## Output Structure

```
website/
├── content/
│   └── blog/
│       ├── knapsack-problem.md
│       ├── linear-regression.md
│       └── ... (60 evergreen notes)
└── static/
    └── images/
        ├── diagram.webp
        ├── diagram.png
        └── ...
```

## Troubleshooting

### No notes discovered

- Check that notes have `status/evergreen` in tags
- Verify `vault_path` and `source_dir` in config.yaml
- Notes with `status/seed` or `status/sapling` are excluded

### Images not found

- Check that image source directories are configured in `image_sources`
- Verify images exist in `Files/` or `Zettelkasten/`
- Check console warnings for missing images

### Links broken

- Ensure referenced notes are also published (have evergreen tag)
- Check that note titles match wikilink text

## Testing Modules

Each module can be tested independently:

```bash
python discovery.py      # Test note discovery
python tag_converter.py  # Test tag conversion
python link_processor.py # Test link processing
```
