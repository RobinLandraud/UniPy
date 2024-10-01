import json
import jsonpickle
import os
from typing import Type
from ..Basics.ID import IDGen
from ..Systems.Scenes import Scene

class DataSaver:
    def __init__(self, path="./.data/"):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.file_path = os.path.join(self.path, f'data.json')

    def _replace_data_with_reference(self, d, target_key, target_value):
        if isinstance(d, dict):
            if target_key in d and d[target_key] == target_value:
                file_path = os.path.join(self.path, f'./{d["name"]}.json')
                with open(file_path, 'w') as file:
                    file.write(json.dumps(d, indent=4))
                for key in list(d.keys()):
                    if key != target_key:
                        del d[key]
                d['__reference__'] = file_path

            for _, value in d.items():
                if isinstance(value, dict):
                    self._replace_data_with_reference(value, target_key, target_value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._replace_data_with_reference(item, target_key, target_value)

    def _replace_reference_with_data(self, d):
        if isinstance(d, dict):
            if '__reference__' in d:
                file_name = d['__reference__']
                with open(file_name, 'r') as file:
                    data = json.loads(file.read())
                del d['__reference__']
                for key, value in data.items():
                    d[key] = value

            for _, value in d.items():
                if isinstance(value, dict):
                    self._replace_reference_with_data(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._replace_reference_with_data(item)

    def export_to_json(self, obj: Type):
        json_result = jsonpickle.encode(obj, indent=4, make_refs=True)
        json_data = json.loads(json_result)
        self._replace_data_with_reference(json_data, "py/object", "ECS.Components.Sprites.Sprites.Image")
        self._replace_data_with_reference(json_data, "py/object", "ECS.Components.Sprites.Animator.Animation")
        json_result = json.dumps(json_data, indent=4)
        with open(self.file_path, 'w') as file:
            file.write(json_result)
        return json_result

    def import_from_json(self, file_name: str = 'data.json'):
        path_file = os.path.join(self.path, file_name)
        with open(path_file, 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        self._replace_reference_with_data(data)
        entity = jsonpickle.decode(json.dumps(data))
        return entity
    
    def import_prefab(self, file_path: str):
        with open(file_path, 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        obj = jsonpickle.decode(json.dumps(data))
        if hasattr(obj, '_is_prefab') and obj._is_prefab:
            obj._is_prefab = False
        if hasattr(obj, 'id') and not obj.id:
            obj.id = IDGen.new_id()
        return obj
    
    def export_prefab(self, obj: Type, file_path: str):
        if hasattr(obj, '_is_prefab') and not obj._is_prefab and hasattr(obj, 'as_prefab'):
            obj = obj.as_prefab()
        json_result = jsonpickle.encode(obj, indent=4, make_refs=True)
        json_data = json.loads(json_result)
        json_result = json.dumps(json_data, indent=4)
        with open(file_path, 'w') as file:
            file.write(json_result)
        return json_result
    
    def update_scene_with_component_prefab(self, scene: Scene, prefab_path: str):
        prefab = self.import_prefab(prefab_path)
        for entity in scene.entities:
            for component_type in entity.components:
                for component in entity.components[component_type].get():
                    if component._prefab_uuid == prefab._prefab_uuid:
                        for attr in prefab.__dict__.keys():
                            if not attr.startswith('_') and not attr.startswith('__'):
                                val = getattr(prefab, attr)
                                if val and val != getattr(component, attr):
                                    print(f"Updating {component.name} attribute {attr}")
                                    setattr(component, attr, val)
        return scene