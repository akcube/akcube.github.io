"""
Tag Converter Module - Convert hierarchical Obsidian tags to Hugo taxonomies
Handles domain/type/status tag structure and maps to Hugo categories/topics/series
"""

from typing import Dict, List, Set
import inflection


class TagConverter:
    """Converts hierarchical tags to Hugo-compatible taxonomies"""

    def __init__(self, config: Dict):
        self.domain_mappings = config.get('domain_mappings', {})
        self.type_mappings = config.get('type_mappings', {})

    def parse_hierarchical_tag(self, tag: str) -> Dict[str, str]:
        """
        Parse a hierarchical tag into components

        Example:
            "domain/cs/algorithms/analysis" ->
            {
                'root': 'domain',
                'domain': 'cs',
                'subdomain': 'algorithms',
                'leaf': 'analysis',
                'full_path': 'domain/cs/algorithms',
            }
        """
        parts = tag.split('/')

        if len(parts) < 2:
            return {'root': parts[0], 'leaf': parts[0]}

        result = {
            'root': parts[0],
            'full_tag': tag,
        }

        if parts[0] == 'domain':
            if len(parts) >= 2:
                result['domain'] = parts[1]
            if len(parts) >= 3:
                result['subdomain'] = parts[2]
            if len(parts) >= 4:
                result['subsubdomain'] = parts[3]
            result['leaf'] = parts[-1]
            # For matching in config, use all but the last part
            result['full_path'] = '/'.join(parts[:-1]) if len(parts) > 2 else tag

        elif parts[0] == 'type':
            result['type'] = parts[1] if len(parts) > 1 else None
            result['leaf'] = parts[-1]

        elif parts[0] == 'status':
            result['status'] = parts[1] if len(parts) > 1 else None
            result['leaf'] = parts[-1]

        else:
            result['leaf'] = parts[-1]

        return result

    def tag_to_topic(self, tag: str) -> str:
        """
        Convert a tag to a Hugo-compatible topic string
        For generic terms, includes parent context for clarity

        Examples:
            "domain/cs/algorithms/analysis" -> "Algorithm-Analysis"
            "domain/cs/algorithms/complexity" -> "Algorithm-Complexity"
            "domain/math/probability-statistics" -> "Probability-Statistics"
            "domain/cs/systems/databases" -> "Databases"
        """
        parsed = self.parse_hierarchical_tag(tag)
        leaf = parsed.get('leaf', tag)
        subdomain = parsed.get('subdomain', '')
        domain = parsed.get('domain', '')

        # Generic terms that need parent context
        generic_terms = {
            'analysis', 'complexity', 'theory', 'general',
            'miscellaneous', 'optimization', 'design'
        }

        # Check if leaf is generic and needs context
        if leaf.lower() in generic_terms:
            if subdomain and subdomain.lower() != leaf.lower():
                # Case 1: domain/cs/algorithms/analysis -> "algorithm-analysis"
                # Use subdomain as context
                parent_singular = inflection.singularize(subdomain)
                combined = f"{parent_singular}-{leaf}"
                topic = inflection.parameterize(combined)
            elif domain:
                # Case 2: domain/math/analysis -> "mathematical-analysis"
                # Use domain as context when subdomain == leaf
                parent_singular = inflection.singularize(domain)
                combined = f"{parent_singular}-{leaf}"
                topic = inflection.parameterize(combined)
            else:
                # Fallback: just use the leaf
                topic = inflection.parameterize(leaf)
        else:
            # Use just the leaf for specific terms
            topic = inflection.parameterize(leaf)

        # Titlecase each word after splitting on hyphens
        words = topic.split('-')
        titlecased = '-'.join(word.capitalize() for word in words)
        return titlecased

    def get_categories_from_tag(self, tag: str) -> List[str]:
        """
        Get Hugo categories from a hierarchical domain tag

        Example:
            "domain/cs/algorithms/analysis" ->
            ["Computer Science", "Algorithms"]
        """
        parsed = self.parse_hierarchical_tag(tag)

        if parsed.get('root') != 'domain':
            return []

        # Try progressively shorter paths to find a mapping
        tag_variants = []
        parts = tag.split('/')

        # Try full path, then remove leaf, then remove sub-subdomain, etc.
        for i in range(len(parts), 1, -1):
            variant = '/'.join(parts[:i])
            tag_variants.append(variant)

        # Find first matching mapping
        for variant in tag_variants:
            if variant in self.domain_mappings:
                mapping = self.domain_mappings[variant]
                category = mapping.get('category', '')
                subcategories = mapping.get('subcategories', [])

                categories = []
                if category:
                    categories.append(category)
                categories.extend(subcategories)

                return categories

        # Fallback: use domain and subdomain as categories
        categories = []
        if 'domain' in parsed:
            categories.append(parsed['domain'].upper())
        if 'subdomain' in parsed:
            categories.append(inflection.titleize(parsed['subdomain']))

        return categories

    def get_series_from_tag(self, tag: str) -> str | None:
        """
        Get Hugo series from a type tag

        Example:
            "type/zettelkasten" -> "Zettelkasten"
        """
        if tag in self.type_mappings:
            return self.type_mappings[tag]

        parsed = self.parse_hierarchical_tag(tag)
        if parsed.get('root') == 'type' and parsed.get('type'):
            return inflection.titleize(parsed['type'])

        return None

    def convert_tags(self, tags: Set[str]) -> Dict[str, List[str]]:
        """
        Convert Obsidian tags to Hugo taxonomies

        Args:
            tags: Set of hierarchical tags from frontmatter

        Returns:
            Dictionary with 'topics', 'categories', and 'series' lists

        Example:
            Input: {
                "domain/cs/algorithms/analysis",
                "domain/cs/algorithms/complexity",
                "type/zettelkasten",
                "status/evergreen"
            }

            Output: {
                "topics": ["algorithm-analysis", "complexity-theory"],
                "categories": ["Computer Science", "Algorithms"],
                "series": ["Zettelkasten"]
            }
        """
        topics = set()
        categories = set()
        series = set()

        for tag in tags:
            parsed = self.parse_hierarchical_tag(tag)
            root = parsed.get('root', '')

            if root == 'domain':
                # Extract topic from leaf
                topics.add(self.tag_to_topic(tag))

                # Extract categories
                cats = self.get_categories_from_tag(tag)
                categories.update(cats)

            elif root == 'type':
                # Extract series
                ser = self.get_series_from_tag(tag)
                if ser:
                    series.add(ser)

            elif root == 'status':
                # Status tags are not published (used only for filtering)
                pass

            else:
                # Unknown tag structure - add as topic
                topics.add(self.tag_to_topic(tag))

        return {
            'topics': sorted(list(topics)),
            'categories': sorted(list(categories)),
            'series': sorted(list(series))
        }

    def filter_tags_for_frontmatter(self, tags: Set[str]) -> List[str]:
        """
        Filter tags for frontmatter output - remove status and type tags

        Args:
            tags: Set of all tags

        Returns:
            List of tags suitable for frontmatter (domain tags only)
        """
        filtered = []
        for tag in tags:
            parsed = self.parse_hierarchical_tag(tag)
            root = parsed.get('root', '')

            # Only include domain tags in frontmatter
            if root == 'domain':
                filtered.append(tag)

        return sorted(filtered)

    def enhance_frontmatter(self, frontmatter: Dict, tags: Set[str]) -> Dict:
        """
        Add Hugo taxonomies to frontmatter while preserving original

        Args:
            frontmatter: Original frontmatter dictionary
            tags: Set of tags from frontmatter

        Returns:
            Enhanced frontmatter with Hugo taxonomies
        """
        # Convert tags
        taxonomies = self.convert_tags(tags)

        # Create new frontmatter (preserve original)
        enhanced = frontmatter.copy()

        # Remove 'related' - it's rendered as links in content via generate_related_section
        enhanced.pop('related', None)

        # Remove 'tags' - we'll add our own converted tags
        enhanced.pop('tags', None)

        # Add Hugo taxonomies
        if taxonomies['topics']:
            enhanced['topics'] = taxonomies['topics']
        if taxonomies['categories']:
            enhanced['categories'] = taxonomies['categories']
        if taxonomies['series']:
            enhanced['series'] = taxonomies['series'][0]  # Hugo expects single series

        return enhanced


def main():
    """Test the tag converter"""
    import yaml

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    converter = TagConverter(config)

    # Test tags
    test_tags = {
        "domain/cs/algorithms/analysis",
        "domain/cs/algorithms/complexity",
        "type/zettelkasten",
        "status/evergreen"
    }

    print("Input tags:")
    for tag in test_tags:
        print(f"  - {tag}")

    print("\nParsed structure:")
    for tag in test_tags:
        parsed = converter.parse_hierarchical_tag(tag)
        print(f"  {tag}:")
        for k, v in parsed.items():
            print(f"    {k}: {v}")

    print("\nConverted taxonomies:")
    taxonomies = converter.convert_tags(test_tags)
    print(yaml.dump(taxonomies, default_flow_style=False))

    # Test more examples
    print("\n\nMore examples:")
    examples = [
        {"domain/finance/quantitative", "type/zettelkasten", "status/evergreen"},
        {"domain/math/probability-statistics", "type/zettelkasten", "status/seed"},
        {"domain/science/bioinformatics", "type/literature-note", "status/evergreen"},
    ]

    for tags in examples:
        print(f"\nInput: {tags}")
        result = converter.convert_tags(tags)
        print(f"Output: {result}")


if __name__ == '__main__':
    main()
