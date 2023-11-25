# pylint: disable-all

import pandas as pd
import re

def parse_log_file(log_file_path):
    # Patterns to identify the data in the log
    section_start_pattern = r'----------------------------------'
    section_end_pattern = r'----------------------------------'
    data_pattern = r'\|\s+(.*?)\s+\|\s+(.*?)\s+\|'

    # List to store all rows of data
    all_stats = []
    current_stats = {}

    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    # Flag to indicate we are in the stats section
    in_stats_section = False

    # Process each line in the log file
    for line in lines:
        if re.match(section_start_pattern, line) and not in_stats_section:
            in_stats_section = True
            continue
        elif re.match(section_end_pattern, line) and in_stats_section:
            in_stats_section = False
            # Add the current stats to all_stats and reset current_stats
            if current_stats:
                all_stats.append(current_stats)
                current_stats = {}
            continue

        if in_stats_section and re.match(data_pattern, line):
            key, value = re.match(data_pattern, line).groups()
            current_stats[key.strip()] = value.strip()

    # Convert the accumulated data into a pandas DataFrame
    df = pd.DataFrame(all_stats)

    return df


