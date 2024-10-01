#!/usr/bin/python

from sys import exit
from ECS.Entities.entity import Entity
from ECS.Components import Image, Animation, SpriteRenderer, FrameDuration
from ECS.Systems import Window, GameLoop, Scene
from ECS.Basics import Vector2D
from ECS.Data import DataManager

def create_scene():
    mainScene = Scene('Main Scene')
    entity = Entity('Entity')
    entity.transform.position = Vector2D(300, 300)
    image = Image('Earth', "./Assets/earth.png").make_frames(50, 1, 50, 0.1)

    pf = image.as_prefab()
    DataManager().export_prefab(pf, 'image_prefab.pimg')

    animation = Animation("Earth Animation", image, [FrameDuration(49-i, 0.1) for i in range(50)])
    s_renderer = SpriteRenderer("Earth Renderer", image, animation)

    entity.add_component(image)
    entity.add_component(animation)
    entity.add_component(s_renderer)

    mainScene.add_entity(entity)
    return mainScene

def main():
    data_saver = DataManager()
    #mainScene = create_scene()
    #data_saver.export_to_json(mainScene)
    scene = data_saver.import_from_json()
    data_saver.update_scene_with_component_prefab(scene, 'image_prefab.pimg')


    #image_prefab = image.as_prefab()
    #anim_prefab = animation.as_prefab()
    #DataManager().export_prefab(image_prefab, 'image_prefab.pimg')
    #DataManager().export_prefab(anim_prefab, 'anim_prefab.panim')
    #image_from_prefab = DataManager().import_prefab('image_prefab.pimg')
    #anim_from_prefab = DataManager().import_prefab('anim_prefab.panim')
    #for attr in image.__dict__.keys():
    #    print(f"Attribute {attr}: {getattr(image, attr)}")

    print(scene)


    Window(800, 600, 'Window')
    Window().set_bg_color((0, 0, 255))
    loop = GameLoop()
    loop.set_scene(scene)
    loop.start()
    data_saver.export_to_json(scene)


if __name__ == '__main__':
    exit(main())