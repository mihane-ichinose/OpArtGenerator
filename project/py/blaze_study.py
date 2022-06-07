import cairo, argparse, math

coloursRGB = [(0,0,0), # Black
(255,255,255), # White, this is treated as blank stripes
]

colours = []
for colourRGB in coloursRGB:
    colours.append([e / 255 for e in colourRGB])

# x_orig: starting point, top left
# stripeh: height of the stripe
# stripew: width of the stripe
def blaze_stripe(orig, circleradius, circlecentre, angleoffset, angle):

    bs = []
    bs.append(orig)

    # Vertices add by number of circles
    for i in range (len(circleradius)):
        bs.append((circlecentre[i][0] + circleradius[i]*math.sin(math.radians(angleoffset[i])),
            circlecentre[i][1] - circleradius[i]*math.cos(math.radians(angleoffset[i]))))
        angleoffset[i] += angle
    # And go back
    for i in range (len(circleradius)):
        bs.append((circlecentre[len(circleradius)-i-1][0]
            + circleradius[len(circleradius)-i-1]*math.sin(math.radians(angleoffset[len(circleradius)-i-1])),
            circlecentre[len(circleradius)-i-1][1]
            - circleradius[len(circleradius)-i-1]*math.cos(math.radians(angleoffset[len(circleradius)-i-1]))))

    bs.append(orig)
    return bs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cr", "--circleradius", default=[400, 600, 1000, 1400, 1800, 2200], type=list)
    parser.add_argument("-cc", "--circlecentre", default=[(3000,3000), (2900,2800), (2800,2700), (2700,2600), (2600,2700), (2500,2800)], type=list)
    parser.add_argument("-ao", "--angleoffset", default=[0, 300, 340, 320, 350, 320], type=list)
    parser.add_argument("-a", "--angle", default=5, type=int)
    parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    parser.add_argument("-m", "--mode", default="png", type=str)
    
    args = parser.parse_args()

    circleradius = args.circleradius
    circlecentre = args.circlecentre
    angleoffset = args.angleoffset
    angle = args.angle

    shapealpha = args.shapealpha

    mode = args.mode

    # Width of the image decided by number of elements
    width = 3*circleradius[len(circlecentre)-1]
    height = width

    if (mode == "png"):
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)
    elif (mode == "svg"):
        svg = cairo.SVGSurface("blaze_study.svg", width, height)
        cr = cairo.Context(svg)

    cr.set_source_rgb(1,1,1)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    a = 0
    index = 0
    while (a < 360):
        if (index % 2 == 0):
            colour = colours[0] # Black for even index
        else:
            colour = colours[1] # White for odd index
        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
        printShape(circlecentre[0], circleradius, circlecentre, angleoffset, angle, cr)

        a += angle
        index += 1

    if (mode == "png"):
        ims.write_to_png("blaze_study.png")

def printShape(orig, circleradius, circlecentre, angleoffset, angle, cr):
    shape = blaze_stripe(orig, circleradius, circlecentre, angleoffset, angle)
    cr.set_line_width(0)
    for i in range(len(shape)):
        cr.line_to(shape[i][0], shape[i][1])
    cr.fill()

    # Reach the outest point - needs segments
    circle_index = len(circlecentre) - 1
    # arc(x, y, radius, start_angle, end_angle)
    cr.arc(circlecentre[circle_index][0], circlecentre[circle_index][1], circleradius[circle_index],
        math.radians(angleoffset[circle_index]-angle), math.radians(angleoffset[circle_index]))
    cr.close_path()
    cr.fill()

if __name__ == "__main__":
    main()