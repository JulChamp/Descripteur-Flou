import cv2
import numpy as np
from flous import centroid_method, mean_method, mix_method


def create_image():
    img = np.zeros((500,500), dtype = 'uint8')
    cv2.rectangle(img, (150,300),(250,250),200, thickness=cv2.FILLED)
    cv2.circle(img,(250,250), 20, 255,thickness=cv2.FILLED)
    return img

img = create_image()
#cv2.imwrite("img6.png",img)

#path = "test_entoure.PNG"
#img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)


cv2.imshow("Image Test",img)
cv2.waitKey(0)
mix_method(img)