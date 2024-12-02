from dotenv import load_dotenv
import os
import json


class Env:
    def __init__(self):
        load_dotenv()

    def cast_value(self, value, type):
        if type == "bool":
            return value.lower() in ["true", "1"]
        if type == "int":
            return int(value)
        if type == "float":
            return float(value)
        if type == "array":
            return value.split(",")
        if type == "dict":
            return dict(item.split("=") for item in value.split(","))
        if type == "json":
            return json.loads(value)
        return value

    def get(self, key, default=None):
        return os.getenv(key, default)

    def get_bool(self, key, default=False):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "bool")

    def get_int(self, key, default=0):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "int")

    def get_float(self, key, default=0.0):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "float")

    def get_array(self, key, default=[]):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "array")

    def get_dict(self, key, default={}):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "dict")

    def get_json(self, key, default={}):
        value = self.get(key)
        if value is None:
            return default
        return self.cast_value(value, "json")

    def get_or_fail(self, key):
        value = self.get(key)
        if value is None:
            raise Exception(f"Environment variable {key} is required")
        return value

    def get_bool_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "bool")

    def get_int_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "int")

    def get_float_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "float")

    def get_array_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "array")

    def get_dict_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "dict")

    def get_json_or_fail(self, key):
        value = self.get_or_fail(key)
        return self.cast_value(value, "json")

    def set(self, key, value):
        os.environ[key] = str(value)

env = Env()
