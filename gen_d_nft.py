#made by Gabriel Asher (github gaasher)

from PIL import Image, ImageDraw
import random
import pandas as pd

SIZE = 1024

OUTLINE_WIDTH = int(SIZE / 128)

#pipeline to generate individual keggy images
def generate_single_image():
    color_prob_list, metadata = generate_color_symbol()
    
    base = Image.new("RGB", (SIZE, SIZE), color_prob_list[0])
    image1 = draw_legs(base, color_prob_list[1], color_prob_list[2], color_prob_list[3])
    image2 = draw_keg(image1, color_prob_list[4], color_prob_list[5])
    image3 = draw_arms(image2, color_prob_list[3], color_prob_list[6], color_prob_list[0])
    image4 = draw_face(image3, color_prob_list[12], color_prob_list[7], color_prob_list[8])
    image5 = draw_keg_top(image4, color_prob_list[9], color_prob_list[4])
    image6 = draw_symbols(image5, color_prob_list[10], color_prob_list[11])
    
    return (image6, metadata)

#generate metadata dict and colors/items for keggy
def generate_color_symbol():
    color_prob_list = []
    attribute_name_list = ["Background", "Shoe Color", "Leg Color", "Body Color", "Keg Color", "Keg Line Color", "Glove Color", "Nose Color", "Eye Color", "Spout Color", "Description"]
    metadata = {}

    color_df = pd.read_csv("colors_list.csv").transpose() #ensure correct reading of df by switching rows and cols
    color_dict = color_df.to_dict(orient='list')

    metadata["Description"] = "None"

    #for each attribute pick a random color from the colors csv
    for i in range(10):
        rowidx = random.randint(0, 863)
        row = color_dict[rowidx]
        r = row[3]
        g = row[4]
        b = row[5]
        metadata[attribute_name_list[i]] = row[1] #assign attribute to color name (not r,g,b value)
        color_prob_list.append((r,g,b))

    #Populate left hand (can change probability of items)
    leftprob = random.random()
    metadata["RightHand"] = "No Item"
    if leftprob > 0.98:
        metadata["RightHand"] = "GDX Delta"
        color_prob_list.append("GDX Delta")
    elif 0.98 >= leftprob >= 0.75:
        metadata["RightHand"] = "Pong Paddle"
        color_prob_list.append("Pong Paddle")
    elif 0.75 > leftprob > 0.5:
        metadata["RightHand"] = "Dartmouth Flag"
        color_prob_list.append("Dartmouth Flag")
    else:
        color_prob_list.append("No item")

    #populate right hand 
    rightprob = random.random()
    metadata["LeftHand"] = 'No Item'
    if rightprob > 0.95:
        metadata["LeftHand"] = "Secret Cane"
        color_prob_list.append("Secret Cane")
    elif 0.95 >= rightprob >= 0.75:
        metadata["LeftHand"] = "Keystone"
        color_prob_list.append("Keystone")
    elif 0.75 > rightprob > 0.5:
        metadata["LeftHand"] = "Book"
        color_prob_list.append("Book")
    else:
        color_prob_list.append("No item")

    if metadata["LeftHand"] == "Secret Cane" and metadata["RightHand"] == "GDX Delta":
        metadata["Description"] = "Secret Keggy had the GDX Delta all along!"
    elif metadata["LeftHand"] == "Secret Cane":
        metadata["Description"] = "A very secretive Keggy"
    elif metadata["RightHand"] == "GDX Delta":
        metadata["Description"] = "Keggy had the GDX Delta all along!"

    #Determine if normal or dead eye
    eye = random.random()
    metadata["Eye"] = "Normal Eye"
    if eye > 0.75:
        metadata["Eye"] = "Dead Eye"
        color_prob_list.append("Dead Eye")
    else:
        color_prob_list.append("Normal Eye")

    return color_prob_list, metadata

#Function which draws legs with given colors for shoes, shorts, and body
def draw_legs(image: Image.Image, shoecolor: tuple, shortcolor: tuple, bodycolor: tuple):
    overlay = image.copy()
    legs = ImageDraw.Draw(overlay)
    
    added = SIZE / 32
    
    ##draw shorts
    x1, y1, x2 = int((SIZE / 3) + (2 * added) / 3), int(SIZE * 2 / 3), int((2*SIZE / 3) - (2 * added) / 3) #top line of shorts
    x3, x4, x5, x6, y2 = int((SIZE / 3) - (2 * added / 3)), int((SIZE / 2) - added), int((SIZE / 2) + added), int((SIZE * 2 / 3) + (2 * added) / 3), int((SIZE * 2 / 3) + 2 * added) #mid line of shorts
    x7, x8, y3 = int((SIZE / 3) + added), int((SIZE * 2 / 3) - added), int((SIZE *2 / 3) + added * 4)  #bottom line of shorts
    shorts = [(x1, y1), (x2, y1), (x6, y2), (x8, y3), (x5, y2), (x4, y2), (x7, y3), (x3, y2), (x1, y1)] #shorts polygon lines
    
    legs.polygon(shorts, fill=shortcolor)
    #outline shorts
    for i in range(0, len(shorts)- 1):
        legs.line((shorts[i], shorts[i+1]), (0,0,0), width=OUTLINE_WIDTH)

    ##draw legs +
    left_leg = [(int(x3), int(y2 + added / 5)), (int(x3 - (3 * added / 2)), int(y3 + added / 2)), (int(x3 - (3 * added / 2)), int(y3 + 3 * added)), 
                (int(x3), int(y3 + 3 * added)), (int(x3 + added / 2), int(y3 + (3 * added / 4))), (int(x7), int(y3)), (int(x3), int(y2 + added / 5))]

    right_leg = [(int(x6), int(y2 + added / 5)), (int(x6 + (3 * added / 2)), int(y3 + added / 2)), (int(x6 + (3 * added / 2)), int(y3 + 3 * added)),
                 (int(x6), int(y3 + 3 * added)), (int(x6 - added / 2), int(y3 + (3 * added / 4))), (int(x8), int(y3)), (int(x6), int(y2 + added / 5))]

    legs.polygon(left_leg, fill=bodycolor)            
    legs.polygon(right_leg, fill=bodycolor)

    offset = (OUTLINE_WIDTH / 2) - 1
    #outline legs
    for i in range(0, len(left_leg) - 1):
        legs.line((left_leg[i], left_leg[i+1]), (0,0,0), width=OUTLINE_WIDTH, joint='curve')
        legs.line((right_leg[i], right_leg[i+1]), (0,0,0), width=OUTLINE_WIDTH, joint='curve')
        legs.ellipse((left_leg[i][0] - offset, left_leg[i][1] - offset, left_leg[i][0] + offset, left_leg[i][1] + offset),
                     fill=(0,0,0))
        legs.ellipse((right_leg[i][0] - offset, right_leg[i][1] - offset, right_leg[i][0] + offset, right_leg[i][1] + offset),
                     fill=(0,0,0))

    #Draw new shoe color onto shoes
    rshoe = Image.open("keg_body_parts/keg_shoe.png")
    rshoe.convert("RGB")
    rshoe.thumbnail((int(SIZE / 8), int(SIZE / 8)), Image.ANTIALIAS)
    for x in range(rshoe.width):
        for y in range(rshoe.height):
            if rshoe.getpixel((x,y))[0] >= 100:
                rshoe.putpixel((x,y), shoecolor)
    lshoe = rshoe.copy().transpose(method= Image.FLIP_LEFT_RIGHT)
    #paste shoes onto keggy
    overlay.paste(lshoe, (int(SIZE / 5 - added / 5), int(SIZE * 6 / 7)), lshoe)
    overlay.paste(rshoe, (int(SIZE * 2 / 3 + added / 2), int(SIZE * 6 / 7)), rshoe)



    return overlay

#Function which draws the keg body with given keg color and line color (horizontal lines on keg)
def draw_keg(image: Image.Image, kegcolor: tuple, linecolor: tuple):
    overlay = image.copy()
    keg = ImageDraw.Draw(overlay)

    added = SIZE / 25
    #(x,y) coordinates for 4 corners of box that is used to base keg off of
    x1, y1 = int(SIZE / 3), int(SIZE / 4) 
    x2, y2 = int(SIZE * 2 / 3), int(SIZE * 2 / 3)


    keg.polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 
      fill = kegcolor, outline=None)
    
    keg.chord((x1, y1 - added, x2, y1 + added), 180, 360, fill=kegcolor)
    keg.chord((x1, y2 - added, x2, y2 + added), 0, 180, fill=kegcolor)

    #draw keg lines

    keg.arc((x1, (SIZE * 4 / 11) - added, x2, (SIZE * 4 / 11) + added), 0, 180, fill=linecolor, width=OUTLINE_WIDTH)
    keg.arc((x1, (SIZE * 6 / 11) - added, x2, (SIZE * 6 / 11) + added), 0, 180, fill=linecolor, width=OUTLINE_WIDTH)
    keg.arc((x1, y1 - added / 2, x2, y1 + added / 2), 0, 180, fill=(0,0,0), width=OUTLINE_WIDTH)

    #draw outlines
    keg.arc((x1, y1 - added, x2, y1 + added), 180, 360, fill= (0,0,0), width=OUTLINE_WIDTH)
    keg.arc((x1, y2 - added, x2, y2 + added), 0, 180, fill= (0,0,0), width=OUTLINE_WIDTH)
    keg.line((x1 + OUTLINE_WIDTH / 3, y1,x1 + OUTLINE_WIDTH / 3,y2), fill=(0,0,0), width=OUTLINE_WIDTH)
    keg.line((x2 - OUTLINE_WIDTH / 3,y1,x2 - OUTLINE_WIDTH / 3,y2), fill=(0,0,0), width=OUTLINE_WIDTH)


    return overlay

def draw_arms(image: Image.Image, bodycolor: tuple, glovecolor: tuple, backgroundcolor: tuple):
    overlay = image.copy()
    rarm = Image.open("keg_body_parts/keg_arm.png")
    rarm.convert("RGB")
    rarm.thumbnail((SIZE * 3 / 11, SIZE * 4 / 11), Image.ANTIALIAS)

    
    for x in range(rarm.width):
         for y in range(rarm.height):
             px = rarm.getpixel((x,y))
             if px[0] >= 200 and px[1] >= 200 and px[2] >= 200:
                 rarm.putpixel((x,y), (backgroundcolor))
             elif px[0] >= 100:
                 rarm.putpixel((x,y), bodycolor)
             elif px[1] >= 100:
                 rarm.putpixel((x,y), glovecolor)
    
    larm = rarm.copy().transpose(method= Image.FLIP_LEFT_RIGHT)
    
    overlay.paste(rarm, (int(SIZE * 2 / 3), int(SIZE / 3)))

    overlay.paste(larm, (int(SIZE / 3) - larm.width, int(SIZE / 3)))
    
    return overlay

def draw_face(image: Image.Image, deadeye: str, nose_color: tuple, eye_color: tuple):
    overlay = image.copy()
    face = ImageDraw.Draw(overlay)
    eye_size = SIZE / 16
    pupil_size = eye_size / 3

    #left eye
    lefteye = [(SIZE * 2 / 5, SIZE * 2 / 5 - eye_size), (SIZE * 2 / 5 + eye_size, SIZE * 2 / 5)]
    leftpupil = [(SIZE * 2 / 5 + pupil_size, SIZE * 2 / 5 - pupil_size * 2), (SIZE * 2 / 5 + pupil_size * 2, SIZE * 2 / 5 - pupil_size)]
    lefteyebrow = [(SIZE * 2 / 5, SIZE * 2 / 5 - eye_size * 3 / 2), (SIZE * 2 / 5 + eye_size, SIZE * 2 / 5 - eye_size)]
    
    if deadeye == "Dead Eye":
        face.line((lefteye[0], lefteye[1]), fill=(0,0,0), width=OUTLINE_WIDTH)
        face.line((lefteye[0][0], lefteye[1][1], lefteye[1][0], lefteye[0][1]), fill=(0,0,0), width=OUTLINE_WIDTH)
    else:
        face.ellipse(lefteye, fill=(eye_color), outline=(0,0,0), width=int(OUTLINE_WIDTH / 2))
        face.ellipse(leftpupil, fill=(0,0,0), outline=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    face.arc(lefteyebrow, 210, 330, fill=(0,0,0), width=OUTLINE_WIDTH)

    #right eye
    righteye = [(SIZE * 3 / 5 - eye_size, SIZE * 2 / 5 - eye_size), (SIZE * 3 / 5, SIZE * 2 / 5)]
    rightpupil = [(SIZE * 3 / 5 - pupil_size * 2, SIZE * 2 / 5 - pupil_size * 2), (SIZE * 3 / 5 - pupil_size, SIZE * 2 / 5 - pupil_size)]
    righteyebrow = [(SIZE * 3 / 5 - eye_size, SIZE * 2 / 5 - eye_size * 3 / 2), (SIZE * 3 / 5, SIZE * 2 / 5 - eye_size)]

    face.ellipse(righteye, fill=(eye_color), outline=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    face.ellipse(rightpupil, fill=(0,0,0), outline=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    face.arc(righteyebrow, 210, 330, fill=(0,0,0), width=OUTLINE_WIDTH)


    #mouth
    mouth = Image.open("keg_body_parts/keg_mouth.png")
    mouth.convert("RGB")
    mouth.thumbnail((int(SIZE * 3 / 11), int(SIZE * 4 / 11)), Image.ANTIALIAS)

    overlay.paste(mouth, ((int(SIZE * 4 / 11), int(SIZE * 4 / 9))), mask=mouth)

    #nose
    nose = [(SIZE * 2 / 5 + eye_size, SIZE * 2 / 5), (SIZE * 3 / 5 - eye_size, SIZE * 2 / 5 + eye_size)]
    face.ellipse(nose, fill=nose_color, outline=(0,0,0), width=OUTLINE_WIDTH)


    return overlay

def draw_keg_top(image: Image.Image, spoutcolor: tuple, kegcolor: tuple):
    overlay = image.copy()
    spout = ImageDraw.Draw(overlay)

    pump_height = SIZE / 32

    #pump
    pump_base = [(int(SIZE / 2 - pump_height / 2), int(SIZE / 4 - 4 * pump_height)), (int(SIZE / 2 + pump_height / 2), int(SIZE / 4 - pump_height / 2))]
    spout.rectangle(pump_base, fill=spoutcolor)
    spout.line((pump_base[0][0], pump_base[0][1], pump_base[0][0], pump_base[1][1]), fill=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    spout.line((pump_base[1][0], pump_base[0][1], pump_base[1][0], pump_base[1][1]), fill=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    spout.chord((pump_base[0][0], pump_base[1][1] - pump_height / 4, pump_base[1][0], pump_base[1][1] + pump_height / 4), 0, 180, fill=spoutcolor)
    spout.arc((pump_base[0][0], pump_base[1][1] - pump_height / 4, pump_base[1][0], pump_base[1][1] + pump_height / 4), 0, 180, fill=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    spout.chord((pump_base[0][0], pump_base[0][1] - pump_height / 4, pump_base[1][0], pump_base[0][1] + pump_height / 4), 180, 360, fill=spoutcolor)
    spout.arc((pump_base[0][0], pump_base[0][1] - pump_height / 4, pump_base[1][0], pump_base[0][1] + pump_height / 4), 180, 360, fill=(0,0,0), width=int(OUTLINE_WIDTH / 2))
    spout.arc((pump_base[0][0], pump_base[0][1] - pump_height / 4, pump_base[1][0], pump_base[0][1] + pump_height / 4), 0, 180, fill=(0,0,0), width=int(OUTLINE_WIDTH / 2))

    spout.line((SIZE / 2, pump_base[0][1], SIZE / 2, pump_base[0][1] - 2 * pump_height), fill=(0,0,0), width=OUTLINE_WIDTH)
    spout.ellipse((pump_base[0][0], pump_base[0][1] - 3 * pump_height, pump_base[1][0], pump_base[0][1] - 2 *pump_height), fill=spoutcolor, outline=(0,0,0), width=int(OUTLINE_WIDTH / 2))

    #mouthpiece
    mouthpiece = [(int(SIZE * 3 / 5), pump_base[0][1]), (int(SIZE * 4 / 5 - 2 * pump_height), SIZE / 2 + pump_height)]
    spout.arc(mouthpiece, 205, 70, fill=(0,0,0), width=OUTLINE_WIDTH)
    mouth = [(int(SIZE * 7 / 10) - pump_height / 2, int(SIZE / 2 + pump_height * 3 / 4)), (int(SIZE * 7 / 10 - pump_height / 4), int(SIZE / 2)), (int(SIZE * 7 / 10 + pump_height / 4), int(SIZE / 2 + pump_height / 4)), (int(SIZE * 7 / 10 - pump_height / 4), int(SIZE / 2 + pump_height))]
    spout.polygon(mouth, fill=kegcolor, outline=(0,0,0))

    return overlay

def draw_symbols(image: Image.Image, lefthand: float, righthand: float):
    overlay = image.copy()

    symboldir = "keg_symbols/"

    ##left hand

    #paddle
    if lefthand == "Pong Paddle":
        paddle = Image.open(symboldir + "keg_paddle.png")
        paddle.convert("RGB")
        paddle.thumbnail((SIZE / 7, SIZE / 7))
        overlay.paste(paddle, (0, int(SIZE * 2 / 7 + SIZE / 48)), paddle)

    #flag
    if lefthand == "Dartmouth Flag":
        flag = Image.open(symboldir + "keg_flag.png")
        flag.convert("RGB")
        flag.thumbnail((SIZE / 2, SIZE / 2))
        overlay.paste(flag, (int(SIZE/20), int(SIZE / 10)), flag)

    #delta
    if lefthand == "GDX Delta":
        delta = Image.open(symboldir + "keg_delta.png")
        delta.convert("RGB")
        delta.thumbnail((SIZE / 5, SIZE / 5))
        overlay.paste(delta, (int(0), int(SIZE * 2/ 7 - SIZE / 32)), delta)

    ## right hand
    if righthand == "Book": 
        books = Image.open(symboldir + "keg_book.png")
        books.convert("RGB")
        books.thumbnail((SIZE / 5, SIZE / 5))
        overlay.paste(books, (int(SIZE * 4 / 5), int(SIZE / 3)), books)

    if righthand == "Keystone":
        stone = Image.open(symboldir + "keg_stone.png")
        stone.convert("RGB")
        stone.thumbnail((SIZE / 6, SIZE / 6))
        overlay.paste(stone, (int(SIZE * 6.1 / 7), int(SIZE / 3.4)), stone)

    if righthand == "Secret Cane":
        cane = Image.open(symboldir + "keg_cane.png")
        cane.convert("RGB")
        cane.thumbnail((SIZE, SIZE))
        overlay.paste(cane, (int(SIZE * 6 / 7), int(SIZE / 3.55)), cane)


    return overlay


