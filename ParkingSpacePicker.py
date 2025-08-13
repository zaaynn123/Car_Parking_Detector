import cv2
import pickle

#Enter the path to the image from your directories
img = cv2.imread('Your Path')

width, height = 107, 48
try:

    with open('CarParkingPositions', 'rb') as f:
        position_lists = pickle.load(f)

except:
    position_lists = []



def mouseClick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:
        position_lists.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(position_lists):
            c_x, c_y = position
            if c_x < x < c_x + width and c_y < y < c_y + height:
                position_lists.pop(i)
    with open('CarParkingPositions', 'wb') as f:
        pickle.dump(position_lists, f)


#cv2.rectangle(img, (50, 192), (140, 500), (0, 255, 255), 2) // used for estimating the box size


while True:

    img = cv2.imread(r'C:\Users\PCS\Desktop\Python and Machine Learning\carParkImg.png')
    for position in position_lists:
        cv2.rectangle(img, position, (position[0]+width, position[1]+height), (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)