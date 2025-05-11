from collections.abc import Callable
from pathlib import Path
from typing import List, Optional, Set

from wordsoup.dictionary import DictionaryTrie
from wordsoup.wordsoup import WordSoup


# How many words to print on each line of the output
WORDS_PER_LINE = 10


def input_prompt(question: str, validator: Callable[[str], bool], default: Optional[str]=None) -> str:
    """Ask the user a question and collect their response.
    
    Args:
        question: What we are asking the user.
        validator: A callable to ensure the input meets some criteria. The callable
          should take a single string argument and should return a boolean.
        default: An optional default value. This is not validated before being returned.
        
    Returns:
      the user's input.
    """
    prompt = question
    if default:
        prompt += f"(default: {default})"
    prompt += "  "
    while True:
        user_input = input(prompt)
        if not user_input and default:
            print("using default value.")
            return default
        elif validator(user_input):
            return user_input
        else:
            print(f"Input was invalid.")


if __name__ == "__main__":
    try:
        print("Welcome to the Mt. Holly word distiller!")
        print("This program will find words of a given length, using the specified set of letters.")
        print("Letters should be supplied as a contiguous string.")
        print("Example: Given three sets of letters: abc def ghi, the word beg will be returned.\n")

        dictionary_file = input_prompt(
            question="Input the path to a dictionary file to use. File should have one word per line.",
            validator=lambda path: Path(path).is_file(),
            default="/usr/share/dict/words",
        )
        dictionary_file = Path(dictionary_file)
        
        word_length = input_prompt(
            question="How long will the words be?",
            validator=lambda number: number.isdigit(),
        )
        word_length = int(word_length)

        letter_groups: List[Set[str]] = []
        for i in range(word_length):
            letter_group = input_prompt(
                question=f"Enter letter group {i + 1}.",
                validator=lambda group: group.isalpha() and len(group) == len(set(group))
            )
            letter_groups.append(set(letter_group))

        dictionary = DictionaryTrie(dictionary_file, word_length)
        word_soup = WordSoup(dictionary, letter_groups)
        words = word_soup.solidify()

        print(f"{len(words)} valid words:")
        index = 0
        if words:
            for word in words:
                if index < WORDS_PER_LINE:
                    end = "  "
                    index += 1
                else:
                    index = 0
                    end = "\n"
                print(word, end=end)
        else:
            print("None!?")
    except KeyboardInterrupt:
        print("Ending the day early, Baron Reddington?")
