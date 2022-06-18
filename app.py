# The universal library of Op Art Generator and Animator
# Now contains: Double quadratic, blaze study, parallelogram, kiss, waves and stripes.

import random, math
# Use CFFI version - cairocffi instead of normal PyCairo library for heroku deployment.
import cairocffi as cairo
from scipy.stats import binom
from flask import Flask, render_template, request

app = Flask(__name__)

float_gen = lambda a, b: random.uniform(a, b)

imageType = 'undefined'
mode = 'undefined'

# decimal: decimal places for random possibilities between 0 and 1
def randomP(decimal):
    return round(random.uniform(0.0, 1.0),decimal)

## Below are basic shapes for print use
# ellipseh: height of ellipse
# ellipsew: width of ellipse
def ellipse(x_orig, y_orig, ellipseh, ellipsew):
    # An ellipse with focuses on y-axis
    # (y-k)^2/a^2 + (x-h)^2/b^2 = 1
    h = x_orig
    k = y_orig
    a = ellipseh
    b = ellipsew

    elli = []

    for x in range(-b+h, b+h+1):
        y = math.sqrt((1 - ((x - h) ** 2) / (b ** 2)) * (a ** 2)) + k
        elli.append((x, y))
    
    for x in range(b+h, -b+h-1, -1):
        y = -math.sqrt((1 - ((x - h) ** 2) / (b ** 2)) * (a ** 2)) + k
        elli.append((x, y))
    
    return elli

# x_orig, y_orig: starting point, top left
# recth: height of the rectangle
# rectw: width of the rectangle
def rect(x_orig, y_orig, recth, rectw):
    x = x_orig
    y = y_orig

    rt = []

    # Four vertices
    rt.append((x, y))

    rt.append((x, y+recth))

    x += rectw
    rt.append((x, y+recth))

    rt.append((x, y))

    x -= rectw
    rt.append((x, y))

    return rt

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

def kiss(height, base, kisspoint, curve, distance, accuracy):
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
    kiss = []
    # Add top curve
    while x <= w:
        y = a*((x-h)**2)+k
        kiss.append((x, y))
        x += accuracy
    # Add bottom horizontal line
    kiss.append((w, base))
    kiss.append((0, base))
    kiss.append((0, a*(h**2)+k)) # x = 0 in quadratic function

    return kiss

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

@app.route('/home', methods = ['POST', 'GET'])
def home():
    
    return render_template("index.html",
    graph="img/home_img.jpg")

@app.route('/selectType', methods = ['POST', 'GET'])
def selectType():
    global imageType
    imageType = request.args.get('imageType')
    initShapeAlpha = 100

    if imageType == 'parallelogram':
        return render_template("parallelogram.html",
        initShapeAlpha=initShapeAlpha,
        initAngle=45,
        initStripes=20,
        initHeight=400,
        initSide=20,
        initStripeWidth=20,
        colourPattern="random",
        initAdjacentProbability=10,
        initAdjacentNums="4 5",
        initZebraNums="2 3",
        graph="img/home_img.jpg")
    elif imageType == 'blaze':
        return render_template("blaze.html",
        initShapeAlpha=initShapeAlpha,
        initAngle=5,
        initCircleRadius=[400, 600, 1000, 1400, 1800, 2200],
        initCircleCentre=[(3000,3000), (2900,2800), (2800,2700), (2700,2600), (2600,2700), (2500,2800)],
        initAngleOffset=[0, 300, 340, 320, 350, 320],
        initInsertNum=6,
        graph="img/home_img.jpg")
    elif imageType == 'doublequad':
        return render_template("doublequad.html",
        initShapeAlpha=initShapeAlpha,
        initMinWidth=1,
        initMaxWidth=10,
        initValley=24,
        initNum=38,
        initOffset=2,
        shape="square",
        initAngle=30,
        colourPattern="check",
        initGradientPoint=3,
        initGradientWidth=5,
        initGradientDelta=90,
        initAdjacentProbability=10,
        initAdjacentNums="4 5",
        initZebraNums="2 3",
        formulaLeftMsg="N/A".encode('utf-8'),
        formulaRightMsg="N/A".encode('utf-8'),
        isAnimator=False,
        initImgs = 10,
        initInterval = 0.4,
        isValley = True,
        initValleyStep = 1,
        isGradientPoint = False,
        initGradientPointStep = 1,
        graph="img/home_img.jpg")
    elif imageType == 'kiss':
        return render_template("kiss.html",
        initShapeAlpha=initShapeAlpha,
        initHeight=2500,
        initBase=1500,
        initKissPoint=1000,
        initCurve=0.1,
        initDistance=1,
        initAccuracy=0.1,
        formulaMsg="N/A".encode('utf-8'),
        graph="img/home_img.jpg")
    elif imageType == "waves":
        return render_template("waves.html",
        initShapeAlpha=initShapeAlpha,
        initWidth=500,
        initAmplitude=4,
        initPeriod=0.05,
        initVerticalOffset=4,
        initHorizontalOffset=-10,
        initAccuracy=0.1,
        initGradientDelta=70,
        isRedGradient=True,
        isGreenGradient=False,
        isBlueGradient=False,
        formulaTopMsg="N/A".encode('utf-8'),
        formulaBottomMsg="N/A".encode('utf-8'),
        graph="img/home_img.jpg")
    elif imageType == "stripes":
        return render_template("stripes.html",
        initShapeAlpha=initShapeAlpha,
        initStripes=200,
        orientation="V",
        shape="normal",
        initStripew=8,
        initColourWeights="0.3 0.3 0.3 0.05 0.05",
        initAdjacentProbability=10,
        initAdjacentNums="2 3 4",
        initGap=2,
        initMaxWidth=5,
        initAmplitude=500,
        initMinWidth=1,
        formulaBinomialMsg="N/A".encode('utf-8'),
        formulaQuadraticMsg="N/A".encode('utf-8'),
        graph="img/home_img.jpg")

@app.route('/output', methods = ['POST', 'GET'])
def output():
    global mode
    # Public arguments here
    shapealpha = request.form.get('shapeAlpha_input', type=int)/100
    mode = request.form['mode_input']
    image = imageType

    ## Arguments for each different image type
    #  Double quadratic
    if image == "doublequad":
        minwidth = request.form.get('minWidth_input', type=int)
        maxwidth = request.form.get('maxWidth_input', type=int)
        # Valley, also known as numbers of rectangles on the left
        valley = request.form.get('valley_input', type=int)
        # Total index, number of rectangles
        num = request.form.get('num_input', type=int)
        # Power by offset times make the variance greater hence image feels more 3D
        offset = request.form.get('offset_input', type=int)
        # Set to either 'square' or 'dot' for different shape pattern
        shape = request.form['shape_input']
        angle = request.form.get('angle_input', type=int)
        # Animator part
        isanimator = request.form.get('isAnimator_input', type=bool)
        imgs = request.form.get('imgs_input', type=int)
        interval = request.form.get('interval_input', type=float)
        isvalley = request.form.get('isValley_input', type=bool)
        valleystep = request.form.get('valleyStep_input', type=int)
        isgradientpoint = request.form.get('isGradientPoint_input', type=bool)
        gradientpointstep = request.form.get('gradientPointStep_input', type=int)
    
    # Blaze study
    if image == "blaze":
        circleradius = request.form.getlist('circleRadius_input', type=int)
        circlecentre = list(zip(request.form.getlist('circleCentreX_input', type=int),
                        request.form.getlist('circleCentreY_input', type=int)))
        angleoffset = request.form.getlist('angleOffset_input', type=int)
        insertnum = request.form.get('insertNum_input', type=int)
        angle = request.form.get('angle_input', type=int)

    # Parallelogram
    if image == "parallelogram":
        stripes = request.form.get('stripes_input', type=int)
        height = request.form.get('height_input', type=int)
        side = request.form.get('side_input', type=int)
        stripew = request.form.get('stripeWidth_input', type=int)
        angle = request.form.get('angle_input', type=int)

    # Kiss
    if image == "kiss":
        # height: height of the image
        height = request.form.get('height_input', type=int)
        # base: the distance between horizontal line and top of the image
        base = request.form.get('base_input', type=int)
        # kisspoint: x point where the lowest point of curve is reached
        kisspoint = request.form.get('kissPoint_input', type=int)
        # curve: parameter 'a' of quadratic function
        curve = request.form.get('curve_input', type=float)
        # distance: the distance between horizontal line and lowest point
        distance = request.form.get('distance_input', type=int)
        # accuracy: step of x
        accuracy = request.form.get('accuracy_input', type=float)

    # Waves
    if image == "waves":
        # width: width of the image
        width = request.form.get('width_input', type=int)
        # Four parameters for sine waves
        amplitude = request.form.get('amplitude_input', type=float)
        period = request.form.get('period_input', type=float)
        verticaloffset = request.form.get('verticalOffset_input', type=int)
        horizontaloffset = request.form.get('horizontalOffset_input', type=int)
        # accuracy: step of x
        accuracy = request.form.get('accuracy_input', type=float)
        # the three booleans below decide gradient colour
        isredgradient = request.form.get('isRedGradient_input', type=bool)
        isgreengradient = request.form.get('isGreenGradient_input', type=bool)
        isbluegradient = request.form.get('isBlueGradient_input', type=bool)
    
    # Stripes
    if image == "stripes":
        stripes = request.form.get('stripes_input', type=int)
        orientation = request.form['orientation_input']
        shape = request.form['shape_input']
        # Normal
        stripew= request.form.get('stripew_input', type=int)
        colourweights = list(map(float, request.form['colourWeights_input'].split()))
        adjacentprobability = request.form.get('adjacentProbability_input', type=float)/100
        ADJACENT = list(map(int, request.form['adjacentNums_input'].split()))
        # Binomial and quadratic
        gap = request.form.get('gap_input', type=int)
        maxwidth = request.form.get('maxWidth_input', type=int)
        # Binomial
        amplitude = request.form.get('amplitude_input', type=int)
        # Quadratic
        minwidth = request.form.get('minWidth_input', type=int)

    ## Colours
    # Colour pattern
    if image == "blaze":
        colourpattern = "check"
    elif image == "kiss":
        colourpattern = "blank"
    elif image == "waves":
        colourpattern = "gradient"
    elif image == "stripes":
        if shape == "normal":
            colourpattern = "fives"
        elif shape == "binomial" or shape == "quadratic":
            colourpattern = "redBlueGaps"
    else:
        colourpattern = request.form['colourPattern_input']
    # Required when colour pattern set to 'gradient'
    if image == "doublequad":
        gradientpoint = request.form.get('gradientPoint_input', type=int)
        gradientwidth = request.form.get('gradientWidth_input', type=int)
        gradientdelta = request.form.get('gradientDelta_input', type=int)/100
    # Required when colour pattern set to 'random'
    if image == "doublequad" or image == "parallelogram":
        adjacentprobability = request.form.get('adjacentProbability_input', type=int)/100
        ADJACENT = list(map(int, request.form['adjacentNums_input'].split()))
        ZEBRA = list(map(int, request.form['zebraNums_input'].split()))
    if image == "waves":
        gradientdelta = request.form.get('gradientDelta_input', type=int)/100

    # Colour adjustments
    colours = []
    
    # Colours to be added definetely
    if colourpattern == "check" or colourpattern == "gradient":
        coloursRGB = [(255,255,255), # White
        (0,0,0), # Black
        ]
    elif colourpattern == "blank":
        coloursRGB = [(255,255,255)] # White
    elif colourpattern == "fives":
        coloursRGB = [(255,0,0), # Red
        (255, 165, 0), # Orange
        (0,0,255), # Blue
        (0,0,0), # White
        (255,255,255) # Black
        ]
    elif colourpattern == "redBlueGaps":
        coloursRGB = [(255,0,0), # Red
        (0,0,255), # Blue
        (255,255,255), # White, this is treated as blank stripes
        ]
    
    # Way to add colours - defined or randomised
    if colourpattern == "random":
        for i in range(15):
            colours.append((float_gen(.2, .9), float_gen(.2, .9), float_gen(.2, .9)))
    else:
        for colourRGB in coloursRGB:
            colours.append([e / 255 for e in colourRGB])
    if image != "doublequad":
        imgs = 0
    else:
        if not isanimator:
            imgs = 0
    for animateIndex in range(0, imgs+1):
        # Define size of the image, and its logical behaviour.
        if image == "doublequad":
            # Quadratic Function
            # Case 1: x <= valley point - 1 (l)
            # h = 0, the graph passes (0, maxwidth) and (l, minwidth)
            # As ax^2+k passes (l, minwidth), a = (minwidth-k)/l^2 since h = 0
            # Case 2: x > valley point - 1 (l)
            # h = width, the graph passes (l, minwidth) and (rects, maxwidth)
            # As a(x-rects)^2+k passes (l, minwidth), a = (minwidth-k)/(l-rects)^2 since h = rects
            l = valley - 1
            k = maxwidth

            data1 = list(range(l+1))
            data2 = list(range(l+1,num))
            
            # Set up lists for two shape widths with quadratic values
            if l <= 0:
                l = 0
                valley = 1

                a1 = 0
                quadratic1 = [0]
                ws1 = [0]

                a2 = (minwidth-k) / ((l-num+1)**2)
                quadratic2 = [a2*((x-num+1)**2) + k for x in data2]
                ws2 = [math.ceil(q**offset) for q in quadratic2 if q > 0]
            elif l >= num - 1:
                l = num - 1
                valley = num

                a1 = (minwidth-k) / (l**2)
                quadratic1 = [a1*(x**2) + k for x in data1]
                ws1 = [math.ceil(q**offset) for q in quadratic1 if q > 0]

                a2 = 0
                quadratic2 = [0]
                ws2 = [0]
            else:
                a1 = (minwidth-k) / (l**2)
                quadratic1 = [a1*(x**2) + k for x in data1]
                ws1 = [math.ceil(q**offset) for q in quadratic1 if q > 0]

                a2 = (minwidth-k) / ((l-num+1)**2)
                quadratic2 = [a2*((x-num+1)**2) + k for x in data2]
                ws2 = [math.ceil(q**offset) for q in quadratic2 if q > 0]
        
            # Width of the image decided by number of elements
            width = sum(ws1) + sum(ws2)
            if shape == "square":
                height = width
            elif shape == "dot":
                height = width + math.ceil(ws1[0]*0.4)
            elif shape == "parallelogram":
                height = width
        elif image == "blaze":
            width = max(circlecentre[len(circlecentre)-1][0] * 2,
                circlecentre[len(circlecentre)-1][0] + circleradius[len(circlecentre)-1])
            height = max(circlecentre[len(circlecentre)-1][1] * 2,
                circlecentre[len(circlecentre)-1][1] + circleradius[len(circlecentre)-1])
        elif image == "parallelogram":
            width = stripew * stripes
        elif image == "kiss":
            width = height
        elif image == "waves":
            height = width
        elif image == "stripes":
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
        
        # Image output mode
        if mode == "png":
            ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            cr = cairo.Context(ims)
        elif mode == "svg":
            if animateIndex == 0:
                svg = cairo.SVGSurface("static/out/output.svg", width, height)
            else:
                svg = cairo.SVGSurface("static/out/output"+str(animateIndex)+".svg", width, height)
            cr = cairo.Context(svg)
            
        if image == "kiss":
            # Background, default set to black in kiss
            cr.set_source_rgb(0, 0, 0)
        else:
            # Otherwise default set to white
            cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        # Output logic for each image type
        if (image == "doublequad"):
            v = 0
            while (v*round(maxwidth**offset) < 3*height):
                h = 0
                index = 0
                prev_o = 0
                while (index < num):
                    if (colourpattern == "check"):
                        if ((index+v) % 2 == 0):
                            colour = colours[0] # White for even index+v
                        else:
                            colour = colours[1] # Black for odd index+v
                        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                    elif (colourpattern == "gradient"):
                        if ((index+v) % 2 == 0):
                            colour = colours[0] # White for even index+v
                        else: # The index of the shape with gradient colours rather than black
                            gradient_index = (index-1)//2 - v//2 - gradientpoint
                            step = 1 / gradientwidth
                            if (gradient_index > -gradientwidth and gradient_index <= 0): # Gradient to white
                                colour = (gradientdelta * (gradientwidth+gradient_index) * step,
                                    gradientdelta * (gradientwidth+gradient_index) * step,
                                    gradientdelta * (gradientwidth+gradient_index) * step)
                            elif (gradient_index > 0 and gradient_index < gradientwidth): # Gradient to black
                                colour = (gradientdelta * (gradientwidth-gradient_index) * step,
                                    gradientdelta * (gradientwidth-gradient_index) * step,
                                    gradientdelta * (gradientwidth-gradient_index) * step)
                            else:
                                colour = colours[1] # Black for odd index+v
                        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                    elif (colourpattern == "random"):

                        isAdjacent = randomP(2) < adjacentprobability
                        isZebra = randomP(2) < adjacentprobability
                        fstColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
                        sndColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
                        
                        # Probablity for adjacent shapes having same colour or zebra pattern
                        if(isAdjacent or isZebra):
                            if(isZebra):
                                for i in range (random.choice(ZEBRA)):
                                    # Set no offset for squares and dots
                                    if (shape == "square" or shape == "dot"): prev_o = 0
                                    cr.set_source_rgba(fstColour[0], fstColour[1], fstColour[2], shapealpha)
                                    if (index < valley):
                                        if(ws1[index] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws1[index], angle, cr, shape)
                                            h += ws1[index]
                                            prev_o += math.tan(angle * math.pi / 180) * ws1[index]
                                            index += 1
                                            if index >= num: break
                                    else:
                                        if(ws2[index-valley] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws2[index-valley], angle, cr, shape)
                                            h += ws2[index-valley]
                                            prev_o += math.tan(angle * math.pi / 180) * ws2[index-valley]
                                            index += 1
                                            if index >= num: break
                                    # Set no offset for squares and dots
                                    if (shape == "square" or shape == "dot"): prev_o = 0
                                    cr.set_source_rgba(sndColour[0], sndColour[1], sndColour[2], shapealpha)
                                    if (index < valley):
                                        if(ws1[index] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws1[index], angle, cr, shape)
                                            h += ws1[index]
                                            prev_o += math.tan(angle * math.pi / 180) * ws1[index]
                                            index += 1
                                            if index >= num: break
                                    else:
                                        if(ws2[index-valley] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws2[index-valley], angle, cr, shape)
                                            h += ws2[index-valley]
                                            prev_o += math.tan(angle * math.pi / 180) * ws2[index-valley]
                                            index += 1
                                            if index >= num: break
                            else:
                                cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                                for i in range (random.choice(ADJACENT)):
                                    # Set no offset for squares and dots
                                    if (shape == "square" or shape == "dot"): prev_o = 0
                                    if (index < valley):
                                        if(ws1[index] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws1[index], angle, cr, shape)
                                            h += ws1[index]
                                            prev_o += math.tan(angle * math.pi / 180) * ws1[index]
                                            index += 1
                                            if index >= num: break
                                    else:
                                        if(ws2[index-valley] >= 0):
                                            printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws2[index-valley], angle, cr, shape)
                                            h += ws2[index-valley]
                                            prev_o += math.tan(angle * math.pi / 180) * ws2[index-valley]
                                            index += 1
                                            if index >= num: break
                        else:
                            # Set no offset for squares and dots
                            if (shape == "square" or shape == "dot"): prev_o = 0
                            cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                            if (index < valley):
                                if(ws1[index] >= 0):
                                    printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws1[index], angle, cr, shape)
                                    h += ws1[index]
                                    prev_o += math.tan(angle * math.pi / 180) * ws1[index]
                                    index += 1
                                    if index >= num: break
                            else:
                                if(ws2[index-valley] >= 0):
                                    printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws2[index-valley], angle, cr, shape)
                                    h += ws2[index-valley]
                                    prev_o += math.tan(angle * math.pi / 180) * ws2[index-valley]
                                    index += 1
                                    if index >= num: break
                    if (colourpattern == "check" or colourpattern == "gradient"):
                        # Set no offset for squares and dots
                        if (shape == "square" or shape == "dot"): prev_o = 0
                        if (index < valley):
                            if(ws1[index] >= 0):
                                printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws1[index], angle, cr, shape)
                                h += ws1[index]
                                prev_o += math.tan(angle * math.pi / 180) * ws1[index]
                                index += 1
                                if index >= num: break
                        else:
                            if(ws2[index-valley] >= 0):
                                printDoubleQuad(h, v*round(maxwidth**offset) - prev_o, round(maxwidth**offset), ws2[index-valley], angle, cr, shape)
                                h += ws2[index-valley]
                                prev_o += math.tan(angle * math.pi / 180) * ws2[index-valley]
                                index += 1
                                if index >= num: break
                v += 1
            
            # Toggle animator feature with steps
            if animateIndex != 0:
                if isvalley: valley += valleystep
                if isgradientpoint: gradientpoint += gradientpointstep

        elif (image == "blaze"):
            a = 0
            index = 0
            while (a < 360):
                if (colourpattern == "check"):
                    if (index % 2 == 0):
                        colour = colours[1] # Black for even index
                    else:
                        colour = colours[0] # White for odd index
                    cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                    printBlaze(circlecentre[0], circleradius, circlecentre, angleoffset, angle, cr)
                a += angle
                index += 1
        elif (image == "parallelogram"):
            stripe_index = 0
            for h in range(-int(width*.2), int(width*1.2), stripew):
                shape_index = 0
                # v offset for shapes to line up
                offset = stripe_index*(side - math.tan(angle * math.pi / 180) * stripew)
                v = -int(height*2-offset)
                while v <= int(height*2):
                    if (colourpattern == "random"):
                        isAdjacent = randomP(2) < adjacentprobability
                        isZebra = randomP(2) < adjacentprobability
                        fstColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
                        sndColour = [random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2]]
                        
                        # Probablity for adjacent shapes having same colour or zebra pattern
                        if(isAdjacent or isZebra):
                            if(isZebra):
                                for i in range (random.choice(ZEBRA)):
                                    cr.set_source_rgba(fstColour[0], fstColour[1], fstColour[2], shapealpha)
                                    printParallelogram(h, v, side, stripew, angle, cr)
                                    v += side
                                    cr.set_source_rgba(sndColour[0], sndColour[1], sndColour[2], shapealpha)
                                    printParallelogram(h, v, side, stripew, angle, cr)
                                    v += side
                            else:
                                cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                                for i in range (random.choice(ADJACENT)):
                                    printParallelogram(h, v, side, stripew, angle, cr)
                                    v += side
                        else:
                            cr.set_source_rgba(random.choice(colours)[0], random.choice(colours)[1], random.choice(colours)[2], shapealpha)
                            printParallelogram(h, v, side, stripew, angle, cr)
                            v += side
                    elif (colourpattern == "check"):
                        if (shape_index % 2 == 0):
                            colour = colours[1] # Black for even index
                        else:
                            colour = colours[0] # White for odd index
                        cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                        printParallelogram(h, v, side, stripew, angle, cr)
                        v += side
                    shape_index += 1
                stripe_index += 1
        elif (image == "kiss"):
            colour = colours[0] # White
            cr.set_source_rgba(colour[0], colour[1], colour[2],shapealpha)
            printKiss(height, base, kisspoint, curve, distance, accuracy, cr)
        elif (image == "waves"):
            index = 0
            v = 0
            h = 0
            while (v <= height):
                if (index % 2 == 0):
                    colour = colours[0] # White for even index
                    cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                else:
                    colour = colours[1] # Black with gradient for odd index
                    r = colour[0]
                    g = colour[1]
                    b = colour[2]
                    step = 1 / (height/2)
                    gradient = (height/2-abs(v-height/2))*gradientdelta*step
                    # Add colour gradient for r/g/b
                    if isredgradient:
                        r = gradient
                    if isgreengradient:
                        g = gradient
                    if isbluegradient:
                        b = gradient
                    cr.set_source_rgba(r, g, b, shapealpha)
                printWaves(0, amplitude, period, v, h, width, accuracy, cr)

                index += 1
                v += verticaloffset
                h += horizontaloffset
        elif image == "stripes":
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
                        printStripes(h, stripeh, stripew, orientation, cr)
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
                    printStripes(h, stripeh, stripews[index], orientation, cr)
                    h += stripews[index]

                    colour = colours[2] # White for gaps
                    cr.set_source_rgba(colour[0], colour[1], colour[2], shapealpha)
                    printStripes(h, stripeh, gap, orientation, cr)
                    h += gap

                    index += 1

        if mode == "png":
            if animateIndex == 0:
                ims.write_to_png("static/out/output.png")
            else:
                ims.write_to_png("static/out/output"+str(animateIndex)+".png")

    initShapeAlpha = request.form['shapeAlpha_input']
    if image == "doublequad" or image == "waves":
        gradientdelta = request.form.get('gradientDelta_input', type=float)
    
    if image == "doublequad":
        valley = request.form.get('valley_input', type=int)
        gradientpoint = request.form.get('gradientPoint_input', type=int)
        imgs = request.form.get('imgs_input', type=int)
        if num - valley + 1 < imgs:
            imgs = num - valley + 1
        if valley == 1:
            formulaLeftMsg = "N/A".encode('utf-8')
        else:
            formulaLeftMsg = ("\U0001D432="+str(round((minwidth-maxwidth)/((valley-1)**2), 2))+"\U0001D499\u00B2+"+str(maxwidth)).encode('utf-8')
        
        if valley == num:
            formulaRightMsg = "N/A".encode('utf-8')
        else:
            formulaRightMsg = ("\U0001D432="+str(round((minwidth-maxwidth)/((valley-num)**2), 2))+"(\U0001D499-"+str(num-1)+")\u00B2+"+str(maxwidth)).encode('utf-8')

    if image == "parallelogram" or image == "doublequad":
        initAdjacentProbability = int(adjacentprobability * 100)
        initAdjacentNums = request.form['adjacentNums_input']
        initZebraNums = request.form['zebraNums_input']
    elif image == "blaze":
        angleoffset = request.form.getlist('angleOffset_input', type=int)
    elif image == "waves":
        if horizontaloffset > 0:
            # (x+h)
            hTStr = "(\U0001D499+" + str(horizontaloffset) + ")"
            hBStr = "(\U0001D499+" + str(2*horizontaloffset) + ")"
        elif horizontaloffset == 0:
            # x
            hTStr = "\U0001D499"
            hBStr = "\U0001D499"
        else:
            # (x-h)
            hTStr = "(\U0001D499" + str(horizontaloffset) + ")"
            hBStr = "(\U0001D499" + str(2*horizontaloffset) + ")"
    elif image == "stripes":
        initAdjacentProbability = int(adjacentprobability * 100)
        initAdjacentNums = request.form['adjacentNums_input']
        initColourWeights = request.form['colourWeights_input']

    # Output for python flask
    if image == 'parallelogram':
        return render_template("parallelogram.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initAngle=angle,
        initStripes=stripes,
        initHeight=height,
        initSide=side,
        initStripeWidth=stripew,
        colourPattern=colourpattern,
        initAdjacentProbability=initAdjacentProbability,
        initAdjacentNums=initAdjacentNums,
        initZebraNums=initZebraNums,
        graph="out/output."+mode)
    elif image == 'blaze':
        return render_template("blaze.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initAngle=angle,
        initCircleRadius=circleradius,
        initCircleCentre=circlecentre,
        initAngleOffset=angleoffset,
        initInsertNum=insertnum,
        graph="out/output."+mode)
    elif image == 'doublequad':
        return render_template("doublequad.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initMinWidth=minwidth,
        initMaxWidth=maxwidth,
        initValley=valley,
        initNum=num,
        initOffset=offset,
        shape=shape,
        initAngle=angle,
        colourPattern=colourpattern,
        initGradientPoint=gradientpoint,
        initGradientWidth=gradientwidth,
        initGradientDelta=gradientdelta,
        initAdjacentProbability=initAdjacentProbability,
        initAdjacentNums=initAdjacentNums,
        initZebraNums=initZebraNums,
        formulaLeftMsg=formulaLeftMsg,
        formulaRightMsg=formulaRightMsg,
        isAnimator=isanimator,
        initImgs = imgs,
        initInterval = interval,
        isValley=isvalley,
        initValleyStep = valleystep,
        isGradientPoint = isgradientpoint,
        initGradientPointStep = gradientpointstep,
        graph="out/output."+mode)
    elif imageType == 'kiss':
        return render_template("kiss.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initHeight=height,
        initBase=base,
        initKissPoint=kisspoint,
        initCurve=curve,
        initDistance=distance,
        initAccuracy=accuracy,
        formulaMsg=("\U0001D432="+str(curve/1000)+"(\U0001D499-"+str(kisspoint)+")\u00B2-"+str(base-distance)).encode('utf-8'),
        graph="out/output."+mode)
    elif imageType == "waves":
        return render_template("waves.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initWidth=width,
        initAmplitude=amplitude,
        initPeriod=period,
        initVerticalOffset=verticaloffset,
        initHorizontalOffset=horizontaloffset,
        initAccuracy=accuracy,
        initGradientDelta=gradientdelta,
        isRedGradient=isredgradient,
        isGreenGradient=isgreengradient,
        isBlueGradient=isbluegradient,
        formulaTopMsg=("\U0001D432="+str(amplitude)+"sin("+str(period)+hTStr+")+"+str(verticaloffset)).encode('utf-8'),
        formulaBottomMsg=("\U0001D432="+str(amplitude)+"sin("+str(period)+hBStr+")+"+str(2*verticaloffset+2)).encode('utf-8'),
        graph="out/output."+mode)
    elif imageType == "stripes":
        return render_template("stripes.html",
        mode=mode,
        initShapeAlpha=initShapeAlpha,
        initStripes=stripes,
        orientation=orientation,
        shape=shape,
        initStripew=stripew,
        initColourWeights=initColourWeights,
        initAdjacentProbability=initAdjacentProbability,
        initAdjacentNums=initAdjacentNums,
        initGap=gap,
        initMaxWidth=maxwidth,
        initAmplitude=amplitude,
        initMinWidth=minwidth,
        formulaBinomialMsg=("\U0001D432=\U0001D4D2("+str(stripes)+", \U0001D499)0.5\u02E30.5\u00B9\u207B\u02E3").encode('utf-8'),
        formulaQuadraticMsg=("\U0001D432="+str(round((minwidth-maxwidth)/(((stripes-1)/2)**2), 5))+"(\U0001D499-"+str((stripes-1)/2)+")\u00B2+"+str(maxwidth)).encode('utf-8'),
        graph="out/output."+mode)
    
def printDoubleQuad(h, v, height, stripew, angle, cr, shape):
    if (shape == "square"):
        shapeList = rect(h, v, height, stripew)
    elif (shape == "dot"):
        # Added some magic numbers here to move shapes to middle of the image
        shapeList = ellipse(h+math.ceil(stripew*0.5), v+math.ceil(height*0.5), math.ceil(height*0.4), math.ceil(stripew*0.4))
    elif (shape == "parallelogram"):
        shapeList = parallelogram(h, v, height, stripew, angle)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

def printBlaze(orig, circleradius, circlecentre, angleoffset, angle, cr):
    shapeList = blaze_stripe(orig, circleradius, circlecentre, angleoffset, angle)
    cr.set_line_width(0)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

    # Reach the outest point - needs segments
    circle_index = len(circlecentre) - 1
    # arc(x, y, radius, start_angle, end_angle)
    cr.arc(circlecentre[circle_index][0], circlecentre[circle_index][1], circleradius[circle_index],
        math.radians(angleoffset[circle_index]-angle), math.radians(angleoffset[circle_index]))
    cr.close_path()
    cr.fill()

def printParallelogram(h, v, side, stripew, angle, cr):
    shapeList = parallelogram(h, v, side, stripew, angle)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

def printKiss(height, base, kisspoint, curve, distance, accuracy, cr):
    shapeList = kiss(height, base, kisspoint, curve, distance, accuracy)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

def printWaves(x_orig, amplitude, period, verticaloffset, horizontaloffset, length, accuracy, cr):
    shapeList = waves(x_orig, amplitude, period, verticaloffset, horizontaloffset, length, accuracy)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

def printStripes(h, height, stripew, orientation, cr):
    if orientation == "V":
        shapeList = stripev(h, height, stripew)
    elif orientation == "H":
        shapeList = stripeh(h, height, stripew)
    for i in range(len(shapeList)):
        cr.line_to(shapeList[i][0], shapeList[i][1])
    cr.fill()

@app.route('/fullScreen', methods = ['POST', 'GET'])
def fullScreen():
    return render_template("fullscreen.html",
    imageType=imageType,
    mode=mode)

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")