import kivy
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty

import cv2
import numpy as np

from utils import movenet, test_warrior, TESTS

class MainApp(App):

    # Class variables

    mvmt_array = ['warrior']
    mvmt_nb = 0
    
    count = 0
    routineStarted = False
    stopWatchLabel = Label(text = 'Start a routine!')
    buttonLabel = Label(text = 'START')
    camera = Camera(play=True, resolution=(640, 480))

    # Method when pressing button

    def buttonCallback(self, instance):

        if not self.routineStarted:
            self.routineStarted = True
            self.buttonLabel.text = 'STOP'
            Clock.schedule_interval(self.clockCallback, 0.5)

        else:
            self.routineStarted = False
            Clock.unschedule(self.clockCallback)
            self.count = 0
            self.stopWatchLabel.text = 'Start a routine!'
            self.buttonLabel.text = 'STOP'


    # MAIN LOOP

    def _nextMovement(self):
        
        self.count = 0
        nb_of_movements = len(self.mvmt_array)
        self.mvmt_nb = (self.mvmt_nb + 1)%nb_of_movements

        print('CHANGING MOVEMENT TO: ' + self.mvmt_array[self.mvmt_nb])
        
    def _convertToNumpy(self, image):
        height, width = image.height, image.width
        newvalue = np.frombuffer(image.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        return newvalue[:,:,:3]

    def _updateStopWatch(self):
        self.count = self.count + 1
        self.stopWatchLabel.text = str(self.count)

    def clockCallback(self, instance):

        if self.count == 10:
            self._nextMovement()

        numpy_array = self._convertToNumpy(self.camera.texture)
        keys = movenet(numpy_array)
        
        test = TESTS[self.mvmt_array[self.mvmt_nb]]

        if test(keys) != []:
            self._updateStopWatch()
        else:
            print('wrong pause!')

    # BUILD METHOD

    def build(self):

        button = Button(text=self.buttonLabel.text)
        button.bind(on_press=self.buttonCallback)

        layout = BoxLayout(orientation='horizontal')

        layout.add_widget(self.stopWatchLabel)
        layout.add_widget(self.camera)
        layout.add_widget(button)

        return layout

if __name__== "__main__":

    MainApp().run()