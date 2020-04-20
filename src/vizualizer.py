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

def create_frame(maze, paths, t):
    size = 25

    im = ImageOps.invert(Image.fromarray(maze.grid * 255))
    im = im.resize((im.width * size, im.height * size),Image.NEAREST)
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)

    for agent in maze.agents:
        for waypoint in agent.waypoints:
            col = agent_to_col(agent,50)
            draw.rectangle([size*waypoint[0],size*waypoint[1],size*waypoint[0]+size-1,size*waypoint[1]+size-1], col)
        col = agent_to_col(agent, 80)
        draw.rectangle([size*agent.goal[0],size*agent.goal[1],size*agent.goal[0]+size-1,size*agent.goal[1]+size-1], col)

    for path in paths.paths:
        pos1 = path.path[min(floor(t),len(path.path)-1)][0]
        pos2 = path.path[min(ceil(t), len(path.path) - 1)][0]
        if pos1 in path.agent.waypoints:
            path.agent.waypoints.remove(pos1)

        linear = modf(t)[0]

        true_pos = (int((size*((1-linear)*pos1[0]+linear*pos2[0]))),int(size*((1-linear)*pos1[1]+linear*pos2[1])))

        col = agent_to_col(path.agent)


        draw.rectangle((true_pos[0],true_pos[1],
                      true_pos[0]+size-1,true_pos[1]+size-1),
                     fill=col)
    return im


def create_gif(file, maze, paths, speed):
    im = [create_frame(maze, paths, t) for t in stepped_range(paths.max_of_individual_costs(),10)]
    for x in range(len(im)):
        im[x] = im[x]
    im[0].save(file, save_all=True, append_images=im[1:], duration=speed, loop=0)
