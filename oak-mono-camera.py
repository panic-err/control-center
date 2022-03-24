#!/usr/bin/env python3

import cv2
import depthai as dai

import numpy as np
import pandas as pd

#maths
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from scipy import signal


import datetime


pipeline = dai.Pipeline()

monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
camRGB = pipeline.create(dai.node.ColorCamera)


#pipeline.setCameraTuningBlobPath('../computer-vision/mono-colourspace/tuning_mono_low_light.bin')


camoutRGB = pipeline.create(dai.node.XLinkOut)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)
controlIn = pipeline.create(dai.node.XLinkIn)
configIn = pipeline.create(dai.node.XLinkIn)


xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')
camoutRGB.setStreamName('rgb')
controlIn.setStreamName('control')
configIn.setStreamName('config')

monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
camRGB.setBoardSocket(dai.CameraBoardSocket.RGB)
camRGB.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#camRGB.setVideoSize(1920, 1080)


#camRGB.setPreviewSize(300, 300)
camRGB.setInterleaved(False)
camRGB.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

camRGB.still.link(camoutRGB.input)
controlIn.out.link(camRGB.inputControl)

monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)

configIn.out.link(camRGB.inputConfig)

STEP_SIZE = 8
EXP_STEP = 500
ISO_STEP = 50
LENS_STEP = 3
WB_STEP = 200

def clamp(num, v0, v1):
    return max(v0, min(num, v1))







#It takes a while to do this step
with dai.Device(pipeline) as device:

    # Defaults and limits for manual focus/exposure controls
    lensPos = 150
    lensMin = 0
    lensMax = 255

    expTime = 20000
    expMin = 1
    expMax = 33000

    sensIso = 800
    sensMin = 100
    sensMax = 1600
    
    wbManual = 4000
    wbMin = 1000
    wbMax = 12000


    #cmd = dai.RawCameraControl.Command(dai.RawCameraControl.Command.START_STREAM)

    #solar = dai.RawCameraControl.Command(dai.RawCameraControl.Command.EFFECT_MODE)
    
    #awb = dai.RawCameraControl.AutoWhiteBalanceMode(dai.RawCameraControl.AutoWhiteBalanceMode.OFF)
    #solar = solar.EffectMode.SOLARIZE
    
    
    #cme.EFFECT_MODE = cmd.EffectMode.SOLARIZE
    #still = dai.RawCameraControl.Command(dai.RawCameraControl.Command.STILL_CAPTURE)
    
    #end = dai.RawCameraControl.Command(dai.RawCameraControl.Command.STOP_STREAM)

    #cmd.STILL_CAPTURE
    #cmd.STOP_STREAM


    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    
    qRGB = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qcontrol = device.getInputQueue(name="control", maxSize=4, blocking=False)
    
    
    count = 0
    ti = datetime.datetime.now()  
    tprevious = datetime.datetime.now()
    measurement = 0.
    holdLeft = None
    holdRight = None
    while True:

        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        
        inRGB = qRGB.tryGet()
        
        
        
        if inLeft is not None:
            holdLeft = inLeft
        if inRight is not None:
            holdRight = inRight
        if inRGB is not None:
            data = inRGB.getData()
            print(str(data))
            print(str(type(data)))
            print(str(data.shape))
            shape = (3110399,)
            
            dataBlobZeros = np.empty(shape, dtype=np.float64, order='C')
            dataArray = np.array(data, dtype=np.float64, order='C')
            
            
            dataBlob = pd.DataFrame(dataArray)
            #find columns of type int
            mask = dataBlob.dtypes==np.float64
            #select columns for the same
            cols = dataBlob.dtypes[mask].index
            #select these columns and convert to float
            
            #dataBlobNew = dataBlob[cols].apply(lambda x: x.multiply(x, x))
            dataCalc = dataBlob[cols].apply(lambda x: x.add(x, x))
            #dataCalcClamp = dataCalc[cols].apply(lambda x: clamp(x, 0.0, 255))
            
            #calc = dataCalc[3::10400]
            #calc = dataCalc[3::4096]
            calc = dataBlob[3::131072]
            sr = 16384
            ts = 1.0/sr
            t = 10
            t = np.arange(sr*t) / sr
            #X = fft(dataBlob)
            X = fft(calc)
            N = len(X)
            n = np.arange(N)
            T = N/sr
            freq = n/T
            iX = ifft(X)
            
            list_x = [-0.00496863, 0.0421293, 0.07577707, 0.122869, 0.160996, 0.203608, 0.252949, 0.291076, 0.331445, 0.371815, 0.418913, 0.459283, 0.542265, 0.584877, 0.623004, 0.663374, 0.705986, 0.869708, 0.916806, 0.961661]
            list_y = [221.733, 177.273, 182.144, 210.225, 55.5515, 28.3916, 217.59, 208.844, 39.4397, 50.4878, 14.1212, 51.4085, 43.587, 105.728, 31.614, 119.538, 113.348, 119.999, 128.666, 125.062]
            
            
            plt.style.use('seaborn-poster')
            #matplotlib inline
            
            plt.figure(figsize = (12, 6))
            plt.subplot(121)
            
            plt.stem(freq, np.abs(X), 'b', markerfmt=" ", basefmt="-b", use_line_collection=True)
            plt.xlabel('Freq (hz)')
            plt.ylabel('FFT Amplitude |X(freq)|')
            plt.xlim(0, 10)
            
            fs = 11240
            t = 10
            
            
            
            
            plt.subplot(122)
            nperseg = 2**14
            noverlap = 2**13
            #noverlap = 2**16
            #f, t, Sxx = signal.spectrogram(mySignal, fs, nperseg=nperseg, noverlap=0.9)
            f, t, Sxx = signal.spectrogram(iX)
            
            myfilter = (f>800) & (f<1200)
            
            filt = f[myfilter]
            #Sxx = Sxx[myfilter, ...]
            fig = plt.figure()
            fig,ax = plt.subplots()
            ax = plt.axes(projection='3d')
            z = (np.sin(f **2) + np.cos(t **2))
            ax.plot_surface(f[:, None], t[None, :], Sxx[None, :], cmap=cm.coolwarm)
            
            #plt.scatter(t, iX, 'r')
            #plt.plot(t, iX, 'r')
            
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            
            #plt.subplot(122)
            #plt.plot(t, x, 'r')
            
            poly = np.polyfit(list_x, list_y, 7)
            poly_y = np.poly1d(poly)(list_x)
            plt.plot(list_x, poly_y)
            plt.plot(list_x, list_y)
            
            plt.tight_layout()
            plt.show()
            
            #create a small mask useful for something I'm sure
            #dataCalc = dataBlobNew[cols].apply(lambda x: np.geomspace(0.1, 65025))
            
            #keep data frame in range
            #dataCalc = dataBlobNew[cols].apply(lambda x: clamp(x, 0.0, 65025))
            #dataBlob[dataBlobNew.columns] = dataBlobNew
            
            print(str(dataBlob))
            print(str(type(dataBlob)))
            print(str(dataCalc))
            print(str(type(dataCalc)))
            #a = np.zeros(shape, dtype=float, order='C')
            #print(str(a))
            #print(str(type(a)))
            #a = np.multiply(data, data)
            #print(str(a))
            #print(str(a.shape))
        if holdLeft is not None and holdRight is not None:
            count += 1
            #print(inLeft)
            t2 = datetime.datetime.now()
            
            #hold = holdLeft * holdRight
            #print(str(holdLeft.getData())+"Type")
            
            c = t2 - ti
            tprevious = c
            smoothing = 0.9
            measurement = (measurement * smoothing) + (tprevious.total_seconds() * (1.0-smoothing))
            #print("Time for both frames is : " + str(c.total_seconds()*1000))
            
            fps = 1/(measurement)
            #print("FPS is " + str(fps))
            ti = datetime.datetime.now()
            cv2.imshow("monoforall", holdLeft.getCvFrame())
            #print(inRight)
            cv2.imshow("Right", holdRight.getCvFrame())
            holdLeft = None
            holdRight = None
    
        key = cv2.waitKey(1)
        
        if key == ord('p'):
            print("Taking picture")
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qcontrol.send(ctrl)
            key = None
        elif key in [ord('3'), ord('4')]:
            if key == ord('3'):
                expTime = 500
                print("Setting manual exposure to ",str(expTime))
                
            if key == ord('4'): 
                sensIso = 1600
                print("Setting ISO to ",str(sensIso))
            expTime = clamp(expTime, expMin, expMax)
            sensIso = clamp(sensIso, sensMin, sensMax)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            qcontrol.send(ctrl)
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): expTime -= EXP_STEP
            if key == ord('o'): expTime += EXP_STEP
            if key == ord('k'): sensIso -= ISO_STEP
            if key == ord('l'): sensIso += ISO_STEP
            expTime = clamp(expTime, expMin, expMax)
            sensIso = clamp(sensIso, sensMin, sensMax)
            print("Setting manual exposure time: ", expTime, "iso: ", sensIso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            qcontrol.send(ctrl)
        if key == ord('q'):
            
            break

