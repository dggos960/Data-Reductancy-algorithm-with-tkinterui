import os
import fnmatch
import pandas as pd
import mmap
import seaech_duplicate_files as sdf

def get_char_value_and_count(file_path, position):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                char_value = mmapped_file[position:position + 1].decode('utf-8', errors='ignore')
                return char_value, len(mmapped_file)
    except Exception as e:
        return f"An error occurred: {e}", 0

def group_files_by_char_count(file_paths, char_position):
    grouped_files = {}

    for file_path in file_paths:
        char_value, char_count = get_char_value_and_count(file_path, char_position)

        if char_count > 1:
            if char_count in grouped_files:
                grouped_files[char_count].append(file_path)
            else:
                grouped_files[char_count] = [file_path]

    return grouped_files

def get_text_and_csv_files_with_paths(folder_paths):
    results = []
    char_position = 5
    valid_extensions = ['.txt', '.csv', '.pix', '.js', '.cfg', '.file', '.rpm', '.zip', '.sh', '.bk', '.gz', '.sql', '.xls', '.xlsx', '.out', '.last', '.shx', '.prj', '.bak']


    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in valid_extensions):
                    file_path = os.path.join(root, file)
                    results.append(file_path)

    # Group files by character count
    grouped_files = group_files_by_char_count(results, char_position)

    # Filter out files with only one occurrence
    grouped_files = {count: paths for count, paths in grouped_files.items() if len(paths) > 1}

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(grouped_files.items(), columns=['Char Count', 'File Paths'])
    

    return df

    