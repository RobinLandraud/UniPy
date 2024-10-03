import json
import jsonpickle
import os
from typing import Type
from ..Basics.ID import IDGen
from ..Systems.Scenes import Scene

class DataManager:
    def __init__(self, path="./.data/"):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.file_path = os.path.join(self.path, f'data.json')
        self._references = {
            "py/object": [
                "ECS.Components.Sprites.Sprites.Image",
                "ECS.Components.Sprites.Animator.Animation"
            ]
        }

    def _rec_replace_data_with_reference(self, d, target_key, target_value):
        if isinstance(d, dict):
            if target_key in d and d[target_key] == target_value:
                for t_key in self._references:
                    for t_value in self._references[t_key]:
                        for key in d.keys():
                            self._replace_data_with_reference(d[key], t_key, t_value)
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

    def _replace_data_with_reference(self, d):
        stack = [d]
        to_write = []

        while stack:
            current_dict = stack.pop()

            if isinstance(current_dict, dict):
                for ref_key, ref_values in self._references.items():
                    if ref_key in current_dict and current_dict[ref_key] in ref_values:
                        to_write.append(current_dict) # append at the end of the list
                        break

                for key, value in current_dict.items():
                    if isinstance(value, dict):
                        stack.append(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                stack.append(item)

        for current_dict in to_write: # read from the end to the beginning
            file_path = os.path.join(self.path, f'{current_dict["name"]}.json')
            with open(file_path, 'w') as file:
                file.write(json.dumps(current_dict, indent=4))

            keys_to_delete = [key for key in current_dict.keys() if key not in self._references]
            for key in keys_to_delete:
                del current_dict[key]

            current_dict['__reference__'] = file_path

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

    def free_data(self):
        if os.path.exists(self.path):
            for file in os.listdir(self.path):
                os.remove(os.path.join(self.path, file))

    def export_to_json(self, obj: Type):
        self.free_data()
        json_result = jsonpickle.encode(obj, indent=4, make_refs=True)
        json_data = json.loads(json_result)
        #for key in self._references:
        #    for value in self._references[key]:
        #        self._replace_data_with_reference(json_data, key, value)
        self._replace_data_with_reference(json_data)
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
    
    def _compare_attributes(self, attr1, attr2):
        if isinstance(attr1, dict):
            for key in attr1.keys():
                if key not in attr2:
                    return False
                if not self._compare_attributes(attr1[key], attr2[key]):
                    return False
            return True
        elif isinstance(attr1, (list, tuple)):
            for i in range(len(attr1)):
                if not self._compare_attributes(attr1[i], attr2[i]):
                    return False
            return True
        elif hasattr(attr1, '__dict__'):
            for attr in attr1.__dict__.keys():
                if not attr.startswith('_') and not attr.startswith('__'):
                    if not self._compare_attributes(getattr(attr1, attr), getattr(attr2, attr)):
                        return False
            return True
        else:
            return attr1 == attr2

    def update_scene_with_component_prefab(self, scene: Scene, prefab_path: str):
        prefab = self.import_prefab(prefab_path)
        for entity in scene.entities:
            for component_type in entity.components:
                for component in entity.components[component_type].get():
                    if component._prefab_uuid == prefab._prefab_uuid:
                        for attr in prefab.__dict__.keys():
                            if not attr.startswith('_') and not attr.startswith('__'):
                                pf_val = getattr(prefab, attr)
                                comp_val = getattr(component, attr)
                                if not self._compare_attributes(pf_val, comp_val):
                                    print(f"Updating {component.name} attribute {attr}")
                                    setattr(component, attr, pf_val)
        return scene