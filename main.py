import cv2
import numpy as np
from flous import centroid_method, mean_method, mix_method

#Pour créer une image manuellement
def create_image():
    img = np.zeros((500,500), dtype = 'uint8')
    cv2.rectangle(img, (150,300),(250,250),200, thickness=cv2.FILLED)
    cv2.circle(img,(200,275), 10, 255,thickness=cv2.FILLED)
    return img

path = "images/img6.png"
img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

cv2.imshow("Image Test",img)
cv2.waitKey(0)

#Deux paramètres : img l'image contenant les objets, inverse booléen 
#qui permet d'inverser l'argument et le référent (False prédéfini)

#centroid_method(img,False)

#mean_method(img,False)

mix_method(img)