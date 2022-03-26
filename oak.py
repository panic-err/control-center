#!/~/bin/python

import depthai as dai
import cv2

pipeline = dai.Pipeline()

#pipeline.setCameraTuningBlobPath('../computer-vision/mono-colourspace/tuning_color_low_light.bin')
#cam = pipeline.create(dai.node.ColorCamera)
pipeline.setCameraTuningBlobPath('../computer-vision/mono-colourspace/tuning_mono_low_light.bin')
cam = pipeline.create(dai.node.MonoCamera)


PreviewSize = (300, 300)

XLinkIn = pipeline.create(dai.node.XLinkIn)
XLinkIn.setStreamName("input_stream")

cam.setPreviewSize(PreviewSize)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_13_MP)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

XLinkIn.out.link(cam.inputControl)

#cam.link(cam.inputControl)



XLinkOut = pipeline.create(dai.node.XLinkOut)
XLinkOut.setStreamName("output_stream")


#In.out.link(cam.inputControl)
#xOut.link(cam.still)
with dai.Device() as device:
    device.startPipeline(pipeline)
    print('MxId:', device.getDeviceInfo().getMxId())
    print('USB Speed:', device.getUsbSpeed())
    print('Connected Cameras:', device.getConnectedCameras())
    
    input_q = device.getInputQueue(cam.getStreamName())
    output_q = device.getOutputQueue(cam.getStreamName(), maxSize=1, blocking=False)
    frame = None
    
    
    ctrl = dai.CameraControl()
    
    ctrl.setCaptureStill(False)
    input_q.send(ctrl)
    print("Sending capture still")
    #input_q = device.getInputQueue("input_name")
    #output_q = device.getOutputQueue("output_name", maxSize=1, blocking=False)
    count = 0
    fps = cam.getFps()
    print("Current FPS is " + str(fps))
    
    #pic = output_q.tryGet()
    #print(pic)
    while True:
        inRGB = output_q.tryGet()
    
        if inRGB is not None:
            #Currently this doesn't trigger the input queue, but I've only attempted
            #to take a photo once and I probably got it wrong. to the queue!
            frame = inRGB.getCvFrame()
            cv2.imshow("RGB camera stills 12 MP", frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    
    #while True:
    #    fps = cam.getFps()
    #    print("FPS: " + str(fps))
    
