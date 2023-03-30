#import kivy
from kivy.app import App
from functools import partial
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from kivy.clock import Clock
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.screenmanager import SlideTransition
import kivy.utils
import json
import random
from datetime import datetime
from kivy.graphics import BorderImage
from kivy.lang import Builder
import unicodedata

import api
print("conn")
import register_screen, user_image_register_screen, profile_screen, home_screen, chat_screen, search_screen, create_post_screen, user_image_screen, other_user_profile_screen, following_screen, log_in_screen, advanced_settings_screen, add_encrypted, show_crypto_key, access_my_info, error_screens
import recomendation
try:
    connection = api.Connection(host="34.175.220.44", port=30003)
    access_my_info.set_connection(connection)
    error = False
except OSError:
    error = True



#optional. errase when doing apk
Window.size = (400, 720)

class MyApp (App):
    def build(self):
        print(1)

        #set basis. screen manager and connection
        global connection
        sm = ScreenManager()
        if not error:
            check_info = register_screen.check_my_info_exists()
        if error:
            sm.add_widget(error_screens.ConnectionErrorScreen(name="connection_error"))

        #look if user created and if it is registered. if it does not, make it
        
        elif check_info == False:
            f = open("user_keys.json", "w")
            f.write("{}")
            f.close()
            f = open("advanced_settings.json", "w")
            f.write(json.dumps({"tor": False, "encryption": False}))
            f.close()
            sm.add_widget(register_screen.RegisterScreen(connection, sm, name = "register"))
            sm.add_widget(user_image_register_screen.ImageScreen(name = "image_register"))
            sm.add_widget(log_in_screen.LogInScreen(connection, sm, name = "log_in"))
            sm.add_widget(advanced_settings_screen.AdvancedSettings(sm, name="advanced"))
        elif check_info == True:
            try:
                f = open("user_keys.json", "r")
                f.close()
            except FileNotFoundError:
                f = open("user_keys.json", "w")
                f.write("{}")
                f.close()
            check_register = register_screen.check_my_user_exists(connection)
            if check_register == False:
                register_screen.register(connection)
            #Update recomendation algorithm position
            recomendation.start()

            #make screens of app
            my_profile_screen = profile_screen.ProfileScreen(connection, name = "profile")
            my_search_screen = search_screen.SearchScreen(connection, name = "search")
            my_chat_screen = chat_screen.ChatScreen(connection, name = "chat")
            other_profile_screen = other_user_profile_screen.OtherProfileScreen(connection, name = "other_profile")
            create_post_scrn = create_post_screen.PostUserScreen(connection, name = "create")
            follow_screen = following_screen.FollowingScreen(connection, name = "following")
            sm.add_widget(home_screen.MainScreen(connection, my_profile_screen, my_search_screen, my_chat_screen, create_post_scrn, other_profile_screen, follow_screen, name = "main"))
            sm.add_widget(my_chat_screen)
            sm.add_widget(my_search_screen)
            sm.add_widget(create_post_scrn)
            sm.add_widget(my_profile_screen)
            sm.add_widget(user_image_screen.ImageScreen(my_profile_screen, connection, name = "image"))
            sm.add_widget(other_profile_screen)
            sm.add_widget(follow_screen)
            sm.add_widget(add_encrypted.AddEncrypted(name = "add_encrypted"))
            try:
                f = open("aes_key.bin", "r")
                f.close()
                sm.add_widget(show_crypto_key.ShowCryptoKey(name = "show_key"))
            except FileNotFoundError:
                pass
        
        Window.bind(on_keyboard = self.go_back)
        return sm
    
    def go_back(self, window, key, *args):
        print(99)
        if key == 27:
            print(100)
            return True

    def on_stop(self):
        print("closing")
        global connection
        connection.send('{"type": "ACTION", "action": "SEND", "msg": "stop"}')
        connection.close()
        return super().on_stop()


print(00)
if __name__ == "__main__":
    print(111)
    #MyApp.run()
    try:
        print(0)
        MyApp().run()
    except IndexError:
        connection.close()

#text_input a alçada de teclat
##alarm symbol in chat button on ground box of other screens

