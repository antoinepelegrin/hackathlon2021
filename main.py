from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget


class PhotoCamera(Widget):
    pass


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Tree - Extended hand to big toe - Warrior 3",
                "height": dp(56),
                "on_release": lambda x="Tree - Extended hand to big toe - Warrior 3": self.menu_callback(x),
             }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=2,
        )
		
        return Builder.load_file('assets/usage/landing.kv')
        # return PhotoCamera()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()
    
    def menu_callback(self, text_item):
        self.menu.dismiss()
        
        PhotoCamera()

if __name__ == '__main__':
    MainApp().run()