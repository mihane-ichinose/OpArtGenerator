import cairo, argparse, math

coloursRGB = [(255,0,0), # Red
(0,0,255), # Blue
(255,255,255), # White, this is treated as blank stripes
]

colours = []
for colourRGB in coloursRGB:
    colours.append([e / 255 for e in colourRGB])

# x_orig: starting point, top left
# stripeh: height of the stripe
# stripew: width of the stripe
def stripev(x_orig, stripeh, stripew):
    x = x_orig

    sv = []

    # Four vertices
    sv.append((x, 0))

    sv.append((x, stripeh))

    x += stripew
    sv.append((x, stripeh))

    sv.append((x, 0))

    x -= stripew
    sv.append((x, 0))

    return sv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--stripes", default=70, type=int)
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-m", "--mode", default="png", type=str)
    parser.add_argument("-g", "--gap", default=2, type=int)
    parser.add_argument("-minw", "--minwidth", default=1, type=int)
    parser.add_argument("-maxw", "--maxwidth", default=5, type=int)
    
    args = parser.parse_args()

    stripes = args.stripes

    shapealpha = args.shapealpha

    mode = args.mode

    gap = args.gap

    minwidth = args.minwidth

    maxwidth = args.maxwidth

    # Quadratic Function
    # We know the graph passes (0, minwidth) and (midpoint, maxwidth)
    # Here we treat c as minwidth, h as midpoint and k as maxwidth
    # So as a(x-h)^2+k passes (0,c), a = (c-k)/h^2 since h > 0
    n = stripes
    c = minwidth
    h = (n - 1) / 2 # h = -b/2a
    k = maxwidth # k = f(h)
    a = (c - k) / (h ** 2)

    data = list(range(n))

    quadratic = [a*((x-h)**2) + k for x in data]

    # Set up a list for stripe widths with quadratic values
    stripews = [round(q) for q in quadratic]

    # Width of the image decided by number of elements
    width = sum(stripews) + gap*stripes
    height = width

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("stripe_quadratic.svg", width, height)
        cr = cairo.Context(svg)
    

    cr.set_source_rgb(.9, .9, .9)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    h = 0
    index = 0
    while (h < width):
        if (index % 2 == 0):
            colour = colours[0] # Blue for even index
        else:
            colour = colours[1] # Red for odd index
        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
        printShape(h, height, stripews[index], cr)
        h += stripews[index]

        colour = colours[2] # White for gaps
        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
        printShape(h, height, gap, cr)
        h += gap

        index += 1
    if (mode == "png"):
        ims.write_to_png("stripe_quadratic.png")

def printShape(h, height, stripew, cr):
    shape = stripev(h, height, stripew)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

if __name__ == "__main__":
    main()