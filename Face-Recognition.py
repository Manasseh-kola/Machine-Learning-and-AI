# -*- coding: utf-8 -*-
import face_recognition
import cv2
import numpy as np
import os
import time


# Creating a video capture object
video_capture = cv2.VideoCapture(0)

#list of known family members read from a textfile
f = open("names.txt","r")
known_names = f.read().splitlines()

def concatenation(names):
    return names +".jpg"

images = list(map(concatenation,known_names))

def concat_image(n):
    return face_recognition.load_image_file(n)

name_image = list(map(concat_image,images))
 

def concat_encodings(y):
   
    return face_recognition.face_encodings(y,known_face_locations=None,num_jitters=50)[0]


name_encoding = list(map(concat_encodings,name_image))
known_face_encodings = name_encoding
known_face_names = known_names

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Capture and resize video frame to 1/4 size for faster face recognition 
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color which OpenCV uses to RGB color used by Face-recognition
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        # Find all the faces and face encodings in the current videoFrame
        # Using default HOG + Linear SVM
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Campare faces with known faces database
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            
            #Give audio feed back for recognized faces
            if True in matches:
                 first_match_index = matches.index(True)
                 name = known_face_names[first_match_index]
                 os.popen( 'espeak -ven+f4 -s150 "I know you your name is %s" --stdout | aplay 2>/dev/null' %name)
                 time.sleep(3)

            else:
                os.popen( 'espeak -ven+f4 -s150 "I dont know you" --stdout | aplay 2>/dev/null')
                time.sleep(3)
                
            face_names.append(name)
            

    process_this_frame = not process_this_frame

    # Displaying the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale video frame back to original size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Displaying the resulting image
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release frame
video_capture.release()
cv2.destroyAllWindows()


