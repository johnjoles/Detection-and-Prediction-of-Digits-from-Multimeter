import cv2 as cv
import numpy as np
from imutils import contours
from tensorflow.keras.models import load_model
from tkinter import *
import tkinter


# from realsense_camera import *

# rs = RealsenseCamera()


class Multimeter:

    def __init__(self, image):
        self.image = image

    # GUI for Waste battery
    def waste_battery(self):
        background = "#fff"
        window = Tk()
        window.title("Bring Your Own Device")
        window.config(bg=background)
        canvas = Canvas(width=200, height=158)
        team_logo = PhotoImage(file="Team Logo.png")
        canvas.create_image(99, 79, image=team_logo)
        canvas.grid(row=0, column=1)
        canvas1 = Canvas(width=70, height=70)
        low_battery = PhotoImage(file="low battery.png")
        canvas1.create_image(35, 35, image=low_battery)
        canvas1.grid(row=1, column=1)
        Result = tkinter.Label(text="Oops! Waste Battery", font=("Ariel", 20, "bold"))
        Result.grid(row=2, column=1)
        window.mainloop()

    # GUI for Usable battery
    def usable_battery(self):
        background = "#fff"
        window = Tk()
        window.title("Bring Your Own Device")
        window.config(bg=background)
        canvas = Canvas(width=200, height=158)
        team_logo = PhotoImage(file="Team Logo.png")
        canvas.create_image(99, 79, image=team_logo)
        canvas.grid(row=0, column=1)
        canvas1 = Canvas(width=90, height=150)
        full_battery = PhotoImage(file="full battery.png")
        canvas1.create_image(45, 75, image=full_battery)
        canvas1.grid(row=1, column=1)
        Result = tkinter.Label(text="Usable Battery", font=("Ariel", 20, "bold"))
        Result.grid(row=2, column=1)
        window.mainloop()

    # Loading of Keras Model
    def initializePrediction(self):
        model = load_model('myModel.h5')
        return model

    # Detection of screen on the Multimeter
    def detect_screen(self, image):
        grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        _, thresh = cv.threshold(grey_image, 180, 255, cv.THRESH_TOZERO)
        cv.imshow("thresh", thresh)

        contour, hierarchy = cv.findContours(thresh, 1, 2)
        for cnt in contour:
            area = cv.contourArea(cnt)

            perimeter = cv.arcLength(cnt, True)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4 and area > 20000:

                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.intp(box)

                if box[0][1] > box[1][1] and box[2][1] < box[3][1]:
                    y1 = box[1][1]
                    y2 = box[3][1]

                elif box[0][1] == box[1][1] and box[2][1] == box[3][1]:
                    y1 = box[0][1]
                    y2 = box[2][1]

                else:
                    y1 = box[0][1]
                    y2 = box[2][1]

                if box[0][0] < box[1][0] and box[2][0] < box[3][0]:
                    x1 = box[1][0]
                    x2 = box[3][0]

                elif box[0][0] == box[1][0] and box[2][0] == box[3][0]:
                    x1 = box[0][0]
                    x2 = box[2][0]

                else:
                    x1 = box[0][0]
                    x2 = box[2][0]
                # print(x1, x2)
                imgCrop = image[y1:y2, x1:x2]

        return imgCrop

    # Prediction Process
    def prediction(self, image, model):

        ## PREPARE IMAGE
        img = cv.resize(image, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)

        ## GET PREDICTION
        predictions = model.predict(img)
        classIndex = np.argmax(predictions)
        probabilityValue = np.amax(predictions)

        ## SAVE TO RESULT
        result = classIndex
        if probabilityValue < 0.50:
            result = 0
            probabilityValue = 0
        return result

    # Number Detection
    def detect_number(self, image):
        grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(grey_image, (5, 5), 0)

        _, thresh = cv.threshold(blur, 190, 255, cv.THRESH_BINARY)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (1, 5))
        thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
        cv.imshow("CropThresh", thresh)
        cv.waitKey(1000)
        cv.destroyAllWindows()
        contour, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        digits = []
        for cnt in contour:
            area = cv.contourArea(cnt)
            print(area)
            perimeter = cv.arcLength(cnt, True)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)
            (x, y, w, h) = cv.boundingRect(cnt)

            if w > 7 and h > 60 and area > 500:
                print(w, h)
                print("area:", area)
                rect = cv.minAreaRect(cnt)
                boxx = cv.boxPoints(rect)
                boxx = np.intp(boxx)
                cv.drawContours(image, [boxx], -1, (255, 0, 0), 2)
                digits.append(boxx)
        print(digits)

        digits = contours.sort_contours(digits)[0]

        first_digit = thresh[digits[1][1][1]:digits[1][3][1], digits[1][0][0]:digits[1][2][0]]
        second_digit = thresh[digits[2][1][1]:digits[2][3][1], digits[2][0][0]:digits[2][2][0]]
        third_digit = thresh[digits[3][1][1]:digits[3][3][1], digits[3][0][0]:digits[3][2][0]]
        fourth_digit = thresh[digits[4][1][1]:digits[4][3][1], digits[4][0][0]:digits[4][2][0]]
        # fifth_digit = thresh[digits[5][1][1]:digits[5][3][1], digits[5][0][0]:digits[5][2][0]]
        digit_number = [first_digit, second_digit, third_digit, fourth_digit]
        return digit_number

    # Display Of Detected Numbers
    def show_numbers(self, numbers):
        screen_digit = []
        model = self.initializePrediction()
        for num in numbers:
            number = self.prediction(image=num, model=model)

            screen_digit.append(number)

        digits = 0
        for num in screen_digit:
            digits = digits * 10 + num
        digits = digits / 100
        print(digits)

        digits_value = 0
        if digits < 0.5:
            digits_value = 0
        else:
            digits_value = 1

        return digits_value
