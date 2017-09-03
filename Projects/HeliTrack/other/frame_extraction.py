import cv2

video_name = "raw_data/Neovision2-Training-Heli-002.mpg"

'''Extracting frames from a video'''
cap = cv2.VideoCapture(video_name)
print(cap)
success,image = cap.read()
count = 0
success = True
while success:
    success,image = cap.read()
    cv2.imwrite("test_frames/frame%d.jpg" % count, image)     # save frame as JPEG file
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break
    count += 1
cap.release()
