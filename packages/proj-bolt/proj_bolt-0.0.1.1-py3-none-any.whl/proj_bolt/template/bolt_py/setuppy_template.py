from ..base_template import Template

fields = [
    'project_name',
    'author',
]

template = """from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.readlines()
    return [req.strip() for req in requirements if req.strip() and not req.startswith('#')]


setup(
    name='{project_name}',
    version='0.0.1',
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    install_requires=read_requirements(),
    author='{author}',
    author_email='',
    description='',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
)

# To build:
# python setup.py sdist bdist_wheel
# To upload to pypi:
# twine upload dist/*
"""


class SetupPyTemplate(Template):
    @classmethod
    def template(cls) -> str:
        return template

    @classmethod
    def fields(cls) -> list[str]:
        return fields


__all__ = [SetupPyTemplate]
