"""
Discovery Module - Auto-discover publishable notes from vault
Scans Zettelkasten directory for markdown files with evergreen status
"""

import os
import yaml
from pathlib import Path
from typing import List, Dict, Set, Tuple


class NoteDiscovery:
    """Discovers and filters notes eligible for publishing"""

    def __init__(self, vault_path: str, source_dir: str, config: Dict):
        self.vault_path = Path(vault_path)
        self.source_dir = self.vault_path / source_dir
        self.required_tags = set(config['filters']['required_tags'])
        self.excluded_tags = set(config['filters']['excluded_tags'])

    def discover_all_notes(self) -> List[Path]:
        """Find all markdown files in source directory"""
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")

        notes = list(self.source_dir.glob("*.md"))
        print(f"Found {len(notes)} total notes in {self.source_dir}")
        return notes

    def parse_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """
        Parse YAML frontmatter and content from markdown file

        Returns:
            Tuple of (frontmatter_dict, content_string)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        if not content.startswith('---'):
            return {}, content

        try:
            # Split frontmatter from content
            parts = content.split('---\n', 2)
            if len(parts) < 3:
                return {}, content

            frontmatter_str = parts[1]
            content_str = parts[2]

            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_str)
            if not isinstance(frontmatter, dict):
                return {}, content

            return frontmatter, content_str

        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse YAML in {file_path.name}: {e}")
            return {}, content

    def extract_tags(self, frontmatter: Dict) -> Set[str]:
        """Extract all tags from frontmatter, handling both list and string formats"""
        tags = set()

        if 'tags' in frontmatter:
            tag_data = frontmatter['tags']
            if isinstance(tag_data, list):
                tags.update(str(tag) for tag in tag_data)
            elif isinstance(tag_data, str):
                tags.add(tag_data)

        return tags

    def is_publishable(self, file_path: Path) -> Tuple[bool, str]:
        """
        Check if a note meets publishing criteria

        Returns:
            Tuple of (is_publishable: bool, reason: str)
        """
        frontmatter, _ = self.parse_frontmatter(file_path)
        tags = self.extract_tags(frontmatter)

        # Check for required tags
        if not self.required_tags.intersection(tags):
            missing = ', '.join(self.required_tags)
            return False, f"Missing required tags: {missing}"

        # Check for excluded tags
        excluded_found = self.excluded_tags.intersection(tags)
        if excluded_found:
            found = ', '.join(excluded_found)
            return False, f"Contains excluded tags: {found}"

        return True, "OK"

    def discover_publishable_notes(self, verbose: bool = False) -> List[Path]:
        """
        Discover all notes eligible for publishing

        Args:
            verbose: Print detailed filtering information

        Returns:
            List of file paths for publishable notes
        """
        all_notes = self.discover_all_notes()
        publishable = []
        skipped = []

        for note_path in all_notes:
            is_pub, reason = self.is_publishable(note_path)

            if is_pub:
                publishable.append(note_path)
                if verbose:
                    print(f"✓ {note_path.name}: {reason}")
            else:
                skipped.append((note_path, reason))
                if verbose:
                    print(f"✗ {note_path.name}: {reason}")

        print(f"\nDiscovery Summary:")
        print(f"  Total notes: {len(all_notes)}")
        print(f"  Publishable: {len(publishable)}")
        print(f"  Skipped: {len(skipped)}")

        if not verbose and skipped:
            print(f"\nSkipped notes (use --verbose for details):")
            for note_path, reason in skipped[:5]:
                print(f"  - {note_path.name}: {reason}")
            if len(skipped) > 5:
                print(f"  ... and {len(skipped) - 5} more")

        return publishable

    def get_note_metadata(self, file_path: Path) -> Dict:
        """Get full metadata for a note including frontmatter and tags"""
        frontmatter, content = self.parse_frontmatter(file_path)
        tags = self.extract_tags(frontmatter)

        return {
            'path': file_path,
            'name': file_path.name,
            'stem': file_path.stem,
            'frontmatter': frontmatter,
            'tags': tags,
            'content': content
        }


def main():
    """Test the discovery module"""
    import yaml

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Initialize discovery
    discovery = NoteDiscovery(
        vault_path=config['vault_path'],
        source_dir=config['source_dir'],
        config=config
    )

    # Discover notes
    publishable = discovery.discover_publishable_notes(verbose=True)

    print(f"\n\nPublishable Notes ({len(publishable)}):")
    for note in publishable[:10]:
        print(f"  - {note.name}")
    if len(publishable) > 10:
        print(f"  ... and {len(publishable) - 10} more")


if __name__ == '__main__':
    main()
