from random import choice, randint
from faker_blog.templates import text
from faker_blog.utils import random_string


def tag(tag, content: str) -> str:
    return f"<{tag}>{content}</{tag}>"


def p(content: str) -> str:
    return tag("p", content)


def h(nivel: int = 1, content: str = "") -> str:
    return tag(f"h{nivel}", content)


def img(src: str) -> str:
    return f'<img src="{src}">'


def blockquote(content: str) -> str:
    return tag("blockquote", content)


def content():
    template_1 = "".join([
        h(2, text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        img(f"https://picsum.photos/1280/720?x={random_string()}"),
        h(3, text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(3, 6))])),
        blockquote(text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
    ])

    template_2 = "".join([
        blockquote(text.make_title()),
        h(2, text.make_title()),
        img(f"https://picsum.photos/1280/720?x={random_string()}"),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        h(3, text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(3, 6))])),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
    ])

    template_3 = "".join([
        h(2, text.make_title()),
        blockquote(text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        h(3, text.make_title()),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        p(". ".join([text.make_title() for _ in range(randint(3, 6))])),
        p(". ".join([text.make_title() for _ in range(randint(4, 7))])),
        img(f"https://picsum.photos/1280/720?x={random_string()}"),
    ])

    return choice([template_1, template_2, template_3])
