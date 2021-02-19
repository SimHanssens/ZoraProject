from naoqi import ALProxy, ALModule, ALBroker
from PIL import Image
mask = False
IP = "10.3.208.67"
port = 9559
video_device = ALProxy("ALVideoDevice", IP, port)

camera = 0  # CameraTop
resolutions = 3  # k4VGA
color_spaces = 13  # kBGRColorSpace
fps = 1


tts = ALProxy("ALTextToSpeech", IP, port)
ledRGB = ALProxy("ALLeds", IP, port)
steps = ALProxy("ALMotion", IP, port)
class FaceCounterModule(ALModule):
    """ Counts all the faces seen """

    def __init__(self, name):
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory")
        self.memory.subscribeToEvent("FaceDetected", self.getName(), "on_face_detected")


    def exit(self):
        self.memory.unsubscribeToEvent("FaceDetected", self.getName(), "on_face_detected")
        ALModule.exit(self)

    def on_face_detected(self, key, value, message):

        def initializer():
            subscriber = video_device.subscribeCamera("demo7", camera, resolutions, color_spaces, fps)
            naoImage = video_device.getImageRemote(subscriber)
            # if (naoImage is not None):
            # show(naoImage)

        def show(naoImage):
                # Get the image size and pixel array.

                imageWidth = naoImage[0]
                imageHeight = naoImage[1]
                array = naoImage[6]
                image_string = str(bytearray(array))


                # Create a PIL Image from our pixel array.
                im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

            # Save the image.
                im.save("D:/ProgramFiles/ZoraProject/images/maskImage", "PNG")

        initializer()
        video_device.unsubscribe("demo7")

        if (mask == False):
            tts.say("Please wear a mask before entering!")
            ledRGB.fadeRGB("AllLeds", "red", 2)
            steps.moveTo(0.2, 0, 0)
        else:
            tts.say("You may now enter")
            ledRGB.fadeRGB("AllLeds", "green", 2)
            steps.moveTo(0.1, 0, 0)





def register_module():
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # listen to anyone
                        0,  # find a port and use it
                        IP,  # ip robot
                        port,  # port robot
                        )

    global face_counter_module  # must be a global variable

    face_counter_module = FaceCounterModule("face_counter_module")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        face_counter_module.exit()


if __name__ == '__main__':
    register_module()
