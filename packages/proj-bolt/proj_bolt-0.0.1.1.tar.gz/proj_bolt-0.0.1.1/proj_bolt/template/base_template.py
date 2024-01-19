import abc


class Template(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def template(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def fields(cls) -> list[str]:
        pass

    @classmethod
    def render(cls, **kwargs):
        # check fields
        cls._check_fields(**kwargs)
        return cls.template().format(**kwargs)

    @classmethod
    def _check_fields(cls, **kwargs):
        missing_fields = []
        redundant_fields = []
        error_msg = ""
        for field in cls.fields():
            if field not in kwargs:
                missing_fields.append(field)
        for field in kwargs:
            if field not in cls.fields():
                redundant_fields.append(field)
        if len(missing_fields) > 0:
            error_msg += f"Missing fields: {missing_fields}\n"
        if len(redundant_fields) > 0:
            error_msg += f"Redundant fields: {redundant_fields}\n"
        if len(error_msg) > 0:
            raise ValueError(error_msg)


__all__ = ['Template']
