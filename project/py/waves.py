import cairo, argparse, random, math
from scipy.stats import binom

coloursRGB = [(255, 255, 255), # White
(0,0,0), # Black
]

colours = []
for colourRGB in coloursRGB:
    colours.append([e / 255 for e in colourRGB])

# decimal: decimal places for random possibilities between 0 and 1
def randomP(decimal):
    return round(random.uniform(0.0, 1.0),decimal)

# x_orig: starting point, top left
def waves(x_orig, amplitude, period, verticaloffset, horizontaloffset, width, accuracy):
    a = amplitude
    p = period
    v = verticaloffset
    h = horizontaloffset

    # Add points on the sine wave by math sine function
    x = x_orig
    sin_points = []
    # Add top curve
    while x <= width:
        y = a*math.sin(p*(x+h))+v
        sin_points.append((x, y))
        x += accuracy
    # Add bottom curve
    x -= accuracy
    while x >= 0:
        y = a*math.sin(p*(x+2*h))+2*v+2
        sin_points.append((x, y))
        x -= accuracy
    # End to end
    x += accuracy
    sin_points.append((x, a*math.sin(p*(x+h))+v))
    return sin_points

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--amplitude", default=4, type=float)
    parser.add_argument("-p", "--period", default=0.05, type=float)
    parser.add_argument("-vo", "--verticaloffset", default=4, type=int)
    parser.add_argument("-ho", "--horizontaloffset", default=-10, type=int)
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-w", "--width", default=500, type=int)
    parser.add_argument("-m", "--mode", default="png", type=str)
    parser.add_argument("-acc", "--accuracy", default=0.1, type=float)
    parser.add_argument("-gd", "--gradientdelta", default=0.002, type=float)
    parser.add_argument("-rg", "--isredgradient", default=True, type=bool)
    parser.add_argument("-gg", "--isgreengradient", default=False, type=bool)
    parser.add_argument("-bg", "--isbluegradient", default=False, type=bool)
    
    args = parser.parse_args()

    

    shapealpha = args.shapealpha

    mode = args.mode

    width = args.width

    amplitude = args.amplitude
    period = args.period
    verticaloffset = args.verticaloffset
    horizontaloffset = args.horizontaloffset
    accuracy = args.accuracy

    gradientdelta = args.gradientdelta
    isredgradient = args.isredgradient
    isgreengradient = args.isgreengradient
    isbluegradient = args.isbluegradient

    height = width

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("waves.svg", width, height)
        cr = cairo.Context(svg)
    

    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    index = 0
    v = 0
    h = 0
    while (v <= height):
        if (index % 2 == 0):
            colour = colours[0] # White for even index
        else:
            colour = colours[1] # Black for odd index
        #cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
        #colour = colours[2] # Black
        r = colour[0]
        g = colour[1]
        b = colour[2]
        gradient = (height/2-abs(v-height/2))*gradientdelta
        # Add colour gradient for r/g/b
        if isredgradient:
            r += gradient
        if isgreengradient:
            g += gradient
        if isbluegradient:
            b += gradient
        cr.set_source_rgba(r, g, b, shapealpha)
        printShape(0, amplitude, period, v, h, width, accuracy, cr)

        index += 1
        v += verticaloffset
        h += horizontaloffset
    if (mode == "png"):
        ims.write_to_png("waves.png")

def printShape(x_orig, amplitude, period, verticaloffset, horizontaloffset, length, accuracy, cr):
    shape = waves(x_orig, amplitude, period, verticaloffset, horizontaloffset, length, accuracy)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

if __name__ == "__main__":
    main()