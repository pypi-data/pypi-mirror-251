from typing import List, Optional

from pydantic import BaseModel, Field


class GoogleDriveObject(BaseModel):
    kind: str
    mime_type: str = Field(alias='mimeType')
    parents: List[str]
    id: str
    name: str
    parent_folder: Optional['GoogleDriveObject']
    full_path: Optional[str]

    @property
    def is_folder(self):
        return self.mime_type == 'application/vnd.google-apps.folder'

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


