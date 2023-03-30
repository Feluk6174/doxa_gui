from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
import kivy.uix.screenmanager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


import random

#import string_sum

class TestApp(App):
    
    def build(self):
        sm = ScreenManager()

        sm.add_widget(ConnectionErrorScreen(name = "screen"))
        
        return sm

class ConnectionErrorScreen(kivy.uix.screenmanager.Screen):
    def __init__(self, **kwargs):
        super(ConnectionErrorScreen, self).__init__(**kwargs)
        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)

        text = """
Connection couldn't be found.
Try these out:
    - Check your internet connection
    - Update your app
If these do not work contect the developers
        """

        self.button = Button (border = (0, 0, 0, 0), size_hint = (1, 1), background_normal = 'images/paper_pink.png', background_down = 'images/paper_pink.png', text=text)
        self.main_all_box.add_widget(self.button)

        
        

if __name__ == '__main__':
    TestApp().run()