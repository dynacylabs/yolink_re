#!/bin/python3
import sys

def find_segment(file1, file2, segment_size):
    with open(file1, 'rb') as f1:
        file1_data = f1.read()

    with open(file2, 'rb') as f2:
        file2_data = f2.read()

    match_found = False
    offset = 0
    while offset <= len(file1_data) - segment_size:
        segment = file1_data[offset:offset + segment_size]

        # Skip the check if the segment consists entirely of zero bytes
        if all(byte == 0 for byte in segment):
            offset += 1
            continue

        if segment in file2_data:
            segment_hex = segment.hex()
            print(f"Found segment at offset {offset}: {segment_hex}")
            match_found = True
            offset += segment_size  # Move to the end of the current segment
        else:
            offset += 1  # Move to the next byte

    if not match_found:
        print("No matching segments found in file2.bin.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py file1.bin file2.bin segment_size")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    try:
        segment_size = int(sys.argv[3])
    except ValueError:
        print("Segment size must be an integer.")
        sys.exit(1)

    if segment_size <= 0:
        print("Segment size must be greater than 0.")
        sys.exit(1)

    find_segment(file1, file2, segment_size)
