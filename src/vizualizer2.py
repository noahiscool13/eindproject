from random import shuffle

from PIL import Image, ImageOps, ImageDraw
from math import floor, ceil, modf

def stepped_range(end,steps):
    t = 0
    while t<end:
        yield t
        t+=1/steps

def agent_to_col(agent,pixel_type=0):
    return tuple(eval(agent.name) + [pixel_type])

def name_from_pixel(pixel):
    return str(list(pixel[:2]))

def create_frame(maze, paths, t,bg,man,wpi,house,all_wp):
    size = 50
    im = bg
    # im = im.resize((im.width * size, im.height * size),Image.NEAREST)
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)


    for agent in maze.agents:
        for waypoint in agent.waypoints:
            col = agent_to_col(agent,0)
            im.paste(wpi[(all_wp.index(waypoint))%len(wpi)], (size*waypoint[0],size*waypoint[1]))
            # draw.ellipse([size*waypoint[0]+size//4,size*waypoint[1]+size//4,size*waypoint[0]+size-1-size//4,size*waypoint[1]+size-1-size//4],col)
            # draw.rectangle([size*waypoint[0],size*waypoint[1],size*waypoint[0]+size-1,size*waypoint[1]+size-1], col)
        col = agent_to_col(agent, 50)

        # draw.rectangle([size*agent.goal[0]+size//8,size*agent.goal[1]+size//8,size*agent.goal[0]+size-1-size//8,size*agent.goal[1]+size-1-size//8], col)

        im.paste(house, (size*agent.goal[0], size*agent.goal[1]))

    for path in paths.paths:
        pos1 = path.path[min(floor(t),len(path.path)-1)][0]
        pos2 = path.path[min(ceil(t), len(path.path) - 1)][0]
        if pos1 in path.agent.waypoints:
            path.agent.waypoints.remove(pos1)

        linear = modf(t)[0]

        true_pos = (int((size*((1-linear)*pos1[0]+linear*pos2[0]))),int(size*((1-linear)*pos1[1]+linear*pos2[1])))

        col = agent_to_col(path.agent)
        im.paste(man,(true_pos[0],true_pos[1]))
        # draw.ellipse([true_pos[0],true_pos[1],
        #               true_pos[0]+size-1,true_pos[1]+size-1], col)

    return im


def create_gif(file, maze, paths, speed):
    bg = Image.open("sprite/shop_bg.png")
    man = Image.open("sprite/man.png")
    man = man.resize((50,50))

    kip = Image.open("sprite/kip.png")
    brood = Image.open("sprite/brood.png")
    melk = Image.open("sprite/melk.png")
    tomaat = Image.open("sprite/tomaat.png")
    prei = Image.open("sprite/prei.png")
    ketchup = Image.open("sprite/ketchup.png")

    house = Image.open("sprite/house.png")

    wp = [kip,brood,melk,tomaat,prei,ketchup]

    all_wp = []
    for agent in maze.agents:
        for waypoint in agent.waypoints:
            all_wp.append(waypoint)
    shuffle(all_wp)


    im = [create_frame(maze, paths, t,bg,man,wp,house,all_wp) for t in stepped_range(paths.max_of_individual_costs(),4)]
    for x in range(len(im)):
        im[x] = im[x]
    im[0].save(file, save_all=True, append_images=im[1:], duration=speed, loop=0)
