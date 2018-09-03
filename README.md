# cameraFCS
Obtain Fluorescent Correlation Spectroscopy data live from camera (designed for macro-size objects like balls)

This Python script was written for the Science Picnic of Polish Radio and the Copernicus Science Centre exhibition where we presented a macro-scale recreation of an FCS experiment: a box filled with blue and red balls was observed by a camera connected to a laptop (our setup is depicted on the second photo in this file: http://info.ifpan.edu.pl/ACTIVITY/Piknik_naukowy_2018-podsumowanie.pdf).

This code requires openCV (for capturing camera images), deque (to efficiently add new datapoints and get rid of the old ones in real time), matplotlib and time (to produce an animated plot) and numpy (for calculations).

Color values in the filters should be changed so that image appearing in the "camera" window is black except for the objects whose "fluorescence" is being observed.
