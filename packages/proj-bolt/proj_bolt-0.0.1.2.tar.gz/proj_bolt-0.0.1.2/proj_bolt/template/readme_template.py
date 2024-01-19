from .base_template import Template

fields = ['project_name']

template = """# {project_name}
"""


class READMEMarkdownTemplate(Template):
    @classmethod
    def template(cls) -> str:
        return template

    @classmethod
    def fields(cls) -> list[str]:
        return fields


__all__ = [READMEMarkdownTemplate]
