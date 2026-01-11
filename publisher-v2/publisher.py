#!/usr/bin/env python3
"""
Enhanced Obsidian to Hugo Publisher
Automatically publishes evergreen notes from vault to Hugo website

Features:
- Auto-discovery of publishable notes (status/evergreen tag)
- Hierarchical tag conversion to Hugo taxonomies
- Wikilink processing
- Image optimization
- Orphan cleanup (removes posts for de-evergreened notes)
"""

import argparse
import datetime
import git
import inflection
import os
import sys
import titlecase
import yaml
from pathlib import Path
from typing import Dict, List, Set

# Import our modules
from discovery import NoteDiscovery
from tag_converter import TagConverter
from link_processor import LinkProcessor

# Import image optimizer from old publisher
old_publisher_path = Path(__file__).parent.parent / 'publisher' / 'publisher.py'
import importlib.util
spec = importlib.util.spec_from_file_location("old_publisher", old_publisher_path)
old_publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old_publisher)
optimize_image = old_publisher.optimize_image


class Publisher:
    """Main publisher orchestrator"""

    def __init__(self, config_path: str = 'config.yaml'):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize paths
        self.vault_path = Path(self.config['vault_path'])
        self.website_path = Path(self.config['website_path'])
        self.dest_dir = self.website_path / self.config['dest_dir']
        self.image_dest = self.website_path / self.config['image_dest']

        # Initialize modules
        self.discovery = NoteDiscovery(
            vault_path=self.config['vault_path'],
            source_dir=self.config['source_dir'],
            config=self.config
        )
        self.tag_converter = TagConverter(self.config)
        self.link_processor = LinkProcessor(self.config)

        # Ensure output directories exist
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        self.image_dest.mkdir(parents=True, exist_ok=True)

    def get_creation_date(self, file_path: Path) -> str:
        """Get file creation date from git history or filesystem"""
        try:
            repo = git.Repo(file_path, search_parent_directories=True)
            log = repo.git.log("--follow", "--format=%ad", "--", str(file_path))

            if not log:
                # Fallback to filesystem
                local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                dt = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
                return dt.replace(tzinfo=local_timezone).strftime('%Y-%m-%d %H:%M:%S%z')
            else:
                # Parse git date
                date_str = log.split('\n')[-1]
                return datetime.datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y %z').strftime('%Y-%m-%d %H:%M:%S%z')
        except Exception as e:
            # Fallback to current time
            print(f"Warning: Could not get creation date for {file_path.name}: {e}")
            return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')

    def get_original_publication_date(self, slug: str, frontmatter: Dict) -> str:
        """
        Get original publication date from existing published file or frontmatter

        Args:
            slug: Output slug for the file
            frontmatter: Frontmatter from source note

        Returns:
            Publication date string in ISO format
        """
        # Check if file already exists in published site
        output_path = self.dest_dir / f"{slug}.md"

        if output_path.exists():
            try:
                # Try to get date from published file's git history
                repo = git.Repo(self.website_path, search_parent_directories=True)

                # Get the date field from the previous version via git
                try:
                    content = repo.git.show(f"HEAD:{output_path.relative_to(self.website_path)}")
                    # Parse the frontmatter to extract date
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 2:
                            import yaml
                            old_frontmatter = yaml.safe_load(parts[1])
                            if old_frontmatter and 'date' in old_frontmatter:
                                # Return the old publication date
                                old_date = old_frontmatter['date']
                                if isinstance(old_date, str):
                                    return old_date
                                elif isinstance(old_date, datetime.datetime):
                                    return old_date.strftime('%Y-%m-%d %H:%M:%S%z')
                except:
                    pass
            except:
                pass

        # For new files, use 'created' date from frontmatter if available
        if 'created' in frontmatter:
            created = frontmatter['created']
            if isinstance(created, str):
                # Try to parse and reformat
                try:
                    dt = datetime.datetime.strptime(created, '%Y-%m-%d')
                    return dt.strftime('%Y-%m-%d %H:%M:%S%z')
                except:
                    return created
            elif isinstance(created, datetime.datetime):
                return created.strftime('%Y-%m-%d %H:%M:%S%z')

        # Last resort: use current time
        return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')

    def process_note(self, note_path: Path) -> bool:
        """
        Process and publish a single note

        Args:
            note_path: Path to source markdown file

        Returns:
            True if published successfully, False otherwise
        """
        try:
            # Get note metadata
            metadata = self.discovery.get_note_metadata(note_path)
            frontmatter = metadata['frontmatter']
            content = metadata['content']
            tags = metadata['tags']

            # Generate output slug
            title = frontmatter.get('title', metadata['stem'])
            slug = inflection.parameterize(title)

            print(f"→ Publishing {note_path.name} as {slug}.md")

            # Filter to only domain tags (remove status/type)
            domain_tags = [tag for tag in tags if self.tag_converter.parse_hierarchical_tag(tag).get('root') == 'domain']

            # Build clean frontmatter - only keep what we need
            enhanced_frontmatter = {}

            # Convert to URL-safe format for Hugo taxonomies (replace / with -)
            # Templates will convert back to slashes for display
            if domain_tags:
                url_safe_tags = [tag.replace('/', '-') for tag in domain_tags]
                enhanced_frontmatter['tags'] = sorted(url_safe_tags)

            # Add additional Hugo metadata
            # Use original publication date if file was previously published
            enhanced_frontmatter['date'] = self.get_original_publication_date(slug, frontmatter)
            enhanced_frontmatter['doc'] = self.get_creation_date(note_path)
            enhanced_frontmatter['title'] = titlecase.titlecase(title).replace(';', ':')
            enhanced_frontmatter['author'] = 'Kishore Kumar'

            # Process links and images
            processed_content, referenced_notes = self.link_processor.process_wikilinks(content)
            processed_content, image_deps = self.link_processor.process_images(processed_content)

            # Add related reading section (uses original frontmatter for 'related' field)
            # Pass referenced_notes to avoid duplicating links already in content
            if self.config['features']['enable_related_reading']:
                related_section = self.link_processor.generate_related_section(frontmatter, slug, referenced_notes)
                processed_content += related_section

            # Process and copy images
            self._process_images(image_deps, note_path)

            # Write published file
            output_path = self.dest_dir / f"{slug}.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('---\n')
                f.write(yaml.dump(enhanced_frontmatter, allow_unicode=True, default_flow_style=False))
                f.write('---\n')
                f.write(processed_content)

            print(f"  ✓ Published successfully")
            print(f"    Tags: {', '.join(enhanced_frontmatter.get('display_tags', []))}")

            return True

        except Exception as e:
            print(f"  ✗ Error publishing {note_path.name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _process_images(self, image_deps: Set[str], note_path: Path):
        """Find and optimize images referenced by note"""
        if not self.config['features']['optimize_images']:
            return

        # Search for images in configured directories
        img_source_dirs = [self.vault_path / d for d in self.config['image_sources']]

        for img_name in image_deps:
            img_found = False

            # Search each source directory
            for source_dir in img_source_dirs:
                for root, _, files in os.walk(source_dir):
                    if img_name in files:
                        img_path = Path(root) / img_name
                        img_basename = Path(img_name).stem
                        slug = inflection.parameterize(img_basename)

                        # Optimize and save
                        optimize_image(
                            str(img_path),
                            str(self.image_dest),
                            slug,
                            max_width=self.config['images']['max_width'],
                            webp_quality=self.config['images']['webp_quality'],
                            png_optimize=self.config['images']['png_optimize']
                        )

                        img_found = True
                        break

                if img_found:
                    break

            if not img_found:
                print(f"  ⚠ Warning: Image not found: {img_name}")

    def publish_all(self, dry_run: bool = False):
        """
        Discover and publish all evergreen notes

        Args:
            dry_run: Don't actually publish, just show what would be published
        """
        print("=" * 70)
        print("OBSIDIAN TO HUGO PUBLISHER")
        print("=" * 70)

        # Discover publishable notes
        print("\n📂 Discovering publishable notes...")
        publishable_notes = self.discovery.discover_publishable_notes(verbose=False)

        if not publishable_notes:
            print("\n⚠ No publishable notes found!")
            return

        print(f"\n📝 Found {len(publishable_notes)} evergreen notes")

        if dry_run:
            print("\n🔍 DRY RUN - Would publish:")
            for note in publishable_notes:
                print(f"  - {note.name}")
            return

        # Publish each note
        print(f"\n📤 Publishing {len(publishable_notes)} notes...")
        published_count = 0
        failed_count = 0

        for note_path in publishable_notes:
            if self.process_note(note_path):
                published_count += 1
            else:
                failed_count += 1

        print(f"\n📊 Summary:")
        print(f"  Published: {published_count}")
        print(f"  Failed: {failed_count}")

        # Clean orphaned files
        self._clean_orphaned_files(publishable_notes)
        self._clean_orphaned_images()

        print("\n✅ Publishing complete!")
        print("\n💡 Remember to run: hugo-obsidian -input=content -output=assets/indices -index -root=.")

    def _clean_orphaned_files(self, current_notes: List[Path]):
        """Remove published files that no longer have source in vault"""
        # Get current slugs from evergreen notes
        current_slugs = set()
        for note_path in current_notes:
            metadata = self.discovery.get_note_metadata(note_path)
            title = metadata['frontmatter'].get('title', metadata['stem'])
            slug = inflection.parameterize(title)
            current_slugs.add(slug + '.md')

        # Get all published files
        published_files = set(f.name for f in self.dest_dir.glob('*.md'))

        # Find orphaned files (published but no longer evergreen)
        orphaned = published_files - current_slugs

        if orphaned:
            print(f"\n🧹 Cleaning {len(orphaned)} orphaned files:")
            for filename in orphaned:
                output_path = self.dest_dir / filename
                output_path.unlink()
                print(f"  ✓ Removed {filename}")
        else:
            print("\n✨ No orphaned files to clean")

    def _clean_orphaned_images(self):
        """Remove images that are no longer referenced by any published post"""
        import re

        # Collect all referenced images from published posts
        referenced_images = set()
        for md_file in self.dest_dir.glob('*.md'):
            content = md_file.read_text(encoding='utf-8')
            # Match ![alt](/images/name.webp) pattern
            matches = re.findall(r'!\[[^\]]*\]\(/images/([^)]+)\)', content)
            for match in matches:
                # Add both the referenced file and its base name (for .png fallback)
                referenced_images.add(match)
                # Also add the .png version if .webp is referenced
                if match.endswith('.webp'):
                    referenced_images.add(match.replace('.webp', '.png'))

        # Get all images in static/images
        existing_images = set()
        for ext in ['*.webp', '*.png', '*.jpg', '*.jpeg', '*.gif']:
            for img in self.image_dest.glob(ext):
                existing_images.add(img.name)

        # Find orphaned images
        orphaned = existing_images - referenced_images

        if orphaned:
            print(f"\n🖼️  Cleaning {len(orphaned)} orphaned images:")
            for img_name in sorted(orphaned):
                img_path = self.image_dest / img_name
                img_path.unlink()
                print(f"  ✓ Removed {img_name}")
        else:
            print("\n✨ No orphaned images to clean")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Obsidian to Hugo Publisher - Publishes evergreen notes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish all evergreen notes
  python publisher.py

  # Dry run (show what would be published)
  python publisher.py --dry-run

After publishing, run hugo-obsidian to generate link indices:
  hugo-obsidian -input=content -output=assets/indices -index -root=.
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Don't actually publish, just show what would be published"
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    args = parser.parse_args()

    # Initialize publisher
    try:
        publisher = Publisher(config_path=args.config)
    except Exception as e:
        print(f"Error initializing publisher: {e}")
        sys.exit(1)

    publisher.publish_all(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
