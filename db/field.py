import dataclasses
from typing import Optional, Callable, Any

DEFAULT_VALUES = ["CURRENT_TIMESTAMP", "NULL", "TRUE", "FALSE"]


class Field:
    def __init__(
        self,
        type: type[str | int | float | bool] | str | int | float | bool,
        primary_key: bool = False,
        unique: bool = False,
        nullable: bool = True,
        default: Optional[Callable[[], Any]] | Any = None,
        index: bool = False,
        foreign_key: Optional[str] = None,
        foreign_table: Optional[str] = None,
        check: Optional[str] = None,
        autoincrement: bool = False,
    ):
        self.type = type
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable
        self.default = default
        self.index = index
        self.foreign_key = foreign_key
        self.foreign_table = foreign_table
        self.check = check
        self.autoincrement = autoincrement

    def _to_sql(self):
        constraints = []
        if self.primary_key:
            constraints.append("PRIMARY KEY")
        if self.unique:
            constraints.append("UNIQUE")
        if not self.nullable:
            constraints.append("NOT NULL")
        if self.index:
            constraints.append("INDEX")
        if self.foreign_key:
            if self.foreign_table:
                constraints.append(
                    f"REFERENCES {self.foreign_table}({self.foreign_key})"
                )
            else:
                constraints.append(f"FOREIGN KEY ({self.foreign_key})")
        if self.check:
            constraints.append(f"CHECK ({self.check})")
        if self.autoincrement:
            constraints.append("AUTOINCREMENT")
        if not callable(self.default) and self.default is not None:
            constraints.append(
                f"DEFAULT {self.default.upper() if isinstance(self.default, str) and self.default.upper() in DEFAULT_VALUES else self.default}"
            )

        return " ".join(constraints)

    def set(self):
        metadata = {
            "type": self.type,
            "primary_key": self.primary_key,
            "unique": self.unique,
            "nullable": self.nullable,
            "index": self.index,
            "foreign_key": self.foreign_key,
            "foreign_table": self.foreign_table,
            "check": self.check,
            "autoincrement": self.autoincrement,
            "sql": self._to_sql(),
        }

        if callable(self.default):
            return dataclasses.field(default_factory=self.default, metadata=metadata)

        return dataclasses.field(default=self.default, metadata=metadata)
