from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import FallOutTransition


import json


class AddEncrypted (Screen):
    def __init__(self, **kwargs):
        super(AddEncrypted, self).__init__(**kwargs)

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)

        self.user_name_label = Button(size_hint = (1, 0.5), text = "User name:", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.user_name_label)

        self.user_name_textinput = TextInput(text='', multiline=False)
        self.main_all_box.add_widget(self.user_name_textinput)

        self.key_label = Button(size_hint = (1, 0.5), text = "key:", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.key_label)

        self.key_textinput = TextInput(text='', multiline=False)
        self.main_all_box.add_widget(self.key_textinput)

        self.done_buton = Button (size_hint = (1, 1), text = "Remove", on_release = self.remove, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.done_buton)

        self.done_buton = Button (size_hint = (1, 1), text = "Add", on_release = self.add, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.done_buton)

        self.done_buton = Button (size_hint = (1, 1), text = "Done", on_release = self.done, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.done_buton)


    def add(self, instance):
        print(self.user_name_textinput.text, self.key_textinput.text)
        try:
            with open("user_keys.json", "r") as f:
                keys = json.loads(f.read())
            keys[self.user_name_textinput.text] = self.key_textinput.text

            with open("user_keys.json", "w") as f:
                f.write(json.dumps(keys))

        except FileNotFoundError:
            keys = {}
            keys[self.user_name_textinput.text] = self.key_textinput.text

            with open("user_keys.json", "w") as f:
                f.write(json.dumps(keys))

    def remove(self, instance):
        print(self.user_name_textinput.text, self.key_textinput.text)
        try:
            with open("user_keys.json", "r") as f:
                keys = json.loads(f.read())
            keys.pop(self.user_name_textinput.text, None)
            print(keys)

            with open("user_keys.json", "w") as f:
                f.write(json.dumps(keys))

        except FileNotFoundError:
            with open("user_keys.json", "w") as f:
                f.write("{}")

    def done(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "profile"