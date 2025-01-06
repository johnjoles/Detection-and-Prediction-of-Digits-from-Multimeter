# Detection and Prediction of Digits from Multimeter

This script determines whether or not an AA battery is usable by detecting the multimeter's reading when it is connected to the battery.

#Important: Intel Realsense D435i Camera is mounted on UR5eRobot, from that point of view the localization of multimeter is projected.

Number prediction is carried out with Keras "model.h5" (CNN MNIST). Various image processing techniques, such as thresholding and blurring, were employed to detect the digit.

Finally, a window that uses a graphical user interface (GUI) opens to display the battery performance.

model.h5 = weight and model configuration file

# A Battery With Residual Charge 
<img width="529" alt="image" src="https://github.com/user-attachments/assets/6f876caa-69e9-4311-9fe4-e4940b10acf6" />





