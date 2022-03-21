#!/~/bin/python

import depthai as dai

pipeline = dai.Pipeline()

xIn = pipeline.create(dai.node.XLinkIn)
xOut = pipeline.create(dai.node.XLinkOut)
xOut.setStreamName("GetFrom")
xIn.setStreamName("h264orbust")
cam = pipeline.create(dai.node.ColorCamera)
cam.setPreviewSize(300, 300)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)


xIn.out.link(cam.inputControl)
#xOut.link(cam.still)
with dai.Device(pipeline) as device:
    device.startPipeline()
    print('MxId:', device.getDeviceInfo().getMxId())
    print('USB Speed:', device.getUsbSpeed())
    print('Connected Cameras:', device.getConnectedCameras())
    
    input_q = device.getInputQueue("h264orbust")
    output_q = device.getOutputQueue("GetFrom", maxSize=1, blocking=False)
    
    ctrl = dai.CameraControl()
    
    ctrl.setCaptureStill(True)
    input_q.send(ctrl)
    print("Sending capture still")
    #input_q = device.getInputQueue("input_name")
    #output_q = device.getOutputQueue("output_name", maxSize=1, blocking=False)
    count = 0
    while True:
        fps = cam.getFps()
        print("FPS: " + str(fps))
    
