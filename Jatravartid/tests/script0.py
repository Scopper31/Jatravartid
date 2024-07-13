import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import shutil
import heapq
import zlib
import struct

# Developer 1 (GUI and Basic Archiving)

def select_files():
    """Opens a file selection dialog and returns a list of selected files."""
    global selected_files
    selected_files = filedialog.askopenfilenames(
        initialdir=".", title="Select Files to Archive"
    )
    status_label.config(text=f"Selected {len(selected_files)} files")

def select_output_dir():
    """Opens a directory selection dialog and returns the selected directory."""
    global output_dir
    output_dir = filedialog.askdirectory(
        initialdir=".", title="Select Output Directory"
    )
    status_label.config(text=f"Output directory: {output_dir}")

def archive_files():
    """Archives the selected files to the chosen output directory."""
    if not selected_files or not output_dir:
        status_label.config(text="Please select files and output directory.")
        return

    # Update progress bar
    progress_bar['maximum'] = len(selected_files)
    progress_bar['value'] = 0

    for i, file in enumerate(selected_files):
        # Get the filename without the path
        filename = os.path.basename(file)
        # Create the archive file path
        output_dir_tmp = str(output_dir)
        filename_tmp = str(filename)
        archive_path = os.path.join(output_dir_tmp, filename_tmp)
        # Copy the file to the archive directory
        shutil.copy2(file, archive_path)
        # Update the progress bar
        progress_bar['value'] = i + 1
        # Update the status message
        status_label.config(text=f"Archiving {filename}...")
        # Update the window
        window.update()

    # Set progress bar to 100% and update status message
    progress_bar['value'] = progress_bar['maximum']
    status_label.config(text="Archiving complete.")

# Create main window
window = tk.Tk()
window.title("File Archiver")

# Create file selection button
select_button = tk.Button(window, text="Select Files", command=select_files)
select_button.pack(pady=10)

# Create output directory selection button
output_button = tk.Button(window, text="Select Output Directory", command=select_output_dir)
output_button.pack(pady=10)

# Create archive button
archive_button = tk.Button(window, text="Archive", command=archive_files)
archive_button.pack(pady=10)

# Create progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Create status label
status_label = tk.Label(window, text="")
status_label.pack()

# Initialize global variables
selected_files = []
output_dir = None

# Start the main event loop
window.mainloop()

# Developer 2 (Compression Algorithms)

# Huffman Coding Implementation

def build_frequency_table(data):
    """
    Builds a frequency table from the input data.
    """
    frequency_table = {}
    for char in data:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

def build_huffman_tree(frequency_table):
    """
    Builds a Huffman tree from the frequency table.
    """
    heap = [(frequency, char) for char, frequency in frequency_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        freq1, char1 = heapq.heappop(heap)
        freq2, char2 = heapq.heappop(heap)
        heapq.heappush(heap, (freq1 + freq2, (char1, char2)))

    return heap[0][1]

def generate_huffman_codes(tree):
    """
    Generates Huffman codes for each character in the tree.
    """
    codes = {}
    def traverse(node, code=''):
        if isinstance(node, str):
            codes[node] = code
        else:
            left, right = node
            traverse(left, code + '0')
            traverse(right, code + '1')
    traverse(tree)
    return codes

def huffman_compress(data):
    """
    Compresses the input data using Huffman coding.
    """
    frequency_table = build_frequency_table(data)
    tree = build_huffman_tree(frequency_table)
    codes = generate_huffman_codes(tree)
    compressed_data = ''.join([codes[char] for char in data])
    return compressed_data, codes

def huffman_decompress(compressed_data, codes):
    """
    Decompresses the compressed data using Huffman codes.
    """
    decompressed_data = ''
    current_code = ''
    for bit in compressed_data:
        current_code += bit
        if current_code in codes:
            decompressed_data += codes[current_code]
            current_code = ''
    return decompressed_data

# RLE Implementation

def run_length_encode(data):
    """
    Encodes the input data using Run-Length Encoding.
    """
    encoded_data = ''
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data += str(count) + data[i - 1]
            count = 1
    encoded_data += str(count) + data[-1]
    return encoded_data

def run_length_decode(encoded_data):
    """
    Decodes the encoded data using Run-Length Encoding.
    """
    decoded_data = ''
    i = 0
    while i < len(encoded_data):
        count = ''
        while encoded_data[i].isdigit():
            count += encoded_data[i]
            i += 1
        decoded_data += encoded_data[i] * int(count)
        i += 1
    return decoded_data

# Developer 3 (File Handling)

def read_file_data(file_path):
    """Reads data from a file and returns its contents.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file contents.
    """

    try:
        with open(file_path, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_compressed_data(data, archive_path, metadata):
    """Writes compressed data and metadata to an archive file.

    Args:
        data (bytes): The data to compress and write.
        archive_path (str): The path to the archive file.
        metadata (dict): A dictionary containing metadata.
    """

    try:
        # Create the archive directory if it doesn't exist
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)

        # Compress the data using gzip
        with gzip.open(archive_path, 'wb') as f:
            f.write(data)

        # Write metadata to a separate file within the archive
        metadata_path = os.path.splitext(archive_path)[0] + "_metadata.json"
        with open(metadata_path, 'w') as f:
            # Implement your metadata serialization logic here
            # Example: using JSON
            import json
            json.dump(metadata, f)
    except Exception as e:
        print(f"Error writing compressed data: {e}")

# Developer 4 (GUI Integration and Error Handling)

# Define the archive file structure
ARCHIVE_HEADER_FORMAT = "!4sI"  # Format: magic (4 bytes), number of files (4 bytes)
MAGIC_NUMBER = b"ARCH"

# Function to read the archive file
def read_archive(archive_file_path):
    """Reads an archive file and extracts its contents.

    Args:
        archive_file_path (str): Path to the archive file.

    Returns:
        dict: A dictionary containing extracted data, keyed by file names.
    """

    extracted_data = {}
    with open(archive_file_path, "rb") as archive_file:
        # Read the header
        magic, num_files = struct.unpack(ARCHIVE_HEADER_FORMAT, archive_file.read(8))
        if magic != MAGIC_NUMBER:
            raise ValueError("Invalid archive file.")

        # Read each file
        for _ in range(num_files):
            # Read file metadata
            file_name_length = int.from_bytes(archive_file.read(4), "big")
            file_name = archive_file.read(file_name_length).decode("utf-8")
            compressed_size = int.from_bytes(archive_file.read(4), "big")

            # Read and decompress file data
            compressed_data = archive_file.read(compressed_size)
            decompressed_data = zlib.decompress(compressed_data)

            # Store extracted data
            extracted_data[file_name] = decompressed_data

    return extracted_data

# Function to write compressed data and metadata to the archive file
def write_archive(archive_file_path, files_to_archive):
    """Writes compressed data and metadata of files to an archive file.

    Args:
        archive_file_path (str): Path to the archive file.
        files_to_archive (dict): A dictionary where keys are file names and values are file contents.
    """

    with open(archive_file_path, "wb") as archive_file:
        # Write the header
        archive_file.write(struct.pack(ARCHIVE_HEADER_FORMAT, MAGIC_NUMBER, len(files_to_archive)))

        # Write each file
        for file_name, file_data in files_to_archive.items():
            # Write file metadata
            file_name_bytes = file_name.encode("utf-8")
            archive_file.write(struct.pack("!I", len(file_name_bytes)))
            archive_file.write(file_name_bytes)

            # Compress and write file data
            compressed_data = zlib.compress(file_data)
            archive_file.write(struct.pack("!I", len(compressed_data)))
            archive_file.write(compressed_data)

# Example usage
if __name__ == "__main__":
    # Create files to archive
    files = {
        "file1.txt": b"This is file 1 content.",
        "file2.txt": b"This is file 2 content.",
    }

    # Write files to archive
    write_archive("my_archive.arch", files)

    # Read and extract files from archive
    extracted_files = read_archive("my_archive.arch")

    # Print extracted files
    for file_name, file_data in extracted_files.items():
        print(f"File: {file_name}")
        print(f"Content: {file_data.decode('utf-8')}")

# PACKAGES tkinter ttk filedialog os shutil heapq zlib struct
