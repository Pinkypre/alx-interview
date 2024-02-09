#!/usr/bin/python3
import sys
from collections import defaultdict

def compute_metrics(lines):
    total_file_size = 0
    status_code_count = defaultdict(int)
    for line in lines:
        parts = line.split()
        if len(parts) == 10:
            try:
                file_size = int(parts[9])
                total_file_size += file_size
                status_code = int(parts[8])
                if status_code in (200, 301, 400, 401, 403, 404, 405, 500):
                    status_code_count[status_code] += 1
            except (ValueError, IndexError):
                pass

    return total_file_size, status_code_count

def print_statistics(total_file_size, status_code_count):
    print("Total file size:", total_file_size)
    for status_code in sorted(status_code_count.keys()):
        print(f"{status_code}: {status_code_count[status_code]}")

def main():
    lines = []
    try:
        for line in sys.stdin:
            lines.append(line.strip())
            if len(lines) % 10 == 0:
                total_file_size, status_code_count = compute_metrics(lines)
                print_statistics(total_file_size, status_code_count)
                lines = []
    except KeyboardInterrupt:
        total_file_size, status_code_count = compute_metrics(lines)
        print_statistics(total_file_size, status_code_count)

if __name__ == "__main__":
    main()

