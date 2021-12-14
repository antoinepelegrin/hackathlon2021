import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.app import App
from kivymd.app import MDApp

from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.widget import Widget

import cv2
import numpy as np

from utils import movenet, test_warrior, TESTS

class ImageWidget(Widget):
    def on_touch_down(self, touch):
        return 0

class MainApp(MDApp):

    # Class variables
    mvmt_array = ['tree', 'warrior']
    mvmt_nb = 0

    count = 0
    routineStarted = False
    stopWatchLabel = Label(text = 'Start a routine!')
    buttonLabel = Label(text = 'START')
    camera = Camera(play=True, resolution=(640, 480))
    texture = Camera.texture

    # Method when pressing button

    def buttonCallback(self):

        if not self.routineStarted:
            self.routineStarted = True
            # self.buttonLabel.text = 'STOP'
            self.root.ids.toolbar.icon = 'cast-connected'
            Clock.schedule_interval(self.clockCallback, 2)

        else:
            self.routineStarted = False
            Clock.unschedule(self.clockCallback)
            self.count = 0
            self.root.ids.stopWatchLabel.text = 'Start a routine!'
            # self.buttonLabel.text = 'STOP'
            self.root.ids.toolbar.icon = 'cast-connected'


    # MAIN LOOP

    def _nextMovement(self):
        self.count = 0
        self.root.ids.stopWatchLabel.text = str(self.count)
        nb_of_movements = len(self.mvmt_array)
        self.mvmt_nb = (self.mvmt_nb + 1)%nb_of_movements
        print('CHANGING MOVEMENT TO: ' + self.mvmt_array[self.mvmt_nb])
        self.root.ids.yogaPose.source = "assets/usage/warrior.jpg"


    def _convertToNumpy(self, image):
        height, width = image.height, image.width
        newvalue = np.frombuffer(image.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        return newvalue[:,:,:3]

    def _convertToKivy(self, np_array):
        data = np_array.tostring()
        texture = Texture.create(size=(np_array.shape[0], np_array.shape[1]), colorfmt="rgb")
        texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")

        self.texture = texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")


    def _updateStopWatch(self):
        self.count = self.count + 1
        self.root.ids.stopWatchLabel.text = str(self.count)

    def clockCallback(self, instance):
        if self.count == 10:
            self._nextMovement()

        numpy_array = self._convertToNumpy(self.camera.texture)
        keys = movenet(numpy_array)
        
        self._convertToKivy(numpy_array)

        test = TESTS[self.mvmt_array[self.mvmt_nb]]

        if test(keys) == []:
            self._updateStopWatch()
        else:
            self.root.ids.FeedbackLabel.text = str(test(keys))

    # BUILD METHOD

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # button = Button(text=self.buttonLabel.text)
        # button.bind(on_press=self.buttonCallback)

        # layout = BoxLayout(orientation='horizontal')

        # layout.add_widget(self.stopWatchLabel)
        # layout.add_widget(self.camera)
        # layout.add_widget(button)

        return Builder.load_file('assets/usage/landing.kv')

        # return layout

if __name__== "__main__":

    MainApp().run()