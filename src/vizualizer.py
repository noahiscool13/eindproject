from PIL import Image, ImageOps


def create_frame(maze, paths, t):
    im = ImageOps.invert(Image.fromarray(maze.grid * 255))
    im = im.convert('RGB')
    for path in paths.solution.paths:
        pos = path.path[min(t,len(path.path)-1)][0]
        col = tuple(eval(path.agent.name) + [0])
        im.putpixel(pos, col)
    return im


def create_gif(file, maze, paths, speed):
    im = [create_frame(maze, paths, t) for t in range(paths.solution.max_of_individual_costs())]
    for x in range(len(im)):
        im[x] = im[x].resize((im[x].width * 8, im[x].height * 8),Image.NEAREST)
    im[0].save(file, save_all=True, append_images=im[1:], duration=speed, loop=0)
