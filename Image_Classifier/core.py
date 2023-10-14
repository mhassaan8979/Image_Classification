import joblib
import json
import numpy as np
import base64
import cv2
import pywt


__class_name_to_number = {}
__class_number_to_name = {}
__model = None


def classify_image(image_base64_data, file_path=None):
    load_saved_artifacts()
    imgs = get_cropped_image_if_2_eyes(image_base64_data, file_path)
    result = []

    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32 * 32 * 3, 1), scalled_img_har.reshape(32 * 32, 1)))
        len_image_array = 32 * 32 * 3 + 32 * 32

        final = combined_img.reshape(1, len_image_array).astype(float)
        result.append({
            'class': class_number_to_name(__model.predict(final)[0]),
            'class_probability': np.around(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })
    return result


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("static/needs/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

    global __model
    if __model is None:
        with open('static/needs/saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")


def get_cropped_image_if_2_eyes(image_base64_data, file_path):
    face_cascade = cv2.CascadeClassifier('static/opencv_haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('static/opencv_haarcascades/haarcascade_eye.xml')

    if file_path:
        img = cv2.imread(file_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces


def get_cv2_image_from_base64_string(image_base64_data):
    if image_base64_data is None:
        return None  # Handle the case where 'image_base64_data' is None
    
    # Split the base64 string to get the actual data part (after the comma)
    #encoded_data = image_base64_data.split(',')[1]

    # Decode the base64 data into a bytes-like object
    image_data = base64.b64decode(image_base64_data)

    # Convert the bytes-like object to a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the NumPy array to an image using OpenCV
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img


def w2d(img, mode='haar', level=1):
    imArray = img
    
    # Datatype conversions
    # convert to grayscale
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    
    # convert to float
    imArray = np.float32(imArray)
    imArray /= 255;
   
    # compute coefficients
    coeffs = pywt.wavedec2(imArray, mode, level=level)

    # Process Coefficients
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0;

    # reconstruction
    imArray_H = pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H = np.uint8(imArray_H)
    return imArray_H


def class_number_to_name(class_num):
    return __class_number_to_name[class_num]



