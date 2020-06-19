import cv2
import cv2.aruco as aruco
import numpy as np
import math
from numpy import load

#############################FUNCTION TO CHECK WHETHER ANY MARKER IS PRESENT IN THE IMAGE###################################

def check_aruco(img):
    ar_module=aruco.Dictionary_get(aruco.DICT_5X5_250)                           #TO LOAD A DICTIONARY OF ARUCO MARKERS
    detect=aruco.DetectorParameters_create()                                     #INITIALIZING THE DETECTOR
    mc,mid,_=aruco.detectMarkers(img,ar_module,parameters=detect)                #TO GET ID AND CORNER POINTS OF DETECTED ARUCO MARKERS
    return mc                                                                    #RETURNING CORNER POINTS AS A MEANS TO CHECK WHETHER ANY MARKER IS DETECTED OR NOT


###################### FUNCTION TO GET THE LIST OF ARUCO MARKERS DETECTED IN THE IMAGE #########################
###################### THE LIST CONTAINS ARUCO ID,COORDINATE OF ITS CENTRE,ROTATION VECTOR OF ITS CENTRE,TRANSLATION VECTOR OF ITS CENTRE ##############

def detect_aruco(img,mtx,dist):

    ar_module=aruco.Dictionary_get(aruco.DICT_5X5_250)
    detect=aruco.DetectorParameters_create()
    mc,mid,_=aruco.detectMarkers(img,ar_module,parameters=detect)
    aruco_lst=[]

    ################### LOOP TO ADD PROPERTIES OF DETECTED MARKERS IN THE LIST ###################################

    for i in range(len(mid)):
        aruco_id=mid[i]                                                             #ARUCO ID IS STORED IN ARUCO_ID
        rvec,tvec,_=aruco.estimatePoseSingleMarkers(mc,100,mtx,dist)                #ROTATION AND TRANSLATION VECTORS OF MARKER'S CENTRE IS CALCULATED AND STORED IN RVEC AND TVEC

        tpl=(np.array([aruco_id]),rvec[i],tvec[i],mc[i])                            #ALL THE PROPERTIES OF A DETECTED ARUCO IS COLLECTED AND STORED IN A TUPLE
        aruco_lst.append(tpl)                                                       #THE CREATED TUPLE IS ADDED IN THE LIST
    return aruco_lst                                                                #THE FINAL LIST IS RETURNED

############################### FUNCTION TO DRAW CUBE ON MARKER ###########################################################

def draw_cube(img,mtx,dist,aruco_lst):

    for i in range(len(aruco_lst)):
        rvec=aruco_lst[i][1]                                         #GETTING ROTATION VECTOR OF THE FIRST ARUCO DETECTED
        tvec=aruco_lst[i][2]                                         #GETTING ROTATION VECTOR OF THE FIRST ARUCO DETECTED
        pts = np.float32(
            [[-50, -50, 0], [-50, 50, 0],
             [50, 50, 0],[50, -50, 0],
             [-50, -50, 100],[-50, 50, 100],
             [50, 50, 100],[50, -50, 100]])                          #COORDINATES TO MAKE A CUBE
                                                                     #[0,0,0] REPRESENTS CENTER OF ARUCO
                                                                     #THE LENGTH OF EACH EDGE OF MARKER IS 100 UNITS AS DEFINED 

        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, mtx, dist)    #CONVERTING OBJECT POINTS TO IMAGE POINTS

        #################################### LOOP TO DRAW CUBE ###########################################

        for i in range(len(imgpts)):
            j = i + 1
            if (i == 3):
                j = 0
            if (i == 7):
                j = 4
            img = cv2.line(img, tuple(imgpts[i][0]), tuple(imgpts[j][0]), (0, 0, 255), 2)   # TO DRAW LOWER AND UPPER RINGS

        for i in range(0, 4):
            j = i + 4
            img = cv2.line(img, tuple(imgpts[i][0]), tuple(imgpts[j][0]), (0, 0, 255), 2)   # TO DRAW SIDE EDGES

    return img

################################### FUNCTION TO DRAW CYLINDER ON MARKER ################################################

def draw_cylinder(img,mtx,dist,aruco_lst):

    for i in range(len(aruco_lst)):
        rvec=aruco_lst[i][1]
        tvec=aruco_lst[i][2]

        pts1 = np.float32([[50, 0, 0], [50 * math.cos(math.pi / 6), 50 * math.sin(math.pi / 6), 0],
                           [50 * math.cos(math.pi / 3), 50 * math.sin(math.pi / 3), 0], [0, 50, 0],
                           [-50 * math.cos(math.pi / 3), 50 * math.sin(math.pi / 3), 0],
                           [-50 * math.cos(math.pi / 6), 50 * math.sin(math.pi / 6), 0], [-50, 0, 0],
                           [-50 * math.cos(math.pi / 6), -50 * math.sin(math.pi / 6), 0],
                           [-50 * math.cos(math.pi / 3), -50 * math.sin(math.pi / 3), 0], [0, -50, 0],
                           [50 * math.cos(math.pi / 3), -50 * math.sin(math.pi / 3), 0],
                           [50 * math.cos(math.pi / 6), -50 * math.sin(math.pi / 6), 0]])                   # OBJECT POINTS FOR LOWER RING


        pts2 = np.float32([[50, 0, 250], [50 * math.cos(math.pi / 6), 50 * math.sin(math.pi / 6), 250],
                           [50 * math.cos(math.pi / 3), 50 * math.sin(math.pi / 3), 250], [0, 50, 250],
                           [-50 * math.cos(math.pi / 3), 50 * math.sin(math.pi / 3), 250],
                           [-50 * math.cos(math.pi / 6), 50 * math.sin(math.pi / 6), 250], [-50, 0, 250],
                           [-50 * math.cos(math.pi / 6), -50 * math.sin(math.pi / 6), 250],
                           [-50 * math.cos(math.pi / 3), -50 * math.sin(math.pi / 3), 250], [0, -50, 250],
                           [50 * math.cos(math.pi / 3), -50 * math.sin(math.pi / 3), 250],
                           [50 * math.cos(math.pi / 6), -50 * math.sin(math.pi / 6), 250]])                  # OBJECT POINTS FOR UPPER RING

        imgpts1, _ = cv2.projectPoints(pts1, rvec, tvec, mtx, dist)
        imgpts2, _ = cv2.projectPoints(pts2, rvec, tvec, mtx, dist)

        for i in range(len(imgpts1)):
            j = i + 1
            if (i == 11):
                j = 0
            img = cv2.line(img, tuple(imgpts1[i][0]), tuple(imgpts1[j][0]), (0, 255, 0), 2)                  # LOOP TO MAKE LOWER RING

        for i in range(6):
            img = cv2.line(img, tuple(imgpts1[i][0]), tuple(imgpts1[i+6][0]), (0, 255, 0), 2)                # LOOP TO DIVIDE THE LOWER RING INTO EQUAL PARTS


        for i in range(len(imgpts2)):
            j = i + 1
            if (i == 11):
                j = 0
            img = cv2.line(img, tuple(imgpts2[i][0]), tuple(imgpts2[j][0]), (0, 255, 0), 2)                  # LOOP TO MAKE UPPER RING

        for i in range(6):
            img = cv2.line(img, tuple(imgpts2[i][0]), tuple(imgpts2[i+6][0]), (0, 255, 0), 2)                # LOOP TO DIVIDE THE UPPER RING INTO EQUAL PARTS

        for i in range(len(imgpts1)):
            img = cv2.line(img, tuple(imgpts1[i][0]), tuple(imgpts2[i][0]), (0, 255, 0), 2)                  # LOOP TO DRAW SIDE EDGES



    return img






data=load(r"E:\ROBOLUTION SUMMER PROJECT\Task 0.2\Camera.npz")
lst=data.files
dist=data["dist"]
mtx=data["mtx"]

cv2.namedWindow("d",cv2.WINDOW_NORMAL)


cap=cv2.VideoCapture(0)
z=1
while(z):
    ret,frame=cap.read()
    mc= check_aruco(frame)

    if(len(mc)!=0):
        aruco_lst=detect_aruco(frame,mtx,dist)
        if (aruco_lst[0][0][0][0] == 2):
            img=draw_cube(frame,mtx,dist,aruco_lst)
            cv2.imshow("d",img)
        else:
            img=draw_cylinder(frame,mtx,dist,aruco_lst)
            cv2.imshow("d", img)
    else:
        cv2.imshow("d", frame)

    if(cv2.waitKey(1)==ord("q")):                                    # SCREEN QUITS ON ENTERING 'q' AND NOT ON ENTERING 'Q'
        cap.release()
        cv2.destroyAllWindows()
        z=0
