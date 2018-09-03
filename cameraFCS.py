#!/usr/bin/env python
n=50 # number of frames to analyze
delay=100 # delay between frames in miliseconds
# total acquisition time is n*delay

from cv2 import *
from collections import deque
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.animation as animation
import time
import numpy

# filters for blue and red in BGR format
# only values of B, G, R higher than Low and lower than High pass
# values may be from 0 to 255
blueLow = numpy.array([177, 0, 0], dtype = "uint8")
blueHigh = numpy.array([255, 188, 199], dtype = "uint8")
redLow = numpy.array([0, 0, 195], dtype = "uint8")
redHigh = numpy.array([175, 170, 255], dtype = "uint8")

cam = VideoCapture(0)
namedWindow("camera")
FbAve = 0.0
FrAve = 0.0
FbVarAve = 0.0
FrVarAve = 0.0
FbQueue = deque([])
FrQueue = deque([])
FbVarQueue = deque([])
FrVarQueue = deque([])
FbFbAve = numpy.zeros(n)
FrFrAve = numpy.zeros(n)
FbFrAve = numpy.zeros(n)
FbFbQueue = []
FrFrQueue = []
FbFrQueue = []
fig = plt.figure()
gs = gridspec.GridSpec(2, 2)
fig.canvas.set_window_title("FCS")
ax1 = fig.add_subplot(gs[0,:])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[1,1])
xaxis = []

for i in range(n):
	FbQueue.append(1.0)
	FrQueue.append(1.0)
	FbVarQueue.append(0.0)
	FrVarQueue.append(0.0)
	FbAve += 1.0
	FrAve += 1.0
	FbFbQueue.append(deque([]))
	FrFrQueue.append(deque([]))
	FbFrQueue.append(deque([]))
	for j in range(n):
		FbFbQueue[i].append(1.0)
		FrFrQueue[i].append(1.0)
		FbFrQueue[i].append(1.0)
		FbFbAve[j] += 1.0/n
		FbFrAve[j] += 1.0/n
		FrFrAve[j] += 1.0/n
	xaxis.append(i*delay/1000.0)

def animate(i):
	global cam
	global xaxis
	global blueHigh
	global blueLow
	global redHigh
	global redLow
	global FbQueue
	global FrQueue
	global FbAve
	global FrAve
	global FbVarQueue
	global FrVarQueue
	global FbVarAve
	global FrVarAve
	global FbFbAve
	global FrFrAve
	global FbFrAve
	global FbFbQueue
	global FrFrQueue
	global FbFrQueue
	s,img = cam.read()
	maskRed = cv2.inRange(img, redLow, redHigh)
	maskBlue = cv2.inRange(img, blueLow, blueHigh)
	maskAll = cv2.bitwise_or(maskRed,maskBlue)
	outputAll = cv2.bitwise_and(img, img, mask = maskAll)
	outputRed = cv2.bitwise_and(img, img, mask = maskRed)
	outputBlue = cv2.bitwise_and(img, img, mask = maskBlue)
	cv2.imshow("camera", outputAll)
	blueColors = sumElems(outputBlue)
	redColors = sumElems(outputRed)
	
	Fb = (blueColors[0])/(1000.0)
	Fr = (redColors[2])/(1000.0)
	FbQueue.append(Fb)
	FrQueue.append(Fr)
	FbAve += Fb/n
	FrAve += Fr/n
	FbAve -= FbQueue.popleft()/n
	FrAve -= FrQueue.popleft()/n
	
	FbVar = (Fb-FbAve)*(Fb-FbAve)
	FrVar = (Fr-FrAve)*(Fr-FrAve)
	FbVarQueue.append(FbVar)
	FrVarQueue.append(FrVar)
	FbVarAve += FbVar/n
	FrVarAve += FrVar/n
	FbVarAve -= FbVarQueue.popleft()/n
	FrVarAve -= FrVarQueue.popleft()/n
	
	j=0
	for Fbj in reversed(FbQueue):
		FbFb = Fb*Fbj
		FbFr = Fr*Fbj # comment this line to skip cross-correlation
		FbFbQueue[j].append(FbFb)
		FbFrQueue[j].append(FbFr) # comment to skip cross-correlation
		FbFbAve[j] += FbFb/n
		FbFrAve[j] += FbFr/n # comment to skip cross-correlation
		FbFbAve[j] -= FbFbQueue[j].popleft()/n
		FbFrAve[j] -= FbFrQueue[j].popleft()/n # comment to skip c.-c.
		j += 1
	
	j=0
	for Frj in reversed(FrQueue):
		FrFr = Fr*Frj
		FbFr = Fb*Frj # comment to skip cross-correlation
		FrFrQueue[j].append(FrFr)
		FbFrQueue[j].append(FbFr) # comment to skip cross-correlation
		FrFrAve[j] += FrFr/n
		FbFrAve[j] += FbFr/n # comment to skip cross-correlation
		FrFrAve[j] -= FrFrQueue[j].popleft()/n
		FbFrAve[j] -= FbFrQueue[j].popleft()/n # comment to skip c.-c.
		j += 1
	
	ax1.clear()
	ax1.xaxis.tick_top()
	ax1.xaxis.set_label_position('top')
	ax1.set_xlabel("t/s (time)")
	ax1.set_ylabel("F (intensity)")
	ax1.axhline(y=FbAve, color='b', linestyle='-')
	ax1.axhline(y=FrAve, color='r', linestyle='-')
	ax1.plot(xaxis,FbQueue,'b')
	ax1.plot(xaxis,FrQueue,'r')
	ax2.clear()
	ax2.set_xscale('symlog')
	ax2.set_xlabel("t/s (time)")
	ax2.set_ylabel("G (correlation functions)")
	nBlue=(FbAve*FbAve)/FbVarAve
	nRed=(FrAve*FrAve)/FrVarAve
	ax2.axhline(y=FbVarAve/(FbAve*FbAve), color='b', linestyle='-')
	ax2.axhline(y=FrVarAve/(FrAve*FrAve), color='r', linestyle='-')
	ax2.plot(xaxis,FbFbAve/(FbAve*FbAve)-1,'b')
	ax2.plot(xaxis,FrFrAve/(FrAve*FrAve)-1,'r')
	ax2.plot(xaxis,FbFrAve/(FbAve*FrAve)-1,'g') # comment to skip c.-c
	ax3.clear()
	blueBar,redBar=ax3.bar([0,1],(nBlue,nRed))
	blueBar.set_facecolor('b')
	redBar.set_facecolor('r')
	ax3.set_xticks([0,1])
	ax3.set_xticklabels(['blue', 'red'])

ani = animation.FuncAnimation(fig, animate, interval=delay)
plt.show() # this command runs continously until "FCS" window is closed
destroyWindow("camera")
cam.release()
# Lukasz Mioduszewski, piknik naukowy 2018
