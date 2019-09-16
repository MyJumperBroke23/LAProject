import cv2


cap = cv2.VideoCapture('IMG_3707.MOV')
counter = 0

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if counter == 370:
        cv2.imwrite("img2.jpeg", frame)
    #print(counter)
    counter+=1
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()