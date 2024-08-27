import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report

#this is a Keras model that is utilised through TensorFlow for high level APIs. this helps build deep learning models to improve the training of image datasets
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
#this is a model used as a layer to implementing 2D CNN layers to learn spatial hierarchies from facial encodings
#as mentioned in the report, max pooling helps reducing spatial dimensions between cnn layers to reduce any computation or dimensions.
from tensorflow.keras.models import Sequential 
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

#directory to locate image datasets, i.e faceRecognition.db
DATA_DIR = "./faceRecognition.db"
CATEGORIES = ["category1", "category2"]  

#resize all images to 64x64 for both CNN & SVM algorithms
IMG_SIZE = 64  

# this funciton loads the image dataset and preprocess the agent's face images
def validateCapturedImages():
    imageData = []
    imgLabels = []
    for indexCategory, category in enumerate(CATEGORIES):
        IMGpath = os.path.join(DATA_DIR, category)
        for img_name in os.listdir(IMGpath):
            try:
                img_path = os.path.join(IMGpath, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                imageData.append(img)
                imgLabels.append(indexCategory)
            except Exception as e:
                pass
    return np.array(imageData), np.array(imgLabels)

# retreive image data and preprocess the images
imageData, imgLabels = validateCapturedImages()
imageData = imageData / 255.0  # Normalize the data

#this feature splits the image data for the purpose of SVM and CNN training
trainX, testX, trainY, testY = train_test_split(imageData, imgLabels, test_size=0.2, random_state=42)

# svm model implementation starts here
# reshape the image data for SVM (flattening)
trainX = trainX.reshape(len(trainX), -1)
testX_SVM = testX.reshape(len(testX), -1)

#svm model training
SVM_Classifier = svm.SVC(kernel='linear')
SVM_Classifier.fit(testX_SVM, trainY)
predictSVM = SVM_Classifier.predict(testX_SVM)#predictions for SVM
accuracySVM = accuracy_score(testY, predictSVM)#accuracy evaluation for SVM
print("SVM Accuracy score: ", accuracySVM)
print(classification_report(testY, predictSVM))

# Implementaition of CNN model
trainY_CNN = to_categorical(trainY, num_classes=len(CATEGORIES))
testY_CNN = to_categorical(testY, num_classes=len(CATEGORIES))
# CNN model build
optimiseCNNmodel = Sequential()

# CNN model architecture implementation
optimiseCNNmodel.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)))
optimiseCNNmodel.add(MaxPooling2D(pool_size=(2, 2))) #max pool
optimiseCNNmodel.add(Conv2D(64, (3, 3), activation='relu'))
optimiseCNNmodel.add(MaxPooling2D(pool_size=(2, 2)))
optimiseCNNmodel.add(Flatten())
optimiseCNNmodel.add(Dense(128, activation='relu'))
optimiseCNNmodel.add(Dense(len(CATEGORIES), activation='softmax'))
optimiseCNNmodel.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy']) # compile entire CNN model
optimiseCNNmodel.fit(trainX, trainY_CNN, epochs=10, batch_size=32, validation_data=(testX, testY_CNN)) #train CNN model using 10 epochs
lossCNN, accuracyCNNmodel = optimiseCNNmodel.evaluate(testX, testY_CNN)#evaluate  CNN model
print("CNN Accuracy score: ", accuracyCNNmodel)

# Save models for future use
SVMpath = "svm_model.pkl"
CNNpath = "cnn_model.h5"

import pickle
with open(SVMpath, 'wb') as f:
    pickle.dump(SVM_Classifier, f)

optimiseCNNmodel.save(CNNpath)
