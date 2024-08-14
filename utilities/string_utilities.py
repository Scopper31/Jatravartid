import re
from system_utilities import *


def evolution_of_development(a, b):
    try:
        return "\nA piece of code:\n".join([a, b])
    except Exception as e:
        print(f"Error in utilities.string_utilities/evolution_of_developmentt: {e}")
        add_to_log("utilities.string_utilities/evolution_of_development", e)


def extract_blocks(text, block_start, block_end):
    try:
        block_starts = [m.start() for m in re.finditer(block_start, text)]
        block_ends = [m.start() for m in re.finditer(block_end, text)]

        extracted_texts = []
        for start, end in zip(block_starts, block_ends):
            extracted_texts.append(text[start + len(block_start) : end].strip())
    except Exception as e:
        print(f"Error in utilities.string_utilities/extract_blocks: {e}")
        add_to_log("utilities.string_utilities/extract_blocks", e)
        return []
    return extracted_texts
