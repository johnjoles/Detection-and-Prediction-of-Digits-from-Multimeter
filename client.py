import cv2 as cv
from server import Multimeter
from realsense_camera import *

rs = RealsenseCamera()

for _ in range(60):
    Rit, bgr, depth = rs.get_frame_stream()
    image = bgr
    image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)

multimeter = Multimeter(image=image)

imgCrop = multimeter.detect_screen(image=image)
if imgCrop is not None:
    cv.imshow("Crop", imgCrop)

    numbers = multimeter.detect_number(image=imgCrop)
    battery = multimeter.show_numbers(numbers=numbers)
    cv.imshow("M", image)
    cv.waitKey(1000)
    cv.destroyAllWindows()

    if battery == 0:
        print("Waste Battery")
        multimeter.waste_battery()
    elif battery == 1:
        print("Not a Waste Battery, it can be used")
        multimeter.usable_battery()

cv.destroyAllWindows()

cv.waitKey(0)
