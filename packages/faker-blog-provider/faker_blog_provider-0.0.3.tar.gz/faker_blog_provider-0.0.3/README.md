# Python Faker Blog Provider

Python Faker Blog Content Provider

## Description

This Python package provides a Faker provider that generates fake blog content in Brazilian Portuguese. It consists of various methods that can be used to create blog-related fake data such as blog titles, blog posts, images, tags, and more.

## Installation

Use pip for install from [source in PyPI](https://pypi.org/project/faker-blog-provider/):

```bash
pip install faker-blog-provider
```

## Tests

Use pytest to test the project:

```bash
pytest -vvsx
```

## Usage

Import the `Faker` class from the `faker` package and initialize an instance of it. Then, import the `BlogProvider` class from the `faker_blog` module. Finally, add the `BlogProvider` to the instance of `Faker`.

```python
from faker import Faker
from faker_blog import BlogProvider

fake = Faker()
fake.add_provider(BlogProvider)

# Generate fake blog content
title = fake.article_title()
image = fake.article_image()
tag = fake.article_tag()
tags = fake.article_tags(nb=5)
category = fake.article_category()
image = fake.article_image()
content_html = fake.article_content_html()

# You can generate a dictionary containing the text and a slugified version using the following methods.
title = fake.article_title_and_slug()
tag = fake.article_tag_and_slug()
tags = fake.article_tags_and_slug(nb=5)
category = fake.article_category_and_slug()

```

## Features

- Generate fake blog titles
- Generate fake blog posts content
- Generate fake blog tag and tags
- Generate fake blog category
- Generate fake URLs for blog image using the [Lorem Picsum](https://picsum.photos/)

## Examples

#### Generate a fake blog title:

```python
title = fake.article_title()
print(title)
```

Output:
```
Os Segredos De Dirigir Um Poderoso Grupo
```

#### Generate fake blog tags:

```python
tags = fake.article_tags(nb=5)
print(tags)
```

Output:
```
['Transformação Pessoal', 'Gestão do Tempo', 'Estratégias de Crescimento', 'Automação', 'Desenvolvimento Sustentável']
```

#### Generate fake blog tags with slug:

```python
tags_and_slug = fake.article_tags_and_slug(nb=3)
print(tags_and_slug)
```

Output:
```
[{'tag': 'Ferramentas para Empreendedores', 'slug': 'ferramentas-para-empreendedores'}, {'tag': 'Transformação Digital', 'slug': 'transformacao-digital'}, {'tag': 'Cultura Empresarial', 'slug': 'cultura-empresarial'}]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
