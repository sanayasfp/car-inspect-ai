import dataclasses
from typing import Callable, Any
import re


class BaseModel:
    def __post_init__(self):
        self._dict = self.to_dict()

    def to_dict(self):
        return dataclasses.asdict(self)
    
    def to_insert(self):
        data = self.to_dict()
        
        # if keys is autoincrement, remove it from the data
        keys = list(data.keys())
        for key in keys:
            metadata = self.__dataclass_fields__[key].metadata
            if metadata.get("autoincrement", False):
                data.pop(key)
        return data

    @staticmethod
    def _py_type_to_sql_type(py_type: type):
        if py_type in [int, "int"]:
            return "INTEGER"
        elif py_type in [str, "str"]:
            return "TEXT"
        elif py_type in [float, "float"]:
            return "REAL"
        elif py_type in [bool, "bool"]:
            return "INTEGER"
        else:
            return "BLOB"

    @staticmethod
    def from_dict(data: dict):
        return BaseModel(**data)

    @staticmethod
    def from_sql(data: tuple):
        return BaseModel(*data)

    @classmethod
    def to_model(cls):
        """
        Read the class attributes and return a dictionary with the model structure
        Cast the attribute type to the SQL type equivalent
        Read the attribute value for additional constraints
        """
        model = {}
        for attr, annotation_type in cls.__annotations__.items():
            metadata = cls.__dataclass_fields__[attr].metadata
            sql_type = BaseModel._py_type_to_sql_type(
                metadata.get("type", annotation_type)
            )
            metadata = metadata.get("sql", "")
            model[attr] = f"{sql_type} {metadata}".strip()
        return model

    @staticmethod
    def set_constraints(constraints: str = "", default: Callable[[], Any] | Any = None):
        if callable(default):
            return dataclasses.field(
                default_factory=default, metadata={"sql": constraints}
            )
        else:
            return dataclasses.field(default=default, metadata={"sql": constraints})

    def _get_model_name(self, model_name: str, case: str = "snake_case") -> str:
        if hasattr(self, "_table_name"):
            model_name = self._table_name
        else:
            model_name = re.sub(r"Model$", "", model_name)

        def to_snake_case(name: str) -> str:
            return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        def to_camel_case(name: str) -> str:
            parts = to_snake_case(name).split("_")
            return parts[0] + "".join(word.title() for word in parts[1:])

        def to_pascal_case(name: str) -> str:
            parts = to_snake_case(name).split("_")
            return "".join(word.title() for word in parts)

        if case == "snake_case":
            model_name = to_snake_case(model_name)
        elif case == "camelCase":
            model_name = to_camel_case(model_name)
        elif case == "PascalCase":
            model_name = to_pascal_case(model_name)
        else:
            raise ValueError(f"Unknown case format: {case}")

        return model_name

    def get_table_name(self):
        return self._get_model_name(self, self.__class__.__name__)
        
