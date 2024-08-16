import os


def list_directory_recursive_to_string(directory):
    """аналог ls -R"""
    result = []

    for root, dirs, files in os.walk(directory):
        result.append(f"{root}:\n")
        for file in files:
            result.append(f"  {file}\n")
        for dir in dirs:
            result.append(f"  {dir}/\n")
        result.append("\n")

    return "".join(result)
