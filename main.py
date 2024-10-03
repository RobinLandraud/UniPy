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
    entity.transform.position = Vector2D(100, 300)
    image = Image('Earth', "./Assets/earth.png").make_frames(50, 1, 50)
    animation = Animation("Earth Animation", image, [FrameDuration(49-i, 0.3) for i in range(50)])
    s_renderer = SpriteRenderer("Earth Renderer", image, animation)
    entity.add_component(image)
    entity.add_component(animation)
    entity.add_component(s_renderer)

    entity2 = Entity('Entity 2')
    entity2.transform.position = Vector2D(500, 300)
    image = Image('Earth 1', "./Assets/earth.png").make_frames(50, 1, 50)
    animation = Animation("Earth Animation 2", image, [FrameDuration(i, 0.1) for i in range(50)])
    s_renderer = SpriteRenderer("Earth Renderer 2", image, animation)
    entity2.add_component(image)
    entity2.add_component(animation)
    entity2.add_component(s_renderer)

    entity3 = Entity('Entity 3')
    entity3.transform.position = Vector2D(300, 300)
    image = Image('Earth 2', "./Assets/earth.png").make_frames(45, 1, 45)
    animation = Animation("Earth Animation 3", image, [FrameDuration(i, 0.4) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 3", image, animation)
    entity3.add_component(image)
    entity3.add_component(animation)
    entity3.add_component(s_renderer)

    entity4 = Entity('Entity 4')
    entity4.transform.position = Vector2D(700, 300)
    image = Image('Earth 3', "./Assets/earth.png").make_frames(40, 1, 40)
    animation = Animation("Earth Animation 4", image, [FrameDuration(i, 0.1) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 4", image, animation)
    entity4.add_component(image)
    entity4.add_component(animation)
    entity4.add_component(s_renderer)

    entity5 = Entity('Entity 5')
    entity5.transform.position = Vector2D(100, 100)
    image = Image('Earth 4', "./Assets/earth.png").make_frames(35, 1, 35)
    animation = Animation("Earth Animation 5", image, [FrameDuration(i, 0.05) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 5", image, animation)
    entity5.add_component(image)
    entity5.add_component(animation)
    entity5.add_component(s_renderer)

    entity6 = Entity('Entity 6')
    entity6.transform.position = Vector2D(500, 100)
    image = Image('Earth 5', "./Assets/earth.png").make_frames(30, 1, 30)
    animation = Animation("Earth Animation 6", image, [FrameDuration(i, 0.1) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 6", image, animation)
    entity6.add_component(image)
    entity6.add_component(animation)
    entity6.add_component(s_renderer)

    entity7 = Entity('Entity 7')
    entity7.transform.position = Vector2D(300, 100)
    image = Image('Earth 6', "./Assets/earth.png").make_frames(25, 1, 25)
    animation = Animation("Earth Animation 7", image, [FrameDuration(i, 0.1) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 7", image, animation)
    entity7.add_component(image)
    entity7.add_component(animation)
    entity7.add_component(s_renderer)

    entity8 = Entity('Entity 8')
    entity8.transform.position = Vector2D(700, 100)
    image = Image('Earth 7', "./Assets/earth.png").make_frames(20, 1, 20)
    animation = Animation("Earth Animation 8", image, [FrameDuration(i, 0.1) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Rendere 8", image, animation)
    entity8.add_component(image)
    entity8.add_component(animation)
    entity8.add_component(s_renderer)

    entity9 = Entity('Entity 9')
    entity9.transform.position = Vector2D(100, 500)
    image = Image('Earth 8', "./Assets/earth.png").make_frames(15, 1, 15)
    animation = Animation("Earth Animation 9", image, [FrameDuration(i, 0.1) for i in range(len(image.data_frames))])
    s_renderer = SpriteRenderer("Earth Renderer 9", image, animation)
    entity9.add_component(image)
    entity9.add_component(animation)
    entity9.add_component(s_renderer)



    #pf = image.as_prefab()
    #DataManager().export_prefab(pf, 'image_prefab.pimg')

    mainScene.add_entity(entity)
    mainScene.add_entity(entity2)
    mainScene.add_entity(entity3)
    mainScene.add_entity(entity4)
    mainScene.add_entity(entity5)
    mainScene.add_entity(entity6)
    mainScene.add_entity(entity7)
    mainScene.add_entity(entity8)
    mainScene.add_entity(entity9)
    return mainScene

def main():
    Window(800, 600, 'Window')
    Window().set_bg_color((0, 0, 255))

    data_saver = DataManager()
    mainScene = create_scene()
    data_saver.export_to_json(mainScene)
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
    loop = GameLoop(600)
    loop.set_scene(scene)
    loop.start()
    
    data_saver.export_to_json(scene)


if __name__ == '__main__':
    exit(main())