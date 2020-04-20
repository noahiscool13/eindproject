from PIL import Image, ImageOps

def agent_to_col(agent,pixel_type=0):
    return tuple(eval(agent.name) + [pixel_type])

def name_from_pixel(pixel):
    return str(list(pixel[:2]))

def create_frame(maze, paths, t):
    im = ImageOps.invert(Image.fromarray(maze.grid * 255))
    im = im.convert('RGB')
    for agent in maze.agents:
        for waypoint in agent.waypoints:
            col = agent_to_col(agent,50)
            im.putpixel(waypoint, col)
        col = agent_to_col(agent, 80)
        im.putpixel(agent.goal, col)

    for path in paths.paths:
        pos = path.path[min(t,len(path.path)-1)][0]
        if pos in path.agent.waypoints:
            path.agent.waypoints.remove(pos)
        col = agent_to_col(path.agent)
        im.putpixel(pos, col)
    return im


def create_gif(file, maze, paths, speed):
    im = [create_frame(maze, paths, t) for t in range(paths.max_of_individual_costs())]
    for x in range(len(im)):
        im[x] = im[x].resize((im[x].width * 15, im[x].height * 15),Image.NEAREST)
    im[0].save(file, save_all=True, append_images=im[1:], duration=speed, loop=0)
