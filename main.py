# Digital_Image_Processing_Project
import cv2
import pickle
import cvzone
import numpy as np

#Video_streaming

# Enter the path to the video from your directories
cap = cv2.VideoCapture('Your Path')

with open('CarParkingPositions', 'rb') as f:
    position_lists = pickle.load(f)

width, height = 107, 48

def check_parking_position(img_processed):

    spacecounter = 0

    for position in position_lists:
        x, y = position

        imgCrop = img_processed[y:y+height, x:x+width]
        #cv2.imshow(str(x*y),imgCrop)

        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale = 1, thickness = 2,
                           offset = 0, colorR = (255, 0, 0))

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spacecounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, position, (position[0] + width, position[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Free spaces = {spacecounter}/{len(position_lists)}', (190, 50),
                       scale=3, thickness=5, offset=20, colorR=(255, 0, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    kernel = np.ones((3, 3), np.uint8)
    imgdilate = cv2.dilate(imgMedian, kernel,  iterations = 1)


    check_parking_position(imgdilate)

    cv2.imshow('Image', img)
    cv2.imshow('Imageblur',imgBlur)
    cv2.imshow('ImageThresh',imgThreshold)
    cv2.imshow('ImageMed', imgMedian)
    cv2.imshow('ImageDilate',imgdilate)
    cv2.waitKey(10)


