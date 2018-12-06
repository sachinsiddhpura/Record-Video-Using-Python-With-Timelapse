import cv2
import numpy as np 
import os
import datetime
import time
import glob

#for video record
res='720p'
frame_per_second = 20.0
filename = 'video.avi'
shots_per_second=.25
second_duration= 50

SET_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

def change_dimension(cap,width,height):
    cap.set(3,width)
    cap.set(4,height)

def get_dimension(cap,res='1080p'):
    width, height =SET_DIMENSIONS['480p']
    if res in SET_DIMENSIONS:
        width, height = SET_DIMENSIONS[res]
    change_dimension(cap,width,height)
    return width,height

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_file(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['mp4']

cap=cv2.VideoCapture(0)
vout=cv2.VideoWriter(filename,get_file(filename),25,get_dimension(cap,res))

#for multiple photos capture
timelapse_img_path='images/timelapes'

if not os.path.exists(timelapse_img_path):
    os.mkdir(timelapse_img_path)


now = datetime.datetime.now()
finish_time = now + datetime.timedelta(seconds=second_duration)
i=0

while datetime.datetime.now() < finish_time:

    ret, frame = cap.read()
    filename1 = f'{timelapse_img_path}/{i}.jpg'
    i += 1
    cv2.imwrite(filename1,frame)

    #vout.write(frame)
    cv2.imshow("frame",frame)
    time.sleep(shots_per_second)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#transer images to video
def images_to_video(vout,image_dir,clear_images=True):
    image_list = glob.glob( f'{timelapse_img_path}/{i}.jpg')
    sorted_images = sorted(image_list, key=os.path.getmtime)
    if file in sorted_images:
        image_frame = cv2.read(file)
        vout.write(image_frame)
    if clear_images:
        for file in image_list:
            os.remove(file)

images_to_video(vout,timelapse_img_path)

cap.release()
vout.release()
cv2.destroyAllWindows()