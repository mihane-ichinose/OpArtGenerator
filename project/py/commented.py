# Here are all commented code from main program app.py
# Depreciated feature or other commented codes appears below.


## Old method to pass in arguments in Python program

# parser = argparse.ArgumentParser()
    # parser.add_argument("-sa", "--shapealpha", default=1, type=float)
    # parser.add_argument("-m", "--mode", default="png", type=str)
    # Image output code decide which kind of op art: blaze / doublequad / parallelogram
    # parser.add_argument("-im", "--image", default="blaze", type=str)

    # Double quadratic
    # parser.add_argument("-minw", "--minwidth", default=1, type=int)
    # parser.add_argument("-maxw", "--maxwidth", default=10, type=int)
    # parser.add_argument("-l", "--valley", default=24, type=int)
    # parser.add_argument("-n", "--num", default=38, type=int)
    # parser.add_argument("-o", "--offset", default=2, type=float)
    # Shape - square / dot / parallelogram
    # parser.add_argument("-sh", "--shape", default="square", type=str)
    
    # Blaze study
    # parser.add_argument("-cr", "--circleradius", default=[400, 600, 1000, 1400, 1800, 2200], type=list)
    # parser.add_argument("-cc", "--circlecentre", default=[(3000,3000), (2900,2800), (2800,2700), (2700,2600), (2600,2700), (2500,2800)], type=list)
    # parser.add_argument("-ao", "--angleoffset", default=[0, 300, 340, 320, 350, 320], type=list)

    # Parallelogram
    # parser.add_argument("-st", "--stripes", default=20, type=int)
    # parser.add_argument("-ih", "--height", default=369, type=int)
    # parser.add_argument("-si", "--side", default=20, type=int)
    # parser.add_argument("-sw", "--stripew", default=20, type=int)

    # Public arguments
    # parser.add_argument("-a", "--angle", default=30, type=int)

    # Colour pattern - check / gradient / random
    # parser.add_argument("-cp", "--colourpattern", default="check", type=str)
    # parser.add_argument("-gp", "--gradientpoint", default=-1, type=int)
    # parser.add_argument("-gw", "--gradientwidth", default=1, type=int)
    # parser.add_argument("-gd", "--gradientdelta", default=0.8, type=float)
    # parser.add_argument("-ap", "--adjacentprobability", default=0.1, type=float)
    # parser.add_argument("-an", "--adjacentnums", default=[4,5], type=list)
    # parser.add_argument("-zn", "--zebranums", default=[2,3], type=list)

    # args, unknown = parser.parse_known_args()


## Old method to output each image type individually.

    # SVG output mode
    # if (image == "doublequad"):
    #     if (colourpattern == "check"):
    #         if (shape == "square"):
    #             svg = cairo.SVGSurface("square_check_quadratic.svg", width, height)
    #         elif (shape == "dot"):
    #             svg = cairo.SVGSurface("dot_check_quadratic.svg", width, height)
    #         elif (shape == "parallelogram"):
    #             svg = cairo.SVGSurface("para_check_quadratic.svg", width, height)
    #     elif (colourpattern == "gradient"):
    #         if (shape == "square"):
    #             svg = cairo.SVGSurface("square_gradient_quadratic.svg", width, height)
    #         elif (shape == "dot"):
    #             svg = cairo.SVGSurface("dot_gradient_quadratic.svg", width, height)
    #         elif (shape == "parallelogram"):
    #             svg = cairo.SVGSurface("para_gradient_quadratic.svg", width, height)
    #     elif (colourpattern == "random"):
    #         if (shape == "square"):
    #             svg = cairo.SVGSurface("square_random_quadratic.svg", width, height)
    #         elif (shape == "dot"):
    #             svg = cairo.SVGSurface("dot_random_quadratic.svg", width, height)
    #         elif (shape == "parallelogram"):
    #             svg = cairo.SVGSurface("para_random_quadratic.svg", width, height)
    # elif (image == "blaze"):
    #     if (colourpattern == "check"):
    #         svg = cairo.SVGSurface("blaze_check.svg", width, height)
    # elif (image == "parallelogram"):
    #     if (colourpattern == "random"):
    #         svg = cairo.SVGSurface("parallelogram_random.svg", width, height)
    #     elif (colourpattern == "check"):
    #         svg = cairo.SVGSurface("parallelogram_check.svg", width, height)
    # cr = cairo.Context(svg)

    # PNG output mode
    # if (mode == "png"):
    #     if (image == "doublequad"):
    #         if (colourpattern == "check"):
    #             if (shape == "square"):
    #                 ims.write_to_png("square_check_quadratic.png")
    #             elif (shape == "dot"):
    #                 ims.write_to_png("dot_check_quadratic.png")
    #             elif (shape == "parallelogram"):
    #                 ims.write_to_png("para_check_quadratic.png")
    #         elif (colourpattern == "gradient"):
    #             if (shape == "square"):
    #                 ims.write_to_png("square_gradient_quadratic.png")
    #             elif (shape == "dot"):
    #                 ims.write_to_png("dot_gradient_quadratic.png")
    #             elif (shape == "parallelogram"):
    #                 ims.write_to_png("para_gradient_quadratic.png")
    #         elif (colourpattern == "random"):
    #             if (shape == "square"):
    #                 ims.write_to_png("square_random_quadratic.png")
    #             elif (shape == "dot"):
    #                 ims.write_to_png("dot_random_quadratic.png")
    #             elif (shape == "parallelogram"):
    #                 ims.write_to_png("para_random_quadratic.png")
    #     elif (image == "blaze"):
    #         if (colourpattern == "check"):
    #             ims.write_to_png("blaze_check.png")
    #     elif (image == "parallelogram"):
    #         if (colourpattern == "random"):
    #             ims.write_to_png("parallelogram_random.png")
    #         elif (colourpattern == "check"):
    #             ims.write_to_png("parallelogram_check.png")
