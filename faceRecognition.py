import face_recognition
import cv2
import numpy as np
import sqlite3
import os

def captureAgentFace(save_path='captured_image.jpg'):
    #captures agent's face and stores it under captured_image
    """Capture agent's face from the webcam and store it to faceRecognition database."""
    faceID = cv2.VideoCapture(0)
    
    if not faceID.isOpened():
        raise Exception("Could not open video device.")
    
    ret, frame = faceID.read()
    if not ret:
        raise Exception("Failed to capture image.")

    cv2.imwrite(save_path, frame)
    faceID.release()
    cv2.destroyAllWindows()

def validateAgentFaceID(storedAgentFace):
    """Authenticate agent's face by cross referencing with images stored in faceRecognition database."""
    # Capture the image from the webcam
    captureAgentFace()

    # Load the captured image
    #Deep Convolutional Neural Network (CNN), generaties agent's face encodings, which map a face image to a 128-dimensional feature vector.
    capturedFaceID = face_recognition.load_image_file('captured_image.jpg')
    agentFaceEncodings = face_recognition.face_encodings(capturedFaceID)

    if not agentFaceEncodings:
        return False  # No face found in the captured image

    capturedAgentFaceID = agentFaceEncodings[0]
    

    # Load registered faces
    for username, image_path in storedAgentFace:
        #Load and Encode Stored Faces
        #For each stored faces, the function loads the image, computes the agent's face encodings, and checks if a face encoding is matched with the stored images in database
        try:
            # Load the registered face image
            storedFaceID = face_recognition.load_image_file(image_path)
            storedFaceEncodings = face_recognition.face_encodings(storedFaceID)

            if not storedFaceEncodings:
                continue  # Skip if no face encoding found in this image

            faceEncoding = storedFaceEncodings[0]

            # Compare the captured face with the registered face
            #code uses the HOG (Histogram of Oriented Gradients) feature descriptor along with an SVM (Support Vector Machine) to detect faces in the images
            match = face_recognition.compare_faces([faceEncoding], capturedAgentFaceID)
            #To determine if captured and stored faces are similar, the code calculates the Euclidean distance between their respective 128-dimensional encodings. 
            #If the distance is below a certain threshold, the faces are considered to match and authenticated faceID
            if match[0]:
                return True  # Face matched
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    return False  # No match found

def retrieveFaceID():
    """Fetch all registered faces from the database."""
    conn = sqlite3.connect('faceRecognition.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, image_path FROM agent_faces')
    storedAgentFace = cursor.fetchall()
    conn.close()
    return storedAgentFace
