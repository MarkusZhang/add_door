import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

def show_contours(contour,canvas_size):
    canvas = np.zeros(shape=canvas_size)
    cv2.drawContours(canvas, [contour], -1, (255, 255, 255), thickness=2)
    plt.imshow(canvas)
    plt.show()


def get_four_lines(points):
    return [
        [points[i][0],points[i+1][0]]
        for i in range(len(points)-1)
    ] + [[points[-1][0],points[0][0]]]

def line_length(line):
    p,q=line
    squared_dist = (p[0]-q[0])**2 + (p[1]-q[1])**2
    return math.sqrt(squared_dist)


def get_sub_lineseg(line,sub_len):
    sorted_line = sorted(line,key=lambda x:x[0])
    p, q = line
    x1, y1 = p
    x2, y2 = q

    # compute coordinates for the sub line seg
    total_len = line_length(line)
    h = 0.5 * total_len - 0.5 * sub_len
    d_y1 = h / total_len * (y2 - y1)
    d_y2 = (h + sub_len) / total_len * (y2 - y1)
    d_x1 = h / total_len * (x2 - x1)
    d_x2 = (h + sub_len) / total_len * (x2 - x1)

    return [
        [round(x1 + d_x1), round(y1 + d_y1)],
        [round(x1 + d_x2), round(y1 + d_y2)]
    ]

#TODO: now we just check whether the two end points of the door correspond to white pixel in the image
#TODO: later can add more validation checks
def validate_door(image,door):
    for point in door:
        pixel = image[point[1]][point[0]].tolist()
        if (pixel == [255,255,255]):
            return False
    return True


if __name__ == "__main__":
    line = [
        [0,0],
        [10,10]
    ]
    print(get_sub_lineseg(line=line,sub_len=5.66))