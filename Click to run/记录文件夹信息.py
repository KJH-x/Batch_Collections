import csv
import os
import zlib
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Literal, Optional, Tuple

from tqdm import tqdm


def compute_crc32(file_path) -> Optional[int]:
    """Compute the CRC32 checksum of a file."""
    crc = 0
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                crc = zlib.crc32(chunk, crc)
    except (OSError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    return crc & 0xFFFFFFFF  # Ensure it's a 32-bit unsigned value


def process_file(file_info) -> Tuple[Any, int, str] | Tuple[Any, Literal['Error'], Literal['Error']]:
    """Process a single file: compute size and CRC32."""
    relative_path, full_path = file_info
    try:
        size = os.path.getsize(full_path)
        crc32 = compute_crc32(full_path)
        crc32_formatted = f"0x{crc32:08X}" if crc32 is not None else "Error"
        return (relative_path, size, crc32_formatted)
    except Exception as e:
        print(f"Error processing file {full_path}: {e}")
        return (relative_path, "Error", "Error")


def walk_directory_and_generate_csv(input_dir, output_csv, num_threads=32):
    """Walk through the directory, compute file sizes and CRC32 using threads, and save to a CSV file."""
    file_list = []

    # Collect all files with their relative and full paths
    print(f"[Info] Building file list")
    for root, _, files in os.walk(input_dir):
        for file in files:
            full_path = os.path.join(str(root), str(file))
            relative_path = os.path.relpath(full_path, start=input_dir).replace("\\", "/")
            file_list.append((relative_path, full_path))

    results = []
    # Process files in parallel
    print(f"[Info] Calculating Hashes")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(process_file, file_info): file_info for file_info in file_list}
        for future in tqdm(as_completed(futures), total=len(futures)):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error in thread execution: {e}")

    print(f"[Info] Collating Results")

    # Sort results alphabetically by relative path
    results.sort(key=lambda x: x[0])

    # Calculate directory sizes
    dir_sizes = defaultdict(int)
    for relative_path, size, _ in results:
        if isinstance(size, int):  # Exclude errors
            dir_path = os.path.dirname(relative_path)
            while dir_path:  # Add size to all parent directories
                dir_sizes[dir_path] += size
                dir_path = os.path.dirname(dir_path)
            dir_sizes[""] += size  # Root directory

    # Write results to CSV
    print(f"[Info] Writing Results")
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Path", "Size (bytes)", "Type"])

        # Write file entries
        for relative_path, size, crc32 in results:
            writer.writerow([relative_path, size, crc32])

        # Write directory summaries
        for dir_path in sorted(dir_sizes):
            writer.writerow([dir_path or ".", dir_sizes[dir_path], "[DIR]"])


# Example usage
input_directory = os.path.join(input("Enter DIR path: "))
output_csv_file = os.path.join(os.path.dirname(input_directory),
                               f"{os.path.basename(input_directory)}.dir_info.csv")
print(f"[Info] Data will write to: {output_csv_file}")
walk_directory_and_generate_csv(input_directory, output_csv_file)
