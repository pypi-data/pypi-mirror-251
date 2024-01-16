from typing import List, Dict, Any

from pydantic import ValidationError

from invoicing_tools.gdrive.models import GoogleDriveObject


def build_folder_objects(folders: List[Dict[str, Any]], ) -> Dict[str, GoogleDriveObject]:
    folder_dict = dict()
    for folder in folders:
        try:
            folder_dict[folder["id"]] = GoogleDriveObject(**folder)
        except ValidationError as e:
            print(f'Ignored forlder {folder["name"]}')
            # raise e
    return folder_dict


def get_ancestry(folder_dict: Dict[str, GoogleDriveObject], folder: GoogleDriveObject | None):
    ancestry = list()
    if folder is None:
        ancestry.append('')
        return ancestry
    else:
        ancestry.append(folder.name)
    grand_parent_id = folder.parents[0]
    grand_parent = folder_dict.get(grand_parent_id)
    prev = get_ancestry(folder_dict, grand_parent)
    ancestry.extend(prev)
    return ancestry


def build_fullpath_dict(folder_dict: Dict[str, GoogleDriveObject]) -> Dict[str, GoogleDriveObject]:
    new_folder_dict = dict()
    for idx, folder in folder_dict.items():
        parent_id = folder.parents[0]
        parent = folder_dict.get(parent_id)
        folder.parent_folder = parent
        lineage = get_ancestry(folder_dict, folder)
        lineage.reverse()
        key = "/".join(lineage)
        folder.full_path = key
        new_folder_dict[key] = folder
    return new_folder_dict


def build_folder_db(folders: List[Dict[str, Any]]):
    folders_obj_dict = build_folder_objects(folders)
    fullpath_dict = build_fullpath_dict(folders_obj_dict)
    return fullpath_dict
