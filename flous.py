import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import collections

def get_centroid(data):
    x = round(np.mean(data, axis = 0)[0])
    y = round(np.mean(data, axis = 0)[1])
    return x,y

def get_objects(img):
    dataRef = []
    dataArg = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == 255:
                dataArg.append([i,j])
            elif img[i,j] == 200:
                dataRef.append([i,j])
    return dataRef,dataArg

def createVector(x1,y1,x2,y2, img):
    #Premier vecteur de direction x
    v1 = (img.shape[0] - x1,y1 - y1)
    #Deuxième vecteur de direction passant par les deux points
    v2 = (x2 - x1, y2 - y1)
    return v1,v2

#Equation de droite
def line_eq(x1,y1,x2,y2,x):
    a = (y2 - y1) / (x2 - x1)
    b =  y1 - a * x1
    return int(a * x + b)

#Retourne le vecteur unitaire associé au vecteur
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

#Calcule l'angle entre deux vecteurs
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

#Calcule la distance en pixel entre deux points d'une image
def distance(x1,y1,x2,y2):
    return round(math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2)))

#Affiche la distribution des éléments d'une liste et retourne le tableau contenant l'histogramme
def distrib_angle(array):
    plt.figure(figsize=(7,5))
    x= plt.hist(array,bins=40,range=(-np.pi,np.pi),align="mid")
    plt.title("Distribution des angles entre le centroïde du référent et les points de l'argument")
    plt.xlabel("Angle")
    plt.ylabel("Fréquence")
    plt.show()
    return x[0]

#Affiche les degrés d'appartenance des objets aux relations droite, gauche, haut et bas
def appartenance(angle):
    #On définit une marge car les mesures d'angles peuvent parfois être imprécises
    marge = 0.01
    #Droite ou gauche
    a = math.pow(np.cos(angle),2)
    percent_a = str(round((a*100),2))
    if -np.pi/2 <= angle <= np.pi/2:
        if 1 - marge < a :
            print("L'argument est parfaitement à droite du référent")
        elif 0.7 < a < 1 - marge:
            print("L'argument se trouve fortement à droite du référent (" + percent_a + " %)")
        elif 0.3 < a <= 0.7:
            print("L'argument se trouve à droite du référent (" + percent_a + " %)")
        elif 0.2 < a <= 0.3:
            print("L'argument se trouve faiblement à droite du référent (" + percent_a + " %)")
    else:
        if 1 - marge < a:
            print("L'argument est parfaitement à gauche du référent")
        elif 0.7 < a < 1 - marge:
            print("L'argument se trouve fortement à gauche du référent (" + percent_a + " %)")
        elif 0.3 < a <= 0.7:
            print("L'argument se trouve à gauche du référent (" + percent_a + " %)")
        elif 0.2 < a <= 0.3:
            print("L'argument se trouve faiblement à gauche du référent (" + percent_a + " %)")
    #Haut ou bas
    b = math.pow(np.sin(angle),2)
    percent_b = str(round((b*100),2))
    if  0 < angle :
        if 1 - marge < b :
            print("L'argument est parfaitement en bas du référent")
        elif 0.7 < b < 1 - marge:
            print("L'argument se trouve fortement en bas du référent (" + percent_b + " %)")
        elif 0.4 < b <= 0.7:
            print("L'argument se trouve en bas du référent (" + percent_b + " %)")
        elif 0.2 < b <= 0.4:
            print("L'argument se trouve faiblement en bas du référent (" + percent_b + " %)")
    else:
        if 1 - marge < b:
            print("L'argument est parfaitement en haut du référent")
        elif 0.7 < b < 1 - marge:
            print("L'argument se trouve fortement en haut du référent (" + percent_b + " %)")
        elif 0.4 < b <= 0.7:
            print("L'argument se trouve en haut du référent (" + percent_b + " %)")
        elif 0.2 < b <= 0.4:
            print("L'argument se trouve faiblement en haut du référent (" + percent_b + " %)")

#Fonction pour si un objet entoure un autre grâce à la distribution des angles entre les objets
def arround(array):
    count = collections.Counter(array)
    compteur = count[float(0)]
    arround_degree = (len(array) - compteur) / len(array)
    percent_arround_degree = round(arround_degree*100,2)
    if 0.8 >= arround_degree >= 0.5:
        print("L'argument entoure légèrement le référent (" + str(percent_arround_degree) + " %)")
    elif 0.9 >= arround_degree > 0.8:
        print("L'argument entoure le référent (" + str(percent_arround_degree) + " %)")
    elif 1 > arround_degree > 0.9:
        print("L'argument entoure fortement le référent (" + str(percent_arround_degree) + " %)")
    elif arround_degree == 1:
        print("L'argument entoure totalement le référent (" + str(percent_arround_degree) + " %)")
    return arround_degree

#Calcule l'angle entre les centroïdes des objets et affiche les résultats
def centroid_method(img):
    dataRef, dataArg = get_objects(img)
    y1, x1 = get_centroid(dataRef)
    y2, x2 = get_centroid(dataArg)

    d = distance(x1,y1,x2,y2)
    cv2.line(img, (x1,y1), (img.shape[0],y1), 150, 1)
    cv2.line(img, (x1,y1), (x2,y2), 150, 1)
    cv2.imshow('Image test',img)
    cv2.waitKey(0)
    v1, v2 = createVector(x1,y1,x2,y2,img)
    angle = angle_between(v1,v2)
    if y2 < y1:
        angle = -angle
    print("Le centre de l'argument se trouve à " + str(d) + " pixels du centre du référent")
    appartenance(angle)

#Calcule les angles entre tous les points des objets et récupère la moyenne de ces angles
def mean_method(img):
    dataRef, dataArg = get_objects(img)
    all_angles = []
    d_ref = img.shape[0] * img.shape[1]
    for y1,x1 in dataRef:
        for y2,x2 in dataArg:
            v1, v2 = createVector(x1,y1,x2,y2,img)
            angle = angle_between(v1,v2)
            d = distance(x1,y1,x2,y2)
            if d < d_ref:
                d_ref = d
            if y2 < y1:
                angle = -angle
            all_angles.append(angle)
    
    all_angles = np.array(all_angles)
    hist_angles = distrib_angle(all_angles)
    angle_moyen = np.mean(all_angles)
    o = arround(hist_angles)
    #Si l'argument entoure assez le référent l'étude de position sur les axes x et y n'a plus de sens
    if o < 0.8:
        print("L'argument se trouve à " + str(d_ref) + " pixels du référent")
        appartenance(angle_moyen)

#Cette méthode mixe les deux précédentes en calculant les angles entre le centroïde de l'objet référent
#et tous les points de l'objet argument. Le principal intérêt est la réduction du temps de calcul.
def mix_method(img):
    #On récupère tous les points de l'objet argument
    dataRef, dataArg = get_objects(img)
    y1, x1 = get_centroid(dataRef)
    
    all_angles = []

    #On calcule tous les angles et on récupère la distance la plus courte
    d_ref = img.shape[0] * img.shape[1]
    for y2,x2 in dataArg:
        cv2.line(img, (x1,y1), (x2,y2), 150, 1)
        d = distance(x1,y1,x2,y2)
        if d < d_ref:
            d_ref = d
        v1, v2 = createVector(x1,y1,x2,y2,img)
        angle = angle_between(v1,v2)
        if y2 < y1:
            angle = -angle
        all_angles.append(angle)
    all_angles = np.array(all_angles)
    hist_angles = distrib_angle(all_angles)
    angle_moyen = np.mean(all_angles)

    cv2.imshow("Image", img)
    cv2.waitKey(0)

    o = arround(hist_angles)
    #Si l'argument entoure assez le référent l'étude de position sur les axes x et y n'a plus de sens
    if o < 0.8:
        print("L'argument se trouve à " + str(d_ref) + " pixels du centre du référent")
        appartenance(angle_moyen)