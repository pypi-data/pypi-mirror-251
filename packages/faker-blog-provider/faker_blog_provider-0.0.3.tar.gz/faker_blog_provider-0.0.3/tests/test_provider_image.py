from faker import Faker
from faker_blog import BlogProvider
from faker_blog.utils import slugify

fake = Faker()
fake.add_provider(BlogProvider)


def test_provider_has_image_method():
    assert hasattr(fake, "article_image")


def test_article_image_is_a_string():
    assert isinstance(fake.article_image(), str)


def test_article_image_is_a_unique_url():
    image_1 = fake.article_image()
    image_2 = fake.article_image()

    assert image_1 != image_2
