def get_folder_id_by_name(folders, folder_name):
    for folder in folders:
        if folder.name.lower() == folder_name.lower():
            return folder.folder_id

        subfolders = folder.folders
        if subfolders is not None and len(subfolders) > 0:
            folder_id = get_folder_id_by_name(subfolders, folder_name)
            if folder_id is not None:
                return folder_id