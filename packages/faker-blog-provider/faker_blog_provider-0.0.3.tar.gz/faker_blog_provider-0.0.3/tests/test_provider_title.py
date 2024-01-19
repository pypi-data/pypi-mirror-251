from faker import Faker
from faker_blog import BlogProvider
from faker_blog.utils import slugify

fake = Faker()
fake.add_provider(BlogProvider)


def test_provider_has_title_method():
    assert hasattr(fake, "article_title")


def test_provider_title_is_a_string():
    assert isinstance(fake.article_title(), str)


def test_provider_has_title_and_slug_method():
    assert hasattr(fake, "article_title_and_slug")


def test_provider_title_and_slug_is_a_dict():
    assert isinstance(fake.article_title_and_slug(), dict)


def test_slugify_can_slugify_title():
    data = fake.article_title_and_slug()

    assert data["slug"] == slugify(data["title"])
