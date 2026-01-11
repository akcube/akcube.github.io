"""
Link Processor Module - Handle wikilinks and related notes
Converts Obsidian wikilinks to Hugo-compatible markdown links
"""

import re
import inflection
from typing import Dict, Set, Tuple
from pathlib import Path


class LinkProcessor:
    """Process and convert links in markdown content"""

    def __init__(self, config: Dict):
        self.config = config
        self.enable_related = config['features'].get('enable_related_reading', True)

    def parameterize_title(self, title: str) -> str:
        """Convert note title to URL-safe slug"""
        return inflection.parameterize(title)

    def extract_wikilinks(self, content: str) -> Set[str]:
        """
        Extract all wikilinks from content

        Examples:
            [[Note Title]] -> "Note Title"
            [[Note Title|Display Text]] -> "Note Title"
            [[Folder/Note]] -> "Folder/Note"
        """
        # Pattern matches [[link]] and [[link|alias]]
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(pattern, content)
        return set(matches)

    def convert_wikilink(self, match: re.Match) -> str:
        """
        Convert a wikilink to Hugo-compatible markdown link

        [[Note Title]] -> [Note Title](/blog/note-title/)
        [[Note Title|Alias]] -> [Alias](/blog/note-title/)
        """
        full_match = match.group(0)

        # Extract link and optional alias
        inner = match.group(1)
        parts = inner.split('|')

        target = parts[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else target

        # Convert to URL slug
        slug = self.parameterize_title(target)

        # Generate Hugo link (no trailing slash for consistency with hugo-obsidian)
        hugo_link = f'[{alias}](/blog/{slug})'

        return hugo_link

    def process_wikilinks(self, content: str) -> Tuple[str, Set[str]]:
        """
        Process all wikilinks in content

        Returns:
            Tuple of (processed_content, set_of_referenced_notes)
        """
        referenced_notes = self.extract_wikilinks(content)

        # Convert wikilinks - matches [[link]] and [[link|alias]] but NOT ![[image]]
        pattern = r'(?<!!)\[\[([^\]]+)\]\]'
        processed_content = re.sub(pattern, self.convert_wikilink, content)

        return processed_content, referenced_notes

    def extract_image_links(self, content: str) -> Set[str]:
        """
        Extract image wikilinks from content

        ![[image.png]] -> "image.png"
        """
        pattern = r'!\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        return set(matches)

    def convert_image_link(self, match: re.Match, image_deps: Set[str]) -> str:
        """
        Convert image wikilink to Hugo-compatible markdown image

        ![[image.png]] -> ![image](/images/image.webp)
        """
        image_name = match.group(1)
        image_deps.add(image_name)

        # Get base name without extension
        basename = Path(image_name).stem

        # Convert to URL slug
        slug = self.parameterize_title(basename)

        # Reference .webp (Hugo render hook will handle fallback)
        return f'![{slug}](/images/{slug}.webp)'

    def process_images(self, content: str) -> Tuple[str, Set[str]]:
        """
        Process all image links in content

        Returns:
            Tuple of (processed_content, set_of_image_dependencies)
        """
        image_deps = set()

        # Convert image wikilinks
        pattern = r'!\[\[([^\]]+)\]\]'
        processed_content = re.sub(
            pattern,
            lambda m: self.convert_image_link(m, image_deps),
            content
        )

        return processed_content, image_deps

    def generate_related_section(self, frontmatter: Dict, note_slug: str, already_linked: Set[str] = None) -> str:
        """
        Generate Related Reading section from frontmatter

        Args:
            frontmatter: Note frontmatter dict
            note_slug: URL slug of current note (to avoid self-reference)
            already_linked: Set of note names already linked in content (to avoid duplicates)

        Returns:
            Markdown string for related section
        """
        if not self.enable_related:
            return ""

        related = frontmatter.get('related', [])
        if not related:
            return ""

        if already_linked is None:
            already_linked = set()

        # Filter out self-references, already-linked notes, and convert to links
        related_links = []
        for item in related:
            # Extract note name from wikilink format
            note_name = item.strip('[]').split('|')[0]
            slug = self.parameterize_title(note_name)

            # Skip self-references
            if slug == note_slug:
                continue

            # Skip notes already linked in content
            if note_name in already_linked:
                continue

            related_links.append(f"- [{note_name}](/blog/{slug})")

        if not related_links:
            return ""

        section = "\n\n---\n\n## Related Reading\n\n"
        section += "\n".join(related_links)
        section += "\n"

        return section


def main():
    """Test the link processor"""
    import yaml

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    processor = LinkProcessor(config)

    # Test content
    test_content = """
# Test Note

This is a reference to [[Another Note]] and also [[Complex Note Title|simpler alias]].

Here's an image: ![[test-image.png]]

And another note: [[Deep Dive into Algorithms]].
"""

    print("Original content:")
    print(test_content)
    print("\n" + "="*60 + "\n")

    # Process wikilinks
    processed, referenced = processor.process_wikilinks(test_content)
    print("After processing wikilinks:")
    print(processed)
    print(f"\nReferenced notes: {referenced}")
    print("\n" + "="*60 + "\n")

    # Process images
    processed, images = processor.process_images(processed)
    print("After processing images:")
    print(processed)
    print(f"\nImage dependencies: {images}")
    print("\n" + "="*60 + "\n")

    # Test related section
    frontmatter = {
        'title': 'Test Note',
        'related': [
            '[[Another Note]]',
            '[[Deep Dive into Algorithms]]',
            '[[Complex Note Title]]'
        ]
    }

    related_section = processor.generate_related_section(frontmatter, 'test-note')
    print("Generated related section:")
    print(related_section)


if __name__ == '__main__':
    main()
