from random import sample
import unicodedata
import re
import string


def slugify(content: str) -> str:
    content = str(content).lower().strip()
    content = unicodedata.normalize("NFD", content)
    content = re.sub(r"[\u0300-\u036f]", "", content)
    content = re.sub(r"\s+", "-", content)
    content = content.replace("&", "-and-")
    content = re.sub(r"[^\w\-]+", "", content)
    content = re.sub(r"\-\-+", "-", content)

    return content


def random_string(size: int = 10) -> str:
    return "".join(sample(string.ascii_letters + string.hexdigits, k=size))
