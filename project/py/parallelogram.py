import cairo, argparse, random, math

float_gen = lambda a, b: random.uniform(a, b)

colours = []
for i in range(15):
    colours.append((float_gen(.2, .9), float_gen(.2, .9), float_gen(.2, .9)))

# decimal: decimal places for random possibilities between 0 and 1
def randomP(decimal):
    return round(random.uniform(0.0, 1.0),decimal)

# side: length of each parallelogram
# stripew: width of the stripe
# angle: angle of parallelogram
def parallelogram(x_orig, y_orig, side, stripew, angle):
    x = x_orig
    y = y_orig
    d = math.tan(angle * math.pi / 180) * stripew

    paral = []

    # Four vertices
    paral.append((x, y-1))

    y += side
    paral.append((x, y))

    x += stripew
    y -= d
    paral.append((x, y))

    y -= side
    paral.append((x, y-1))

    x -= stripew
    y += d
    paral.append((x, y-1))

    return paral

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--stripes", default=20, type=int)
    parser.add_argument("-ih", "--height", default=369, type=int)
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-s", "--side", default=20, type=int)
    parser.add_argument("-sw", "--stripew", default=20, type=int)
    parser.add_argument("-a", "--angle", default=30, type=int)
    parser.add_argument("-ap", "--adjacentprobability", default=0.1, type=float)
    parser.add_argument("-an", "--adjacentnums", default=[4,5], type=list)
    parser.add_argument("-zn", "--zebranums", default=[2,3], type=list)
    parser.add_argument("-m", "--mode", default="png", type=str)
    
    args = parser.parse_args()

    stripes = args.stripes

    shapealpha = args.shapealpha

    side, stripew, angle = args.side, args.stripew, args.angle

    adjacentprobability = args.adjacentprobability
    ADJACENT = args.adjacentnums
    ZEBRA = args.zebranums

    # Width of the image decided by number of elements
    width = stripew * stripes
    height = args.height

    mode = args.mode

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("parallelogram.svg", width, height)
        cr = cairo.Context(svg)
    
    cr.set_source_rgb(.9, .9, .9)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    stripe_index = 0
    for h in range(-int(width*.2), int(width*1.2), stripew):
        # v offset for shapes to line up
        offset = stripe_index*(side - math.tan(angle * math.pi / 180) * stripew)
        v = -int(height*2-offset)
        while v <= int(height*2):
            isAdjacent = randomP(2) < adjacentprobability
            isZebra = randomP(2) < adjacentprobability
            fstColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
            sndColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
            
            # Probablity for adjacent shapes having same colour or zebra pattern
            if(isAdjacent or isZebra):
                if(isZebra):
                    for i in range (random.choice(ZEBRA)):
                        cr.set_source_rgba(fstColour[0], fstColour[1], fstColour[2], shapealpha)
                        printShape(h, v, side, stripew, angle, cr)
                        v += side
                        cr.set_source_rgba(sndColour[0], sndColour[1], sndColour[2], shapealpha)
                        printShape(h, v, side, stripew, angle, cr)
                        v += side
                else:
                    cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                    for i in range (random.choice(ADJACENT)):
                        printShape(h, v, side, stripew, angle, cr)
                        v += side
            else:
                cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                printShape(h, v, side, stripew, angle, cr)
                v += side
        stripe_index += 1
    if (mode == "png"):
        ims.write_to_png("parallelogram.png")

def printShape(h, v, side, stripew, angle, cr):
    shape = parallelogram(h, v, side, stripew, angle)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

if __name__ == "__main__":
    main()