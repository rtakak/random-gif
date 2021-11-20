import math
import random
import cv2
import numpy as np

old_color = (100, 30, 0)



def drawing_fading_circle(img):
    xy = (random.randint(100, res), random.randint(100, res))
    for r in range(0, random.randint(0, random.randint(10, res * 20 / 100)), random.randint(5, 40)):
        t = random.choice([-1, 1]) * random.randint(1, 10)
        color = random_color()
        cv2.circle(img, xy, r, color, t)


def drawing_circle(img):
    color = random_color()
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, res), random.randint(0, res))
    r = random.randint(0, random.randint(10, res * 15 / 100))
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
    center = (random.randint(0, res), random.randint(0, res))
    r = random.randint(1, random.randint(10, res * 15 / 100))
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
    center = (random.randint(0, res), random.randint(0, res))
    r = random.randint(0, random.randint(10, res * 25 / 100))
    triangle(img, center, r, 0, color, t)


def drawing_ellipse(img):
    color = random_color()
    axes = random.randint(1, 360), random.randint(1, 360)
    angle = random.randint(1, 360)
    t = random.choice([-1, 1]) * random.randint(1, 10)
    center = (random.randint(0, res), random.randint(0, res))
    r = random.randint(0, random.randint(10, res * 15 / 100))
    cv2.ellipse(img, center, axes, angle, 0, 360, color, t)


def drawing_rectanagle(img):
    color = random_color()

    x1 = random.randint(0, res)
    x2 = random.randint(0, res)
    y1 = random.randint(0, res)
    y2 = random.randint(0, res)
    if (res ** 2) / 6 < abs((x2 - x1) * (y2 - y1)):
        t = random.randint(1, 10)
    else:
        t = random.choice([-1, 1]) * random.randint(1, 10)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, t)


def drawing_square(img):
    color = random_color()
    x = random.randint(0, res)
    y = random.randint(0, res)
    x2 = random.randint(0, res)
    y2 = y + x2 - x
    if (res ** 2) / 6 < (x2 - x) ** 2:
        t = random.randint(1, 10)
    else:
        t = random.choice([-1, 1]) * random.randint(1, 10)
    cv2.rectangle(img, (x, y), (x2, y2), color, t)


def drawing_line(img):
    color = random_color()
    t = random.randint(1, 10)
    cv2.line(img, (random.randint(0, res), random.randint(0, res)), (random.randint(0, res), random.randint(0, res)), color,
             t)


def drawing_arrow(img):
    color = random_color()
    t = random.randint(1, 10)
    start = (random.randint(0, res), random.randint(0, res))
    end = (random.randint(0, res), random.randint(0, res))
    cv2.arrowedLine(img, start, end, color, t, tipLength=random.randint(1, 10) / 10)


def random_color_old():
    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)
    return (b, g, r)


def random_color():
    global old_color
    if random.randint(0, 100) > 10:
        b = (old_color[0] + random.randint(0, 150)) % 255
        g = (old_color[1] + random.randint(0, 150)) % 255
        r = (old_color[2] + random.randint(0, 150)) % 255
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)
        choice = random.randint(1, 6)
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
        y1 = random.randint(0, res)
        y2 = random.randint(y1, y1 + 50)
        img[:, y1:y2] = color
    elif choice == -1:
        x1 = random.randint(0, res)
        x2 = random.randint(x1, x1 + 50)
        img[x1:x2, :] = color


def drawing_full_cross_line(img):
    color = random_color()
    x1, y1 = choose_over4()
    x2, y2 = choose_over3(x1, y1)
    cv2.line(img, (x1, y1), (x2, y2), color)


def random_event(img):
    event_no = random.randint(0, 10)
    if event_no == 0:
        drawing_fading_circle(img)
    if event_no == 1:
        choice = random.choice([-1, 1])
        if choice == -1:
            drawing_line(img)
        else:
            drawing_arrow(img)
    if event_no == 2:
        drawing_square(img)
    if event_no == 3:
        drawing_rectanagle(img)
    if event_no == 4:
        drawing_circle(img)
    if event_no == 5:
        drawing_columns_or_rows(img)
    if event_no == 6:
        drawing_full_cross_line(img)
    if event_no == 7:
        drawing_ellipse(img)
    if event_no == 8:
        drawing_triangle(img)
    if event_no == 9:
        drawing_star(img)
    if event_no == 10:
        drawing_columns_or_rows(img)


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
        y1 = random.randint(0, res)
    elif choice == 2:
        y1 = 0
        x1 = random.randint(0, res)
    elif choice == 3:
        x1 = res
        y1 = random.randint(0, res)
    elif choice == 4:
        y1 = res
        x1 = random.randint(0, res)

    return x1, y1


def choose_over3(x1, y1):
    choice = random.randint(1, 3)
    if choice == 1:
        if x1 == 0:
            x2 = res
            y2 = random.randint(0, res)
        if x1 == res:
            x2 = 0
            y2 = random.randint(0, res)
        if y1 == 0:
            y2 = res
            x2 = random.randint(0, res)
        if y1 == res:
            y2 = 0
            x2 = random.randint(0, res)
    elif choice == 2:
        if x1 == 0:
            x2 = random.randint(0, res)
            y2 = 0
        if x1 == res:
            x2 = random.randint(0, res)
            y2 = 0
        if y1 == 0:
            y2 = random.randint(0, res)
            x2 = 0
        if y1 == res:
            y2 = random.randint(0, res)
            x2 = 0
    elif choice == 3:
        if x1 == 0:
            x2 = random.randint(0, res)
            y2 = res
        if x1 == res:
            x2 = random.randint(0, res)
            y2 = res
        if y1 == 0:
            y2 = random.randint(0, res)
            x2 = res
        if y1 == res:
            y2 = random.randint(0, res)
            x2 = res
    return x2, y2


def random_bg3(img, height, width):
    for time in range(0, random.randint(100, 2000)):
        color = random_color()
        x1, y1 = choose_over4()
        x2, y2 = choose_over3(x1, y1)
        cv2.line(img, (x1, y1), (x2, y2), color)


def random_image(height, width):
    blank_image = np.zeros((height, width, 3), np.uint8)
    # random_bg2(blank_image, height, width)
    #  random_bg3(blank_image, height, width)
    events = random.randint(100, 800)
    print("events no: ", events)
    for event in range(0, events):
        random_event(blank_image)

    l1 = chr(random.randint(65, 90))
    l2 = chr(random.randint(65, 90))
    number = random.randint(1000, 9999)
    filename = l1 + l2 + str(number) + ".png"
    cv2.imwrite(filename, blank_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    cv2.imshow("image", blank_image)
    cv2.waitKey(0)

res = 1000
random_image(res, res)

