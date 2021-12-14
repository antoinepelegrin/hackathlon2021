import kivy
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import cv2
import numpy as np

#from utils


class Foo(object):
    def start(self):
        Clock.schedule_interval(self.callback, 0.5)

    def callback(self, dt):
        print('In callback')

class MainApp(App):

    def buttonCallback(self, instance):
        print('IN BUTTON CALLBACK')

        if not self.routineStarted:
            self.routineStarted = True
            Clock.schedule_interval(self.clockCallback, 0.5)
            print("STARTING ROUTINE")
        else:
            self.routineStarted = False
            Clock.unschedule(self.clockCallback)
            print('STOPPING ROUTINE')


    # MAIN LOOP

    def _convertToNumpy(self, image):
        height, width = image.height, image.width
        newvalue = np.frombuffer(image.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        return newvalue

    def clockCallback(self, instance):
        print("IN CLOCK CALLBACK")
        numpy_array = self._convertToNumpy(self.camera.texture)
        print(numpy_array)

    def build(self):
        self.BUTTON_TEXT = {
            True: "STOP ROUTINE",
            False: "START ROUTINE"
        }
        self.routineStarted = False

        self.camera = Camera(play=True, resolution=(640, 480))

        btn1 = Button(text=self.BUTTON_TEXT[self.routineStarted])
        btn1.bind(on_press=self.buttonCallback)

        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(self.camera)
        layout.add_widget(btn1)

        return layout

if __name__== "__main__":

    MainApp().run()