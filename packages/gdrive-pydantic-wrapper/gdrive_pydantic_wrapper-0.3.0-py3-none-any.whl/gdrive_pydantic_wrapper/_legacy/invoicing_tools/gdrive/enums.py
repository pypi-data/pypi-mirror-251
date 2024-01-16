from enum import Enum


class GoogleMimeTypes(str, Enum):
    AUDIO = 'application/vnd.google-apps.audio'
    GOOGLE_DOCS = 'application/vnd.google-apps.document'
    THIRD_PARTY_SHORTCUT = 'application/vnd.google-apps.drive-sdk'
    GOOGLE_DRAWINGS = 'application/vnd.google-apps.drawing'
    GOOGLE_DRIVE_FILE = 'application/vnd.google-apps.file'
    GOOGLE_DRIVE_FOLDER = 'application/vnd.google-apps.folder'
    GOOGLE_FORMS = 'application/vnd.google-apps.form'
    GOOGLE_FUSION_TABLES = 'application/vnd.google-apps.fusiontable'
    GOOGLE_JAMBOARD = 'application/vnd.google-apps.jam'
    GOOGLE_MY_MAPS = 'application/vnd.google-apps.map'
    GOOGLE_PHOTOS = 'application/vnd.google-apps.photo'
    GOOGLE_SLIDES = 'application/vnd.google-apps.presentation'
    GOOGLE_APPS_SCRIPT = 'application/vnd.google-apps.script'
    SHORTCUT = 'application/vnd.google-apps.shortcut'
    GOOGLE_SITES = 'application/vnd.google-apps.site'
    GOOGLE_SHEETS = 'application/vnd.google-apps.spreadsheet'
    UNKOWN = 'application/vnd.google-apps.unknown'
    VIDEO = 'application/vnd.google-apps.video'
