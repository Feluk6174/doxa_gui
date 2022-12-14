import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import FallOutTransition

import functions

class AdvancedSettings (Screen):
    def __init__(self, sm, **kwargs):
        super(AdvancedSettings, self).__init__(**kwargs)
        try:
            with open("advanced_settings.json", "r") as f:
                self.advanced_settings = json.loads(f.read())
        except FileNotFoundError:
            self.advanced_settings = {"tor": False, "encryption": False}
            with open("advanced_settings.json", "w") as f:
                f.write(json.dumps(self.advanced_settings))

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)

        self.tor_buton = Button (size_hint = (1, 0.1), text = "Tor:"+str(self.advanced_settings["tor"]), on_release = self.togle_tor, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.tor_buton)
        
        text = functions.adapt_text_to_window("Enabeling tor will improve your anonimity but will make the app a lo slower. This setting is not reversable. \n Currently not implemented.", int(15/400*Window.size[0]), Window.size[0])
        self.tor_text = Button(size_hint = (1, 0.1), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick_dark.png", background_down = "./images/brick_dark.png", text = text)
        self.main_all_box.add_widget(self.tor_text)

        self.encrypt_buton = Button (size_hint = (1, 0.1), text = "Encrypt:"+str(self.advanced_settings["encryption"]), on_release = self.togle_encryption, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.encrypt_buton)

        text = functions.adapt_text_to_window("Enabeling this will make encrypt evey post you post, perople will have to enter your decrypt key manualy to see the contents. This setting is not reversable.", int(15/400*Window.size[0]), Window.size[0])
        self.tor_text = Button(size_hint = (1, 0.1), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick_dark.png", background_down = "./images/brick_dark.png", text = text)
        self.main_all_box.add_widget(self.tor_text)

        self.done_buton = Button (size_hint = (1, 0.1), text = "Done", on_release = self.done, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.main_all_box.add_widget(self.done_buton)

    def togle_tor(self, instance):
        self.advanced_settings["tor"] = not self.advanced_settings["tor"]
        self.tor_buton.text = "Tor:"+str(self.advanced_settings["tor"])

    def togle_encryption(self, instance):
        self.advanced_settings["encryption"] = not self.advanced_settings["encryption"]
        self.encrypt_buton.text = "Encrypt:"+str(self.advanced_settings["encryption"])

    def done(self, instance):
        with open("advanced_settings.json", "w") as f:
            f.write(json.dumps(self.advanced_settings))

        self.manager.transition = FallOutTransition()
        self.manager.current = "register"