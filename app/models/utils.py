from copy import deepcopy
from typing import Type, Any

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    """
    Decorator, to make existing models, all optional, not too useul here.
    :param model:
    :return:
    """
    def make_field_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
    )
