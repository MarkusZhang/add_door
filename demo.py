from door import add_door
import params
import matplotlib.pyplot as plt
import cv2

if __name__ == "__main__":
    image = cv2.imread("F:/map.png")
    result = add_door(image=image,num_doors=8,params=params)
    plt.imshow(result)
    plt.show()