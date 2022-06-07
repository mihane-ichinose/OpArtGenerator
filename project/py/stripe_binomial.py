## A sample painting of blue and red stripes with width alternates by binomial distribution.
## Not working nicely (too large variation in the middle but no change at end points).
## A quadratic function could work better.
import cairo, argparse, math
from scipy.stats import binom

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
    parser.add_argument("-n", "--stripes", default=30, type=int)
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-m", "--mode", default="png", type=str)
    parser.add_argument("-g", "--gap", default=2, type=int)
    parser.add_argument("-a", "--amplitude", default=500, type=int)
    parser.add_argument("-maxw", "--maxwidth", default=1000, type=int)
    
    args = parser.parse_args()

    stripes = args.stripes

    shapealpha = args.shapealpha

    mode = args.mode

    gap = args.gap

    amplitude = args.amplitude

    maxwidth = args.maxwidth

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

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("stripe_binomial.svg", width, height)
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
        ims.write_to_png("stripe_binomial.png")

def printShape(h, height, stripew, cr):
    shape = stripev(h, height, stripew)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

if __name__ == "__main__":
    main()