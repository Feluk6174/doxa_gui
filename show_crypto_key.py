import json
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import FallOutTransition

class ShowCryptoKey (Screen):
    def __init__(self, **kwargs):
        super(ShowCryptoKey, self).__init__(**kwargs)

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)

        with open("aes_key.bin", "r") as f:
            key = f.read()

        self.key_label = Button(text = "key: "+key, size_hint = (1, 1), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.key_label)

        self.key_textbox = TextInput(text = key, size_hint = (1, 1), background_normal = './images/paper_base.png', background_active = './images/paper_base.png')
        self.main_all_box.add_widget(self.key_textbox)

        self.scroll_view = Button(size_hint = (1, 4), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.scroll_view)

        self.done_button = Button(size_hint = (1, 1), text = "Done", on_release = self.done, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.done_button)


    def done(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "profile"
