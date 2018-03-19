import cv2
import numpy as np
import imutils
import utils
import random

def add_door(image,params,num_doors):
    """
    :param image: a numpy array, from cv2.imread
    :param params: a module object
    :param num_doors: number of doors to add, the # of doors eventually added will be = min(num_doors, # door candidates found)
    :return: a new numpy image
    """
    image = np.copy(image)

    # get thresholded binary image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

    # extract contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # find possible places to add doors
    door_candidates = []
    for c in cnts:
        # find all the polygon shapes
        c = c.astype("int")
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # find rectangle-like shapes
        if (len(approx)==4): # this is a rectangle
            lines = utils.get_four_lines(points=approx.tolist())
            for line in lines:
                if (utils.line_length(line) > params.wall_len_threshold):
                    # door is a segment in the middle of the wall
                    door = utils.get_sub_lineseg(line=line,sub_len=params.door_len)

                    # the shape lines given by `cv2.approxPolyDP` may not be accurate
                    # so here we further check whether this is really the correct place to add door
                    if (utils.validate_door(image=image,door=door)):
                        door_candidates.append(door)

    # sample from the door candidates, and draw to the image
    doors = random.sample(door_candidates, min(num_doors,len(door_candidates)))
    for door in doors:
        cv2.line(image, pt1=tuple(door[0]), pt2=tuple(door[1]),
                 thickness=params.door_thickness, color=params.door_color)

    return image