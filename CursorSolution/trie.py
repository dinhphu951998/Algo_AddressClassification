from rapidfuzz import process, fuzz
from rapidfuzz.distance import DamerauLevenshtein, Levenshtein

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.original_names = []  # List of original names for this normalized key

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._all_norm_names = set()  # Store all normalized names for fuzzy search
        self._norm_to_original = {}   # Map normalized name to original(s)

    def insert(self, normalized_name, original_name):
        node = self.root
        for char in normalized_name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.original_names.append(original_name)
        self._all_norm_names.add(normalized_name)
        if normalized_name not in self._norm_to_original:
            self._norm_to_original[normalized_name] = []
        self._norm_to_original[normalized_name].append(original_name)

    def search(self, normalized_name):
        """Return list of original names if exact match, else empty list."""
        node = self.root
        for char in normalized_name:
            if char not in node.children:
                return []
            node = node.children[char]
        if node.is_end:
            return node.original_names
        return []

    def starts_with(self, prefix):
        """Return all original names that start with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all(node)

    def _collect_all(self, node):
        result = []
        if node.is_end:
            result.extend(node.original_names)
        for child in node.children.values():
            result.extend(self._collect_all(child))
        return result

    def fuzzy_search(self, query, max_distance=2):
        qlen = len(query)
        filtered_keys = [k for k in self._all_norm_names if abs(len(k) - qlen) <= max_distance]
        results = process.extract(
                        query,
                        filtered_keys,
                        score_cutoff=90
                    )
        matches = []
        for match, distance, _ in results:
            matches.extend(self._norm_to_original[match])
        return matches

# Example usage
if __name__ == "__main__":
    trie = Trie()
    # Example: Insert normalized names and their originals
    trie.insert("thuan thanh", "Thuận Thành")
    trie.insert("can giuoc", "Cần Giuộc")
    trie.insert("long an", "Long An")
    trie.insert("ho chi minh", "Hồ Chí Minh")
    # print(trie.search("thuan thanh"))  # ['Thuận Thành']
    # print(trie.starts_with("thuan"))   # ['Thuận Thành']
    print(trie.fuzzy_search("hochiminh"))  # Should match ['Thuận Thành'] 