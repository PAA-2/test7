import hashlib
from io import BytesIO
from PIL import Image
import pytesseract


def sha256_file(f) -> str:
    hasher = hashlib.sha256()
    for chunk in iter(lambda: f.read(8192), b""):
        hasher.update(chunk)
    f.seek(0)
    return hasher.hexdigest()


def extract_text_from_file(django_file, mime_hint=None) -> str:
    content = django_file.read()
    django_file.seek(0)
    try:
        img = Image.open(BytesIO(content))
        return pytesseract.image_to_string(img, lang="fra") or ""
    except Exception:
        return ""
