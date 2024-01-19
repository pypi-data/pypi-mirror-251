import os
from collections import OrderedDict
from InquirerPy import prompt
from dektools.yaml import yaml
from dektools.dict import is_dict, dict_merge
from ..utils import normalize_prompt


class Cfg:
    _empty_value = object()

    @classmethod
    def _flat_schema(cls, schema, *keys):
        result = []
        for k, v in schema.items():
            if is_dict(v):
                result.extend(cls._flat_schema(v, *keys, k))
            else:
                result.append(((*keys, k), v))
        return result

    @classmethod
    def _get_value(cls, values, keys):
        cursor = values
        for key in keys:
            if key not in cursor:
                return cls._empty_value
            cursor = cursor[key]
        return cursor

    def inputs_update_cfg(self, values, schema):
        schema_list = self._flat_schema(schema)
        questions = []
        for keys, value in schema_list:
            default = self._get_value(values, keys)
            if default is self._empty_value:
                default = value
            name = '.'.join(keys)
            questions.append(normalize_prompt({
                "type": "input",
                "message": name + ":",
                "name": name,
                "default": default or ''
            }))
        inputs = prompt(questions)
        result = OrderedDict()
        for keys, _ in schema_list:
            cursor = result
            for key in keys[:-1]:
                cursor = cursor.setdefault(key, OrderedDict())
            cursor[keys[-1]] = inputs['.'.join(keys)]
        return result


class CfgFile(Cfg):
    def __init__(self, path_cfg, *paths_schema):
        self.path_cfg = path_cfg
        self.paths_schema = paths_schema

    @property
    def values(self):
        if self.path_cfg and os.path.isfile(self.path_cfg):
            return yaml.load(self.path_cfg)
        else:
            return OrderedDict()

    @property
    def schema(self):
        schema = OrderedDict()
        for path_schema in self.paths_schema:
            dict_merge(schema, yaml.load(path_schema))
        return schema

    def apply(self):
        result = self.inputs_update_cfg(self.values, self.schema)
        if self.path_cfg:
            yaml.dump(self.path_cfg, result)
        return result
