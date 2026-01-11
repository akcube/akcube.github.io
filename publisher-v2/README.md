# Enhanced Obsidian to Hugo Publisher v2

Automatically publishes evergreen notes from your Obsidian vault to Hugo website with intelligent filtering, hierarchical tag conversion, and backlink generation.

## Features

✅ **Auto-Discovery**: Automatically finds notes with `status/evergreen` tag
✅ **Hierarchical Tags**: Converts `domain/cs/algorithms` to Hugo categories & topics
✅ **Incremental Publishing**: Only publishes changed notes
✅ **Wikilink Processing**: Converts `[[Note]]` to Hugo-compatible links
✅ **Image Optimization**: Auto-converts images to WebP
✅ **Backlink Generation**: Creates bidirectional link graph
✅ **Related Reading**: Auto-generates related notes section
✅ **Change Detection**: Tracks MD5 hashes to avoid redundant publishing
✅ **Orphan Cleanup**: Removes published notes that no longer exist in vault

## Architecture

```
publisher-v2/
├── publisher.py           # Main orchestrator
├── discovery.py           # Auto-scans vault for publishable notes
├── tag_converter.py       # Hierarchical tag → Hugo taxonomy conversion
├── link_processor.py      # Wikilinks, images, backlinks
├── manifest.py            # Change tracking
├── config.yaml            # Configuration
└── README.md              # This file
```

## Installation

```bash
cd /home/akcube/akcube.github.io-worktree/publisher-v2

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to customize:

```yaml
vault_path: "/home/akcube/Kishore-Brain"
source_dir: "Zettelkasten"
dest_dir: "content/blog"

filters:
  required_tags:
    - "status/evergreen"
```

See `config.yaml` for full configuration options.

## Usage

### Auto-publish all evergreen notes (incremental)
```bash
python publisher.py --auto
```

This will:
1. Scan `Zettelkasten/` for markdown files
2. Filter for notes with `status/evergreen` tag
3. Check which ones have changed since last publish
4. Publish only new/modified notes
5. Generate backlink graph
6. Clean up orphaned files

### Force republish everything
```bash
python publisher.py --auto --force
```

### Dry run (see what would be published)
```bash
python publisher.py --auto --dry-run
```

## Tag Conversion

The publisher intelligently converts your hierarchical tags to Hugo taxonomies:

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
topics: ["algorithm-analysis", "complexity-theory"]
categories: ["Computer Science", "Algorithms"]
series: "Zettelkasten"
```

### Mapping Rules

**Domain tags** → Categories + Topics:
- `domain/cs/algorithms/analysis` → Category: "Computer Science, Algorithms", Topic: "algorithm-analysis"
- `domain/finance/quantitative` → Category: "Finance", Topic: "quantitative-finance"
- `domain/math/probability-statistics` → Category: "Mathematics", Topic: "probability-statistics"

**Type tags** → Series:
- `type/zettelkasten` → Series: "Zettelkasten"
- `type/literature-note` → Series: "Literature Notes"

**Status tags** → Filters only (not published):
- `status/evergreen` → Publishable
- `status/seed` → Not published
- `status/sapling` → Not published

## Link Processing

### Wikilinks
```markdown
# Input (Obsidian)
See [[Deep Dive into Knapsack Problem]] for more.
Also check [[Complex Note Title|simpler alias]].

# Output (Hugo)
See [Deep Dive into Knapsack Problem](/blog/deep-dive-into-knapsack-problem/) for more.
Also check [simpler alias](/blog/complex-note-title/).
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

## Backlinks

When enabled, the publisher generates `data/backlinks.json`:

```json
{
  "knapsack-problem": [
    {
      "slug": "dp-as-dags",
      "title": "DP as DAGs",
      "url": "/blog/dp-as-dags/"
    }
  ]
}
```

Use this in your Hugo theme to show "Referenced By" sections.

## Related Reading

The publisher automatically generates a "Related Reading" section from the `related` field in frontmatter:

```yaml
# Frontmatter
related:
  - "[[Linear Regression]]"
  - "[[Logistic Regression]]"
  - "[[Neural Networks]]"
```

Becomes:

```markdown
## Related Reading

- [Linear Regression](/blog/linear-regression/)
- [Logistic Regression](/blog/logistic-regression/)
- [Neural Networks](/blog/neural-networks/)
```

## Change Detection

The publisher maintains a manifest (`data/publish-manifest.json`) with MD5 hashes:

```json
{
  "last_publish": "2026-01-04T22:30:00Z",
  "published_files": {
    "knapsack-problem": {
      "source_path": "/home/akcube/Kishore-Brain/Zettelkasten/...",
      "hash": "a1b2c3d4e5f6...",
      "published_date": "2026-01-04T22:30:00Z",
      "categories": ["Computer Science", "Algorithms"],
      "topics": ["dynamic-programming", "complexity-theory"]
    }
  }
}
```

Only files with changed hashes are republished (unless `--force`).

## Orphan Cleanup

Files in `content/blog/` that no longer have a source in vault are automatically removed. This keeps your published site in sync with your vault.

## Output Structure

```
akcube.github.io-worktree/
├── content/
│   └── blog/
│       ├── knapsack-problem.md
│       ├── linear-regression.md
│       └── ... (69 evergreen notes)
├── static/
│   └── images/
│       ├── diagram.webp
│       ├── diagram.png
│       └── ...
└── data/
    ├── publish-manifest.json
    └── backlinks.json
```

## Troubleshooting

### No notes discovered
- Check that notes have `status/evergreen` in tags
- Verify `vault_path` and `source_dir` in config.yaml
- Run with `--verbose` to see why notes are skipped

### Images not found
- Check that image source directories are configured
- Verify images exist in `Files/` or `Zettelkasten/`
- Check console warnings for missing images

### Links broken
- Ensure referenced notes are also published (have evergreen tag)
- Check that note titles match wikilink text

### No changes detected
- Use `--force` to republish everything
- Check `data/publish-manifest.json` for stored hashes

## Testing Modules

Each module can be tested independently:

```bash
# Test discovery
python discovery.py

# Test tag conversion
python tag_converter.py

# Test link processing
python link_processor.py

# Test manifest
python manifest.py
```

## Migration from v1

1. Backup current website
2. Test v2 with dry run: `python publisher.py --auto --dry-run`
3. Publish: `python publisher.py --auto`
4. Verify output in `content/blog/`
5. Deploy to GitHub Pages

## Next Steps

1. **Hugo Config**: Update `hugo.toml` to add `categories` and `series` taxonomies
2. **Theme Updates**: Add backlinks display to post template
3. **Category Pages**: Create landing pages for each category
4. **CI/CD**: Set up GitHub Actions to auto-publish on commit

## Support

See `/home/akcube/Kishore-Brain/Meta/publisher-redesign-plan.md` for full design documentation.
