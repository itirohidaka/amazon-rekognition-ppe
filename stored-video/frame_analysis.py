#Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import json
import boto3
import cv2
import math
import io

def analyzeVideo():
    videoFile = "video file"


    rekognition = boto3.client('rekognition')        
    people = []    
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5) #frame rate
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        print("Processing frame id: {}".format(frameId))
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            hasFrame, imageBytes = cv2.imencode(".jpg", frame)

            if(hasFrame):
                response = rekognition.detect_protective_equipment(
                    Image={
                        'Bytes': imageBytes.tobytes(),
                    }
                )
            
            for person in response["Persons"]:
                person["Timestamp"] = (frameId/frameRate)*1000
                people.append(person)
    
    print(people)

    with open(videoFile + ".json", "w") as f:
        f.write(json.dumps(people)) 

    cap.release()

analyzeVideo()