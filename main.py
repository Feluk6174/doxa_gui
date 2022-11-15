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
connection = api.Connection()
import register_screen, user_image_register_screen, profile_screen, home_screen, chat_screen, search_screen, create_post_screen, user_image_screen, other_user_profile_screen, following_screen, log_in_screen

#optional. errase when doing apk
#Window.size = (400, 600)



class MyApp (App):
    def build(self):
        print(1)

        #set basis. screen manager and connection
        global connection
        sm = ScreenManager()

        #look if user created and if it is registered. if it does not, make it
        check_info = register_screen.check_my_info_exists()
        if check_info == False:
            sm.add_widget(register_screen.RegisterScreen(connection, sm, name = "register"))
            sm.add_widget(user_image_register_screen.ImageScreen(name = "image_register"))
            sm.add_widget(log_in_screen.LogInScreen(connection, sm, name = "log_in"))
        elif check_info == True:
            check_register = register_screen.check_my_user_exists(connection)
            if check_register == False:
                register_screen.register(connection)
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
        return sm


print(00)
if __name__ == "__main__":
    print(111)
    #MyApp.run()
    try:
        print(0)
        MyApp().run()
    except IndexError:
        connection.close()

#change description api def
#text_input a alçada de teclat
#improve buttons to other screens
#alarm symbol in chat button on ground box of other screens

#functions clicking posts

#flags
#chat subjects: art, programation, videogames, philosophy, politic, sport, books


#textbox with background text
#writing box

