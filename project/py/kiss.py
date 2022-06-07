import cairo, argparse, random, math

coloursRGB = [
(255,255,255), # White
]

colours = []
for colourRGB in coloursRGB:
    colours.append([e / 255 for e in colourRGB])

# height: height and width of the image
# base: the distance between horizontal line and top of the image
# kisspoint: x point where the lowest point of curve is reached
# curve: parameter 'a' of quadratic function
# distance: the distance between horizontal line and lowest point
# accuracy: step of x
def blank_shape(height, base, kisspoint, curve, distance, accuracy):
    w = height

    # Quadratic Function
    # We know the graph has parameter 'a' and passes (kisspoint, base-distance)
    # Here we treat a as curve, h as kisspoint and k as (base-distance)
    h = kisspoint
    k = base - distance
    a = -curve / 1000

    # Add points on the quadratic function
    x = 0
    # List of points for blank shape
    bs = []
    # Add top curve
    while x <= w:
        y = a*((x-h)**2)+k
        bs.append((x, y))
        x += accuracy
    # Add bottom horizontal line
    bs.append((w, base))
    bs.append((0, base))
    bs.append((0, a*(h**2)+k)) # x = 0 in quadratic function

    return bs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-ih", "--height", default=2500, type=int)
    parser.add_argument("-b", "--base", default=1500, type=int)
    parser.add_argument("-kp", "--kisspoint", default=1000, type=int)
    parser.add_argument("-c", "--curve", default=0.1, type=float)
    parser.add_argument("-d", "--distance", default=1, type=int)
    parser.add_argument("-m", "--mode", default="png", type=str)
    parser.add_argument("-acc", "--accuracy", default=0.1, type=float)
    
    args = parser.parse_args()

    shapealpha = args.shapealpha

    height = args.height
    base = args.base
    kisspoint = args.kisspoint
    curve = args.curve
    distance = args.distance

    mode = args.mode

    accuracy = args.accuracy

    width = height

    

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("kiss.svg", width, height)
        cr = cairo.Context(svg)

    # Set background as black
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    colour = colours[0] # White
    cr.set_source_rgba(colour[0], colour[1], colour[2],shapealpha)
    shape = blank_shape(height, base, kisspoint, curve, distance, accuracy)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()
   
    if (mode == "png"):
        ims.write_to_png("kiss.png")

if __name__ == "__main__":
    main()