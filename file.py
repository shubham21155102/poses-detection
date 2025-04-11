import os

def rename_files_in_order(folder_path):
    # Get all files in the folder (ignore directories)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()  # Optional: sort alphabetically or by current name

    for index, filename in enumerate(files, start=1):
        new_name = f"{index}.png"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f"Renamed '{filename}' to '{new_name}'")

# Example usage
folder_path = "dataset/train/Sitting"
rename_files_in_order(folder_path)