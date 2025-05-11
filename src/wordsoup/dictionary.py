from collections import UserDict, deque
from collections.abc import Sequence
from pathlib import Path
from typing import List, Optional


class Node(UserDict):
    def __init__(
            self, 
            letter: Optional[str], 
            previous: Optional["Node"]=None, 
            *args, 
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.letter = letter
        self._previous = previous

    def __str__(self) -> str:
        if not self.letter:
            if not isinstance(self, Trie):
                print("WARN: non-root node is not assigned a letter")
            return ""
        return self.letter

    @property
    def previous(self) -> "Node":
        return self._previous
    
    def path_from_root(self) -> List["Node"]:
        """Traverses to the root node and returns the path.
        
        Returns:
            List of nodes from the root node to this node,
            excluding the root and including this node.
        """
        if isinstance(self.previous, Trie):
            return [self.letter]
        return self.previous.path_from_root() + [self.letter]


class Trie(Node):
    """The root node."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, letter=None, previous=None, **kwargs)


class DictionaryTrie:
    """A browsable data structure containing all words from the given 
    word list file. The file should have one word per line. 

     Args:
        word_list_file: The path to the word list
        num_letters: The number of letters we care about. Words shorter or
            longer than this will be discarded.
    """

    def __init__(self, word_list_file: Path, num_letters: int):
        self.word_list_file = word_list_file
        self.num_letters = num_letters
        self.trie = Trie()
        self.create_trie()

    def _add_to_node(self, node: Node, sequence: Sequence):
        """Adds the letters in the sequence to the data structure."""
        letters = deque(sequence)
        front = letters.popleft()
        next_node = node.setdefault(front, Node(front, previous=node))
        if letters:
            self._add_to_node(next_node, letters)

    def create_trie(self):
        """Create a trie from the words in the file."""
        self.words_trie = dict()
        with self.word_list_file.open(mode="r") as word_list:
            for word in word_list:
                word = word.strip().lower()
                if len(word) != self.num_letters:
                    continue
                self._add_to_node(self.trie, word)
