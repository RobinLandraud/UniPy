#!/usr/bin/python

from sys import exit
from ECS.Entities.entity import Entity
from ECS.Components import Image, Animation, SpriteRenderer, FrameDuration
from ECS.Systems import Window, GameLoop, Scene
from ECS.Basics import Vector2D
from typing import List
import json
import jsonpickle

def export_to_json(entity: Entity, file_name: str = './data.json'):
    json_result = jsonpickle.encode(entity, indent=4, make_refs=True)
    with open(file_name, 'w') as file:
        file.write(json_result)
    return json_result

def create_scene():
    mainScene = Scene('Main Scene')
    entity = Entity('Entity')
    entity.transform.position = Vector2D(300, 300)
    image = Image('Earth', "./Assets/earth.png").make_frames(50, 1, 50, 0.1)
    animation = Animation("Earth Animation", image, [FrameDuration(49-i, 0.1) for i in range(50)])
    s_renderer = SpriteRenderer("Earth Renderer", image, animation)

    entity.add_component(image)
    entity.add_component(animation)
    entity.add_component(s_renderer)

    mainScene.add_entity(entity)
    return mainScene

def main():
    #mainScene = create_scene()
    #export_to_json(mainScene)

    with open('./data.json', 'r') as file:
        json_data = file.read()
    scene = jsonpickle.decode(json_data)


    Window(800, 600, 'Window')
    Window().set_bg_color((0, 0, 255))
    loop = GameLoop()
    loop.set_scene(scene)
    loop.start()


if __name__ == '__main__':
    exit(main())