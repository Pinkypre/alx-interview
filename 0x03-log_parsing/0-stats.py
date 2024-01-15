import sys
import signal

def handle_interrupt(signal, frame):
    print_statistics()
    sys.exit(0)

def print_statistics():
    print(f"Total file size: {total_size}")
    for code in sorted(status_codes):
        print(f"{code}: {status_codes[code]}")

def process_line(line):
    parts = line.split()
    if len(parts) != 10 or parts[5] != '"GET' or not parts[9].isdigit():
        return False

    status_code = int(parts[8])
    file_size = int(parts[9])
    update_statistics(status_code, file_size)

def update_statistics(status_code, file_size):
    global total_size
    total_size += file_size

    if status_code in status_codes:
        status_codes[status_code] += 1
    else:
        status_codes[status_code] = 1

def main():
    global total_size
    global status_codes
    total_size = 0
    status_codes = {}

    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        for line_number, line in enumerate(sys.stdin, start=1):
            line = line.strip()
            if process_line(line) and line_number % 10 == 0:
                print_statistics()
    except KeyboardInterrupt:
        pass

    print_statistics()

if __name__ == "__main__":
    main()

