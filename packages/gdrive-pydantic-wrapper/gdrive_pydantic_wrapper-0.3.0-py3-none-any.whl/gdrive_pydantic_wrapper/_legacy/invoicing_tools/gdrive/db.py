import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from invoicing_tools.codec import ModelDecoder, ModelEncoder
from invoicing_tools.gdrive.models import GoogleDriveObject


class FolderDatabase:

    def __init__(self, db_file: Path):
        self.db_file = db_file
        if self.db_file.exists():
            with open(self.db_file, 'r') as json_file:
                self.db = json.load(json_file, cls=ModelDecoder)

    def get(self, path: str) -> GoogleDriveObject:
        return self.db.get(path)

    def find(self, path: str) -> List[GoogleDriveObject]:
        results = list()
        for key, folder in self.db.items():
            if path in key:
                results.append(folder)
        return results

    def update(self, folders: Dict[str, GoogleDriveObject]):
        with open(self.db_file, 'w') as json_file:
            json.dump(folders, json_file, cls=ModelEncoder)
        self.db = folders

    def exists(self) -> bool:
        return self.db_file.exists()

    @property
    def modified_on(self) -> datetime | None:
        if self.db_file.exists():
            modified = self.db_file.stat().st_mtime
            modified_on = datetime.fromtimestamp(modified)
            return modified_on
