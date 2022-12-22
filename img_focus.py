import cv2


threshold = 20

img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
var = cv2.Laplacian(gray, cv2.CV_64F).var()

if (var > threshold):
    print("Focused")
else:
    print("UnFocused")
