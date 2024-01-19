from faker.providers import BaseProvider
from faker_blog.templates import html, text
from faker_blog.utils import slugify


class BlogProvider(BaseProvider):
    def article_title(self) -> str:
        return text.make_title()

    def article_title_and_slug(self) -> dict[str, str]:
        title = self.article_title()

        return {"title": title, "slug": slugify(title)}

    def article_tag(self) -> str:
        return self.random_element(text.tags)

    def article_tag_and_slug(self) -> dict[str, str]:
        tag = self.article_tag()

        return {"tag": tag, "slug": slugify(tag)}

    def article_tags(self, nb: int = 3) -> list[str]:
        return [self.article_tag() for _ in range(nb)]

    def article_tags_and_slug(self, nb: int = 3) -> list[dict[str, str]]:
        return [self.article_tag_and_slug() for _ in range(nb)]

    def article_category(self) -> str:
        return self.random_element(text.categories)

    def article_category_and_slug(self) -> dict[str, str]:
        category = self.article_category()

        return {"category": category, "slug": slugify(category)}

    def article_image(self) -> str:
        return f"https://picsum.photos/1280/720?x={self.lexify('??????????')}"

    def article_content_html(self) -> str:
        return html.content()
