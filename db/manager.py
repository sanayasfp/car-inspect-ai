import sqlite3
import os
import re
from traceback import print_exc
import constants
import db.models as models_module
from db.models import BaseModel


class Manager:
    def __init__(
        self,
        db_name: str = constants.DB_NAME,
        force: bool | list = False,
        check_same_thread=False,
    ):
        self._models_hash_path = os.path.join(constants.DB_DIR, ".models.hash")
        self.models = {}
        self.db_name = self.get_db_name(db_name)
        self.create_connection(check_same_thread=False)
        self._load_models()
        self.init_models(force)

    def get_db_name(self, db_name: str = None):
        for_self = db_name is None
        db_name = db_name if db_name.endswith(".db") else f"{db_name}.db"

        if for_self:
            self.db_name = db_name

        return db_name

    def __del__(self):
        self.close_connection()

    def create_connection(self, check_same_thread=False) -> sqlite3.Connection:
        db_file_path = os.path.join(constants.DB_DIR, self.db_name)
        self.conn = None
        try:
            if not os.path.exists(db_file_path):
                print(f"WARN: Database file not found: {db_file_path}")
                os.makedirs(constants.DB_DIR, exist_ok=True)
                open(db_file_path, "w").close()

            self.conn = sqlite3.connect(db_file_path, check_same_thread=False)
        except sqlite3.Error as e:
            print_exc()
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self, table_name: str, columns: list | dict) -> bool:
        if not self.conn:
            raise ValueError("Database connection is not established")

        if not table_name or not isinstance(table_name, str):
            raise ValueError("Invalid table name provided")

        if not columns or not isinstance(columns, (list, dict)):
            raise ValueError("Columns must be a non-empty list or dictionary")

        # Format the column definitions
        if isinstance(columns, list):
            if not all(isinstance(col, str) for col in columns):
                raise ValueError("All items in the list must be strings")
            formatted_columns = ", ".join(columns)
        elif isinstance(columns, dict):
            formatted_columns = ", ".join(
                [
                    f"{col_name} {col_data}".strip()
                    for col_name, col_data in columns.items()
                ]
            )

        # Check table name for safety (prevent SQL injection)
        if not table_name.isidentifier():
            raise ValueError(f"Invalid table name: {table_name}")

        try:
            # Execute the CREATE TABLE statement
            cursor = self.conn.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({formatted_columns})"
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
            print_exc()
            return False

    def _update_model_hash(self, models):
        with open(self._models_hash_path, "w") as f:
            f.write(str(hash(str(models))))

        return True

    def _check_for_models_change(self):
        if not os.path.exists(self._models_hash_path):
            return self._update_model_hash(self.models)

        with open(self._models_hash_path, "r") as f:
            old_hash = f.read()
            new_hash = str(hash(str(self.models)))

            if old_hash != new_hash:
                return self._update_model_hash(self.models)

        return False

    @staticmethod
    def _get_models_name(model_name: str, model_class, case: str = "snake_case") -> str:
        if hasattr(model_class, "_table_name"):
            model_name = model_class._table_name
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

    def _load_models(self):
        """
        Load and transform model names from the module.
        """
        for model_name, model_class in models_module.__dict__.items():
            # Skip non-class objects
            if not isinstance(model_class, type):
                continue

            if not issubclass(model_class, models_module.BaseModel):
                continue

            if model_name == "BaseModel":
                continue

            # model_name = self._get_models_name(model_name, model_class)
            model_name = model_class.get_table_name(model_class)
            self.models[model_name] = model_class.to_model()

    def init_models(self, force: bool | list | tuple | dict = False):
        if not self.conn:
            raise ValueError("Database connection is not established")

        if not force and not self._check_for_models_change():
            return

        if force:
            # Drop all tables
            cursor = self.conn.cursor()
            # Hard reset
            # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # table_names = cursor.fetchall()
            # table_names = [table[0] for table in table_names]

            # Soft reset
            if isinstance(force, list | tuple):
                table_names = force
            elif isinstance(force, dict):
                table_names = [key for key, value in force.items() if value]
            else:
                table_names = self.models.keys()

            for table_name in table_names:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

            for table_name in table_names:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        created = []
        errors = []

        for table_name, columns in self.models.items():
            try:
                self.create_table(table_name, columns)
                created.append(table_name)
            except sqlite3.Error as e:
                errors.append((table_name, e))
                continue

        print(f"Tables created:")
        print("\n->".join(created) if created else "No tables created")
        print(f"Errors:")
        if errors:
            print(
                "\n->".join([f"{table_name}: {error}" for table_name, error in errors])
            )
        else:
            print("No errors")

    def insert(self, table_name: str, data: dict | BaseModel) -> bool:
        if not self.conn:
            raise ValueError("Database connection is not established")

        if not table_name or not isinstance(table_name, str):
            raise ValueError("Invalid table name provided")

        if isinstance(data, BaseModel):
            data = data.to_insert()

        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary")

        # Format the data for insertion
        formatted_data = ", ".join([f"'{value}'" for value in data.values()])

        # Check table name for safety (prevent SQL injection)
        if not table_name.isidentifier():
            raise ValueError(f"Invalid table name: {table_name}")

        try:
            # Execute the INSERT INTO statement
            cursor = self.conn.cursor()
            cursor.execute(
                f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({formatted_data})"
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
            print_exc()
            return False

    def select(
        self,
        table_name: str,
        columns: list | str = "*",
        filters: str = "",
        condition: str = "",
        values: list = [],
        verbose: bool = False,
    ) -> list:
        if not self.conn:
            raise ValueError("Database connection is not established")

        if not table_name or not isinstance(table_name, str):
            raise ValueError("Invalid table name provided")

        if not columns:
            raise ValueError("Columns must be a non-empty list or string")

        if not isinstance(columns, str) and not all(
            isinstance(col, str) for col in columns
        ):
            raise ValueError("All items in the list must be strings")

        if not isinstance(condition, str):
            raise ValueError("Condition must be a string")

        # Check table name for safety (prevent SQL injection)
        if not table_name.isidentifier():
            raise ValueError(f"Invalid table name: {table_name}")

        try:
            # Execute the SELECT statement
            cursor = self.conn.cursor()
            where = f"WHERE {filters}" if filters else ""
            sql = f"SELECT {', '.join(columns)} FROM {table_name} {where} {condition}"
            if verbose:
                print(f"SQL: {sql}")
                print(f"Values: {values}")
            cursor.execute(sql, values)

            def to_dict(res: list[tuple]):
                return [dict(zip(columns, row)) for row in res if row]

            return to_dict(cursor.fetchall())
        except sqlite3.Error as e:
            print("SQLite error:", e)
            print_exc()
            return []
