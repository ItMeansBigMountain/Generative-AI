'''
PROCEDURE

installation_command = pip install opencv-python


1. get photos of frontal-faces

2. turn them into grey scale

3. train the machine learning algo 



# TRAINED CV DATA-SETS (load into classifier)
https://github.com/opencv/opencv/tree/master/data/haarcascades


# GREY-SCALE PIXELS
# did you know that 1080p is an array of 1080 items, each item being an array with numbers, each number representing a darkness scale from black to white?


'''


import cv2

# using open cv training data sets and loading face-detection ML model
trained_face_data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# convert image to bits
bit_image = cv2.imread("lol.PNG")


# turn test image into grayscale   (bit image & openCV grey class object option)
black_white_test_image = cv2.cvtColor(bit_image, cv2.COLOR_BGR2GRAY)


# face detection coordinates array
face_coordinates = trained_face_data.detectMultiScale(black_white_test_image)
print(face_coordinates)  # ////   [ [x,y,w,h] ]


# drawing rectangle using coordinates (ADDS RECTANGLE TO TESTING BIT IMAGE)
for face_index in range(0,len(face_coordinates) , 1):
    (x,y,w,h) = face_coordinates[face_index]
    rect_img = cv2.rectangle(bit_image, (x,y), ( x+w , y+h ), (255,255,255) , thickness=10 )



# display test bit-image (RECTANGLE)
cv2.imshow("OYAMA PRODUCTIONS", rect_img)
cv2.waitKey()