import sys
from pathlib import Path


def parse_log_line(line: str) -> dict:
    """
    Parse a single log line into its components.

    :param line: A single line from the log file.
    :return: A dictionary with keys: date, time, level, message.
    """
    # Split into 4 parts to keep the full message intact
    parts = line.split(" ", 3)

    if len(parts) < 4:
        raise ValueError("Log line does not have enough parts")

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3].strip(),
    }


def load_logs(file_path: str) -> list:
    """
    Load log entries from a file and parse them into a list of dictionaries.

    :param file_path: Path to the log file.
    :return: List of parsed log entries.
    """
    path = Path(file_path)
    logs = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    logs.append(parse_log_line(line))
                except ValueError:
                    continue  # Skip malformed lines
            return logs
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Filter log entries by their level.

    :param logs: List of log entries.
    :param level: Log level to filter by (e.g., "ERROR", "INFO").
    :return: List of log entries matching the specified level.
    """
    # Functional style filtering by log level
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Count the number of log entries for each log level.

    :param logs: List of log entries.
    :return: Dictionary with log levels as keys and their counts as values.
    """
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: dict) -> str:
    """
    Display the count of log entries for each level.

    :param counts: Dictionary with log levels and their counts.
    :return: Formatted table as string.
    """
    if not counts:
        return "No log entries found."

    level_width = max(len("Log Level"), max(len(level) for level in counts))
    count_width = max(len("Count"), max(len(str(c)) for c in counts.values()))

    header = f"{'Log Level':<{level_width}} | {'Count':<{count_width}}"
    separator = "-" * len(header)

    lines = [header, separator]

    for level in sorted(counts):
        lines.append(f"{level:<{level_width}} | {counts[level]:<{count_width}}")

    return "\n".join(lines)


def main():
    """
    Main function to load logs, filter by level, and display counts.

    Usage: python task_3.py <logfile_path> [<log_level>]
    """
    if len(sys.argv) < 2:
        print("Error: No input path to logfile.")
        return

    path = sys.argv[1]

    level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    logs = load_logs(path)
    if not logs:
        return

    counts = count_logs_by_level(logs)
    print(display_log_counts(counts))

    if level:
        filtered_logs = filter_logs_by_level(logs, level)
        print(f'\nLogs with level "{level}":')
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} {log['level']} - {log['message']}")


if __name__ == "__main__":
    main()
