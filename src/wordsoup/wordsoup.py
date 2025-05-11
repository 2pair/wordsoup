
from typing import List, Set

from wordsoup.dictionary import DictionaryTrie, Node


class WordSoup:
    """Turns the soup into solid words.

    Args:
        dictionary: The dictionary of valid words.
        letter_groups: The groups of valid letters for each position.
    """

    def __init__(
        self,
        dictionary: DictionaryTrie, 
        letter_groups: List[Set[str]]
    ):
        self.dictionary = dictionary
        self.letter_groups = letter_groups

    @staticmethod
    def _get_valid_paths(node: Node, next_letters: Set[str]) -> List[Node]:
        """Gets nodes for the given letters, if they exist.
        
        Args:
            node: The current node.
            next_letters: The set of candidate letters for the next node.
            
        Returns:
            The valid nodes for the given input data."""
        paths = []
        for letter in next_letters:
            if letter in node.keys():
                paths.append(node[letter])
        return paths

    def solidify(self) -> List[str]:
        """Turns the soup into concrete.
        
        Returns:
            The list of valid words.
        """
        # Seed with the root node.
        nodes: List[Node] = [self.dictionary.trie]
        for letter_group in self.letter_groups:
            new_nodes = []
            for node in nodes:
                new_nodes.extend(self._get_valid_paths(node, letter_group))
            nodes = new_nodes
        
        words = []
        for node in nodes:
            path = node.path_from_root()
            word = "".join(path)
            words.append(word)
        
        return words
