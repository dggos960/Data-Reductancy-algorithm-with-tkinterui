import os
import hashlib

def hash_file(file_path):
    with open(file_path, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()

def find_duplicates_within_groups(file_groups):
    duplicates = []

    for group in file_groups:
        content_dict = {}

        for file_path in group:
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    file_hash = hash_file(file_path)

                    if file_hash in content_dict:
                        content_dict[file_hash].append(file_path)
                    else:
                        content_dict[file_hash] = [file_path]

        for paths in content_dict.values():
            if len(paths) > 1:
                duplicates.append(paths)

    return duplicates

