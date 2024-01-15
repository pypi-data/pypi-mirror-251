import re
from typing import List


def extract_author_names_from_latex_string(latex_string) -> List[str]:
    regex_matches = re.finditer(r'\\author', latex_string)
    author_names: List[str] = []
    for regex_match in regex_matches:
        author_start_index = regex_match.start()
        named_started = False
        curly_brace_depth = 0
        string_position = author_start_index
        author_name = ''
        while curly_brace_depth > 0 or named_started == False:
            character = latex_string[string_position]
            if character == '{':
                curly_brace_depth += 1
                named_started = True
            if character == '}':
                curly_brace_depth -= 1
            if named_started:
                author_name += character
            string_position += 1
        author_name = author_name[1:-1]  # Remove outer curly braces.
        assert ',' not in author_name
        author_names.append(author_name)
    return author_names
