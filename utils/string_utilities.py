import re


def evolution_of_development(a, b):
    return '\nA piece of code:\n'.join([a, b])


def extract_blocks(text, block_start, block_end):
    block_starts = [m.start() for m in re.finditer(block_start, text)]
    block_ends = [m.start() for m in re.finditer(block_end, text)]

    extracted_texts = []
    for start, end in zip(block_starts, block_ends):
        extracted_texts.append(text[start + len(block_start):end].strip())
    return extracted_texts
