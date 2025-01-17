import math
import random
import cv2
import numpy as np
from imutils import rotate
import imageio
import os


wh = 800
def drawing_fading_circle(img):
    xy = (random.randint(100, wh), random.randint(100, wh))
    for r in range(0, random.randint(0, random.randint(10, round(wh * 20 / 100))), random.randint(5, 40)):
        t = random.choice([-1, 1]) * random.randint(1, 10)
        color = random_color()
        cv2.circle(img, xy, r, color, t)


def drawing_circle(img):
    color = random_color()
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, wh), random.randint(0, wh))
    r = random.randint(0, random.randint(10, round(wh * 15 / 100)))
    cv2.circle(img, center, r, color, t)


def intersect_line_segment(l1, l2):
    line1_perpendicular = False
    line2_perpendicular = False
    xs = [l1[0][0], l1[1][0], l2[0][0], l2[1][0]]
    ys = [l1[0][1], l1[1][1], l2[0][1], l2[1][1]]
    xs.sort()
    ys.sort()
    upperx = xs[2]
    downx = xs[1]
    uppery = ys[2]
    downy = ys[1]
    a = l1[0][0] - l1[1][0]
    if a == 0:
        line1_perpendicular = True
    else:
        line1_m = (l1[0][1] - l1[1][1]) / a
        line1_b = l1[0][1] - l1[0][0] * line1_m

    a = l2[0][0] - l2[1][0]
    if a == 0:
        line2_perpendicular = True
    else:
        line2_m = (l2[0][1] - l2[1][1]) / a
        line2_b = l2[0][1] - l2[0][0] * line2_m

    if line1_perpendicular == False and line2_perpendicular == False:
        x = (line1_b - line2_b) / (line2_m - line1_m)
        intersect = [round(x), round(line1_b + line1_m * x)]
        if downx <= intersect[0] <= upperx and downy <= intersect[1] <= uppery:
            return intersect
    elif line1_perpendicular == True and line2_perpendicular == False:
        x = l1[0][0]
        intersect = [round(x), round(line2_b + line2_m * x)]
        if downx <= intersect[0] <= upperx and downy <= intersect[1] <= uppery:
            return intersect
    elif line1_perpendicular == False and line2_perpendicular == True:
        x = l2[0][0]
        intersect = [round(x), round(line1_b + line1_m * x)]
        if downx <= intersect[0] <= upperx and downy <= intersect[1] <= uppery:
            return intersect
    else:
        return False


def triangle(img, center, l, angle, color, t):
    perpendicular = False
    diff = l / math.sqrt(3)
    p1 = round(center[0] + math.sin(math.radians(angle)) * diff), round(
        center[1] - math.cos(math.radians(angle)) * diff)
    p2 = round(center[0] + math.sin(math.radians(angle + 120)) * diff), round(
        center[1] - math.cos(math.radians(angle + 120)) * diff)
    p3 = round(center[0] + math.sin(math.radians(angle + 240)) * diff), round(
        center[1] - math.cos(math.radians(angle + 240)) * diff)
    if t < 0:
        # m 0 olduğunda hata
        cv2.line(img, p1, p2, color, -t)
        cv2.line(img, p1, p3, color, -t)
        cv2.line(img, p2, p3, color, -t)
        if (p2[0] - p3[0]) == 0:
            perpendicular = True
            start = p2[1]
            end = p3[1]
            if start > end:
                start, end = end, start
            for py in range(start, end):
                p = p2[0], py
                cv2.line(img, p, p1, color, -t)
        else:
            m = (p2[1] - p3[1]) / (p2[0] - p3[0])
            b = p2[1] - p2[0] * m
            start = p2[0]
            end = p3[0]
            if start > end:
                start, end = end, start
            for px in range(start, end):
                py = round(m * px + b)
                p = px, py
                cv2.line(img, p, p1, color, -t)
    else:
        cv2.line(img, p1, p2, color, t)
        cv2.line(img, p1, p3, color, t)
        cv2.line(img, p2, p3, color, t)


def drawing_star(img):
    color = random_color()
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, wh), random.randint(0, wh))
    r = random.randint(1, random.randint(10, round(wh * 15 / 100)))
    angle = random.randint(0, 72)
    star(img, center, r, angle, color, t)


def star(img, center, l, angle, color, t):
    diff = l * math.cos(math.radians(18))
    p1 = [round(center[0] + math.sin(math.radians(angle)) * diff),
          round(center[1] - math.cos(math.radians(angle)) * diff)]
    p2 = [round(center[0] + math.sin(math.radians(angle + 72)) * diff),
          round(center[1] - math.cos(math.radians(angle + 72)) * diff)]
    p3 = [round(center[0] + math.sin(math.radians(angle + 144)) * diff),
          round(center[1] - math.cos(math.radians(angle + 144)) * diff)]
    p4 = [round(center[0] + math.sin(math.radians(angle + 216)) * diff),
          round(center[1] - math.cos(math.radians(angle + 216)) * diff)]
    p5 = [round(center[0] + math.sin(math.radians(angle + 288)) * diff),
          round(center[1] - math.cos(math.radians(angle + 288)) * diff)]
    p15 = intersect_line_segment((p1, p3), (p5, p2))
    p25 = intersect_line_segment((p2, p4), (p1, p3))
    p35 = intersect_line_segment((p4, p2), (p5, p3))
    p45 = intersect_line_segment((p1, p4), (p5, p3))
    p55 = intersect_line_segment((p1, p4), (p5, p2))

    pts = np.array([p1, p15, p2, p25, p3, p35, p4, p45, p5, p55], np.int32)
    pts = pts.reshape((-1, 1, 2))
    penta = np.array([[[40, 160], [120, 100], [200, 160], [160, 240], [80, 240]]], np.int32)
    isClosed = True

    if t < 0:
        cv2.fillPoly(img, [pts], color)
    else:
        cv2.polylines(img, [pts], isClosed, color, t)


def drawing_triangle(img):
    color = random_color()
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, wh), random.randint(0, wh))
    r = random.randint(0, random.randint(10, round(wh * 25 / 100)))
    triangle(img, center, r, 0, color, t)


def drawing_ellipse(img):
    color = random_color()
    axes = random.randint(1, 360), random.randint(1, 360)
    angle = random.randint(1, 360)
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, wh), random.randint(0, wh))
    r = random.randint(0, random.randint(10, round(wh * 15 / 100)))
    cv2.ellipse(img, center, axes, angle, 0, 360, color, t)


def drawing_rectanagle(img):
    color = random_color()

    x1 = random.randint(0, wh)
    x2 = random.randint(0, wh)
    y1 = random.randint(0, wh)
    y2 = random.randint(0, wh)
    if (wh ** 2) / 6 < abs((x2 - x1) * (y2 - y1)):
        t = random.randint(1, 10)
    else:
        t = random.choice([-1, 1]) * random.randint(1, 10)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, t)


def drawing_square(img):
    color = random_color()
    x = random.randint(0, wh)
    y = random.randint(0, wh)
    x2 = random.randint(0, wh)
    y2 = y + x2 - x
    if (wh ** 2) / 6 < (x2 - x) ** 2:
        t = random.randint(1, 10)
    else:
        t = random.choice([-1, 1]) * random.randint(1, 10)
    cv2.rectangle(img, (x, y), (x2, y2), color, t)


def drawing_line(img):
    color = random_color()
    t = random.randint(1, 10)
    cv2.line(img, (random.randint(0, wh), random.randint(0, wh)), (random.randint(0, wh), random.randint(0, wh)), color,
             t)


def drawing_arrow(img):
    color = random_color()
    t = random.randint(1, 10)
    start = (random.randint(0, wh), random.randint(0, wh))
    end = (random.randint(0, wh), random.randint(0, wh))
    cv2.arrowedLine(img, start, end, color, t, tipLength=random.randint(1, 10) / 10)


def random_color_old():
    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)
    return (b, g, r)


def random_color():
    if random.randint(0, 100) > 10:
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)
        return b, g, r
    else:
        choice = random.randint(1, 5)
        if choice == 1:
            return (255, 255, 255)
        elif choice == 2:
            return (0, 0, 0)
        elif choice == 3:
            return (255, 0, 0)
        elif choice == 4:
            return (0, 255, 0)
        elif choice == 5:
            return (0, 0, 255)


def hsvrandom_color():
    if random.randint(0, 100) > 6:
        h = random.randint(0, 255)
        s = random.randint(0, 255)
        v = random.randint(0, 255)
        hsv = np.zeros((1, 1, 3), np.uint8)
        hsv[:, :] = (h, s, v)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        b = bgr[:, :, 0]
        g = bgr[:, :, 1]
        r = bgr[:, :, 2]
        return (b, g, r)

    else:
        if random.choice([-1, 1]) == 1:
            return (255, 255, 255)
        else:
            return (0, 0, 0)


def drawing_columns_or_rows(img):
    choice = random.choice([-1, 1])
    color = random_color()
    if choice == 1:
        y1 = random.randint(0, wh)
        y2 = random.randint(y1, y1 + 50)
        img[:, y1:y2] = color
    elif choice == -1:
        x1 = random.randint(0, wh)
        x2 = random.randint(x1, x1 + 50)
        img[x1:x2, :] = color


def drawing_full_cross_line(img):
    color = random_color()
    x1, y1 = choose_over4()
    x2, y2 = choose_over3(x1, y1)
    cv2.line(img, (x1, y1), (x2, y2), color)


def random_event(img):
    events = ["drawing_fading_circle", "drawing_line", "drawing_square", "drawing_square", "drawing_rectanagle",
              "drawing_circle", "drawing_columns_or_rows", "drawing_full_cross_line", "drawing_ellipse",
              "drawing_triangle", "drawing_star", "drawing_columns_or_rows "]
    event = random.choice(events)
    if event == "drawing_fading_circle":
        drawing_fading_circle(img)
    if event == "drawing_line":
        choice = random.choice([-1, 1])
        if choice == -1:
            drawing_line(img)
        else:
            drawing_arrow(img)
    if event == "drawing_square":
        drawing_square(img)
    if event == "drawing_rectanagle":
        drawing_rectanagle(img)
    if event == "drawing_circle":
        drawing_circle(img)
    if event == "drawing_columns_or_rows":
        drawing_columns_or_rows(img)
    if event == "drawing_full_cross_line":
        drawing_full_cross_line(img)
    if event == "drawing_ellipse":
        drawing_ellipse(img)
    if event == "drawing_triangle":
        drawing_triangle(img)
    if event == "drawing_star":
        drawing_star(img)


def random_bg(img, height, width):
    color = random_color()
    for h in range(0, height):
        for w in range(0, width):
            img[h, w] = random_color()


def random_bg2(img, height, width):
    for time in range(0, random.randint(2000, 20000)):
        choice = random.choice([-1, 1])
        color = random_color()
        if choice == 1:
            y1 = random.randint(0, height)
            y2 = random.randint(y1, y1 + 50)
            img[:, y1:y2] = color
        elif choice == -1:
            x1 = random.randint(0, height)
            x2 = random.randint(x1, x1 + 50)
            img[x1:x2, :] = color


def choose_over4():
    choice = random.randint(1, 4)
    if choice == 1:
        x1 = 0
        y1 = random.randint(0, wh)
    elif choice == 2:
        y1 = 0
        x1 = random.randint(0, wh)
    elif choice == 3:
        x1 = wh
        y1 = random.randint(0, wh)
    elif choice == 4:
        y1 = wh
        x1 = random.randint(0, wh)

    return x1, y1


def choose_over3(x1, y1):
    choice = random.randint(1, 3)
    if choice == 1:
        if x1 == 0:
            x2 = wh
            y2 = random.randint(0, wh)
        if x1 == wh:
            x2 = 0
            y2 = random.randint(0, wh)
        if y1 == 0:
            y2 = wh
            x2 = random.randint(0, wh)
        if y1 == wh:
            y2 = 0
            x2 = random.randint(0, wh)
    elif choice == 2:
        if x1 == 0:
            x2 = random.randint(0, wh)
            y2 = 0
        if x1 == wh:
            x2 = random.randint(0, wh)
            y2 = 0
        if y1 == 0:
            y2 = random.randint(0, wh)
            x2 = 0
        if y1 == wh:
            y2 = random.randint(0, wh)
            x2 = 0
    elif choice == 3:
        if x1 == 0:
            x2 = random.randint(0, wh)
            y2 = wh
        if x1 == wh:
            x2 = random.randint(0, wh)
            y2 = wh
        if y1 == 0:
            y2 = random.randint(0, wh)
            x2 = wh
        if y1 == wh:
            y2 = random.randint(0, wh)
            x2 = wh
    return x2, y2


def random_bg3(img, height, width):
    for time in range(0, random.randint(100, 2000)):
        color = random_color()
        x1, y1 = choose_over4()
        x2, y2 = choose_over3(x1, y1)
        cv2.line(img, (x1, y1), (x2, y2), color)


def random_gif(r, n, mode="normal"):
    if mode == "cross":
        n += n%2
    
    
    angle = 360 / n
    width = round(abs(2 * r * math.sin(math.radians(angle/2))))
    height = round(abs(r * math.cos(math.radians(angle/2))))
    blank_image = np.zeros((height*2, width*2, 3), np.uint8)
    blank_sq = np.zeros((r*2, r*2, 3), np.uint8)
    cv2.circle(blank_sq, (r, r), r, (255,255,255), -1)
    events = random.randint(100, 800)
    
    #pattern making
    print("events no: ", events)
    for event in range(0, events):
        random_event(blank_image)

    blank_image = cv2.resize(blank_image, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow("The pattern", blank_image)
    cv2.waitKey(0)

    
    #making pattern triangle or trapezoid or rectangle
    if not mode in("trapezoid", "rectangle"):
        triangle_cnt = np.array([(0,0), (0,height -2), (width//2,0)])
        cv2.drawContours(blank_image, [triangle_cnt], 0, (255, 255, 255), -1)
    if mode != "rectangle":
        triangle_cnt = np.array([(width-1, height-1), (width-1, 0), (round(width / 2), 0)])
        cv2.drawContours(blank_image, [triangle_cnt], 0, (255, 255, 255), -1)

    blank_sq[int(r):int(r + height), int(r - width / 2):int(r + width / 2)] = blank_image
    blank_sq =  rotate(blank_sq, random.choice([0,180]))
    
    #generating random name
    l1 = chr(random.randint(65, 90))
    l2 = chr(random.randint(65, 90))
    number = random.randint(1000, 9999)
    
    #checking if output directory exist and create if not
    directory = os.getcwd() + r"\Outputs\\"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    #ToDo
    print(directory)
    filename_gif = r"D:\Desktop\Projects\OpenCV\random_gif\Outputs\\" + l1 + l2 + str(number) + "_" + mode + ".gif"
    print(l1 + l2 + str(number) + "_" + mode + ".gif")  
    
      
    frames = []
    rotatex = blank_sq.copy()

    #rotation way of animation
    prefix = random.choice([1,-1])
    
    cross_effect = 1
        
    #animations
    for x in list(range(math.ceil((360/angle)))):
        blank_sq = cv2.bitwise_and(blank_sq, rotate(rotatex, cross_effect*prefix*angle*x))
        if mode == "cross":
            cross_effect *= -1
        rgb_frame = cv2.cvtColor(blank_sq, cv2.COLOR_BGR2RGB)
        frames.append(rgb_frame)
        

    for x in list(range(4000 // n)):
        blank_sq = cv2.bitwise_and(blank_sq, rotate(blank_sq, prefix*angle*x))
        rgb_frame = cv2.cvtColor(blank_sq, cv2.COLOR_BGR2RGB)
        frames.append(rgb_frame)
        
    print("Saving GIF file")
    imageio.mimsave(filename_gif, frames, format='GIF', fps=18)



modes = ["normal", "cross", "trapezoid", "rectangle"]
numbers = [15, 30, 45, 60, 75]
resolution = 1000

random_gif(resolution // 2, random.choice(numbers), random.choice(modes))
