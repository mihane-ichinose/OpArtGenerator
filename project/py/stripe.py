# This file now merges stripe_binomial.py, stripe_quadratic and stripev.py together into one.

import cairo, argparse, random, math
from scipy.stats import binom

# decimal: decimal places for random possibilities between 0 and 1
def randomP(decimal):
    return round(random.uniform(0.0, 1.0),decimal)

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

# x_orig: starting point, top left
# stripeh: height of the stripe
# stripew: width of the stripe
def stripeh(y_orig, stripeh, stripew):
    y = y_orig

    sh = []

    # Four vertices
    sh.append((0, y))

    y += stripew
    sh.append((0, y))
    
    sh.append((stripeh, y))

    y -= stripew
    sh.append((stripeh, y))

    sh.append((0, y))

    return sh

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-m", "--mode", default="png", type=str)
    # Public
    parser.add_argument("-n", "--stripes", default=200, type=int)
    parser.add_argument("-o", "--orientation", default="H", type=str)
    parser.add_argument("-sh", "--shape", default="quadratic", type=str)
    # Normal
    parser.add_argument("-sw", "--stripew", default=8, type=int)
    parser.add_argument("-ap", "--adjacentprobability", default=0, type=float)
    parser.add_argument("-an", "--adjacentnums", default=[2,3,4], type=list)
    parser.add_argument("-cw", "--colourweights", default=[0.3,0.3,0.3,0.05,0.05], type=list)
    # Binomial and quadratic
    parser.add_argument("-g", "--gap", default=0, type=int)
    parser.add_argument("-maxw", "--maxwidth", default=5, type=int)
    # Binomial
    parser.add_argument("-a", "--amplitude", default=500, type=int)
    # Quadratic
    parser.add_argument("-minw", "--minwidth", default=1, type=int)
    
    args = parser.parse_args()

    shapealpha = args.shapealpha
    mode = args.mode

    stripes = args.stripes
    orientation = args.orientation

    # Normal, binomial or quadratic
    shape = args.shape

    stripew= args.stripew
    adjacentprobability = args.adjacentprobability
    ADJACENT = args.adjacentnums
    colourweights = args.colourweights

    gap = args.gap
    maxwidth = args.maxwidth

    amplitude = args.amplitude

    minwidth = args.minwidth

    if shape == "normal":
        # Width of the image decided by number of elements
        width = stripew * stripes
        height = width
    elif shape == "binomial":
        # Binomial distribution
        n = stripes
        p = 0.5 # Symmetrical

        data = list(range(n))

        distribution = [binom.pmf(i, n, p) for i in data]

        # Set up a list for stripe widths with scaled distribution values
        stripews = []
        for d in distribution:
            if d*amplitude <= 1: stripews.append(1)
            elif d*amplitude > maxwidth: stripews.append(maxwidth)
            else: stripews.append(round(d*amplitude))

        # Width of the image decided by number of elements
        width = sum(stripews) + gap*stripes
        height = width
    elif shape == "quadratic":
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

    if shape == "normal":
        coloursRGB = [(255,0,0), # Red
        (255, 165, 0), # Orange
        (0,0,255), # Blue
        (0,0,0), # White
        (255,255,255) # Black
        ]
    elif shape == "binomial" or shape == "quadratic":
        coloursRGB = [(255,0,0), # Red
        (0,0,255), # Blue
        (255,255,255), # White, this is treated as blank stripes
        ]

    colours = []
    for colourRGB in coloursRGB:
        colours.append([e / 255 for e in colourRGB])

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        if shape == "normal":
            if orientation == "V":
                svg = cairo.SVGSurface("stripe_v.svg", width, height)
            elif orientation == "H":
                svg = cairo.SVGSurface("stripe_h.svg", width, height)
        elif shape == "binomial":
            if orientation == "V":
                svg = cairo.SVGSurface("stripe_binomial_v.svg", width, height)
            elif orientation == "H":
                svg = cairo.SVGSurface("stripe_binomial_h.svg", width, height)
        elif shape == "quadratic":
            if orientation == "V":
                svg = cairo.SVGSurface("stripe_quadratic_v.svg", width, height)
            elif orientation == "H":
                svg = cairo.SVGSurface("stripe_quadratic_h.svg", width, height)
        cr = cairo.Context(svg)
    

    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    if orientation == "V":
        upper_bound = width
        stripeh = height
    elif orientation == "H":
        upper_bound = height
        stripeh = width
    
    if shape == "normal":
        h = 0
        # Choose a colour with weighted possibilities
        colour = random.choices(population=colours, weights=colourweights, k=1)
        #random.randint(0, len(colours)-1)
        while (h < upper_bound):
            isAdjacent = randomP(2) < adjacentprobability
            # Probablity for adjacent stripes having same colour
            previous = colour
            while(previous[0] == colour[0]):
                colour = random.choices(population=colours, weights=colourweights, k=1)
            cr.set_source_rgba(colour[0][0], colour[0][1], colour[0][2], shapealpha)
            for i in range (random.choice(ADJACENT)):
                printShape(h, stripeh, stripew, orientation, cr)
                h += stripew
                if (not isAdjacent): break
    elif shape == "binomial" or shape == "quadratic":
        h = 0
        index = 0
        while (h < width):
            if (index % 2 == 0):
                colour = colours[0] # Blue for even index
            else:
                colour = colours[1] # Red for odd index
            cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
            printShape(h, stripeh, stripews[index], orientation, cr)
            h += stripews[index]

            colour = colours[2] # White for gaps
            cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
            printShape(h, stripeh, gap, orientation, cr)
            h += gap

            index += 1
    if (mode == "png"):
        if shape == "normal":
            if orientation == "V":
                ims.write_to_png("stripe_v.png")
            elif orientation == "H":
                ims.write_to_png("stripe_h.png")
        elif shape == "binomial":
            if orientation == "V":
                ims.write_to_png("stripe_binomial_v.png")
            elif orientation == "H":
                ims.write_to_png("stripe_binomial_h.png")
        elif shape == "quadratic":
            if orientation == "V":
                ims.write_to_png("stripe_quadratic_v.png")
            elif orientation == "H":
                ims.write_to_png("stripe_quadratic_h.png")
        

def printShape(h, height, stripew, orientation, cr):
    if orientation == "V":
        shape = stripev(h, height, stripew)
    elif orientation == "H":
        shape = stripeh(h, height, stripew)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

if __name__ == "__main__":
    main()