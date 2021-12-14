from kivymd.app import MDApp
from kivy.uix.widget import Widget


class PhotoCamera(Widget):
    pass


class MainApp(MDApp):

    def build(self):
        return PhotoCamera()


if __name__ == '__main__':
    MainApp().run()