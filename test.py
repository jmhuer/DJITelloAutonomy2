import cv2

camera = cv2.VideoCapture(0)

camera.set(3, 1280)

while True:
    ret, image = camera.read()

    cv2.imshow('Webcam', image)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
