from enum import Enum

class MimeType(Enum):
    JSON = 'application/json'
    TEXT = 'text/plain'
    HTML = 'text/html'
    XML = 'application/xml'
    JPEG = 'image/jpeg'
    PNG = 'image/png'
    PDF = 'application/pdf'
    OCTET_STREAM = 'application/octet-stream'
    ZIP = 'application/zip'

EXTENSION_TO_MIME = {
    'json': MimeType.JSON.value,
    'txt': MimeType.TEXT.value,
    'html': MimeType.HTML.value,
    'xml': MimeType.XML.value,
    'jpg': MimeType.JPEG.value,
    'jpeg': MimeType.JPEG.value,
    'png': MimeType.PNG.value,
    'pdf': MimeType.PDF.value,
    'bin': MimeType.OCTET_STREAM.value,
    'zip': MimeType.ZIP.value
}