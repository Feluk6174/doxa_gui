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
from kivy.uix.textinput import TextInput
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
import register_screen
import random
from datetime import datetime
from kivy.graphics import BorderImage
from kivy.lang import Builder

import user_image_register_screen, auth, home_screen, search_screen, chat_screen, create_post_screen, profile_screen, user_image_screen, access_my_info, other_user_profile_screen, following_screen, functions, show_crypto_key, add_encrypted


#gotta change this!!!!!!!!!!!!!

class LogInScreen (Screen):
    def __init__(self, conn, sm, **kwargs):
        super(LogInScreen, self).__init__(**kwargs)

        #import info
        self.connection = conn
        self.sm = sm
        

        #llista imatges de fons ((inicials)
        #self.my_list_of_background_images = ['images/username_register.png', 'images/password_register.png', 'images/repeat_password_register.png', 'images/description_register.png', 'images/following_register.png']

        self.main_box = BoxLayout()
        self.main_box.orientation = "vertical"
        self.add_widget(self.main_box)

        #titel
        self.title_box = BoxLayout(orientation = "vertical")
        self.main_box.add_widget(self.title_box)
        
        self.banner = Button (size_hint=(1, None), height = Window.size[1] / 8, border = (0, 0, 0, 0), background_normal = "./images/banner.png", background_down = "./images/banner.png")
        self.title_box.add_widget(self.banner)

        #cos de la pantalla. text inputs i boto
        self.username_box = BoxLayout(orientation = 'vertical', size_hint=(1, None), height = Window.size[1] / 8)
        self.main_box.add_widget(self.username_box)

        self.username_btn = Button(text = "Username:", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = './images/brick.png', background_down = './images/brick.png')
        self.username_box.add_widget(self.username_btn)

        self.username_text_input = TextInput(multiline = False, background_normal = './images/paper_base.png', background_active = './images/paper_base.png')
        #self.username_text_input.bind(keyboard_on_key_down = self.username_text_input_background_image_f)
        self.username_box.add_widget(self.username_text_input)

        self.password_box = BoxLayout(orientation = 'vertical', size_hint=(1, None), height = Window.size[1] / 8)
        self.main_box.add_widget(self.password_box)

        self.password_btn = Button(text = "Password:", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = './images/brick.png', background_down = './images/brick.png')
        self.password_box.add_widget(self.password_btn)

        self.password_text_input = TextInput(multiline = False, password = True, background_normal = './images/paper_base.png', background_active = './images/paper_base.png')
        #self.password_text_input.bind(keyboard_on_key_down = self.password_text_input_background_image_f)
        self.password_box.add_widget(self.password_text_input)
        
        #logo
        self.logo_box = BoxLayout(orientation = "horizontal", size_hint = (1, None), height = Window.size[1] * (1- 4/8 - 1/10))
        self.main_box.add_widget(self.logo_box)

        self.black_label = Label(size_hint = (None, 1), width = (Window.size[0] - Window.size[1] * (1- 4/8 - 1/10))/2)
        self.logo_box.add_widget(self.black_label)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), height = Window.size[1] * (1- 4/8 - 1/10), width = Window.size[1] * (1- 4/8 - 1/10), background_normal = 'images/logo.png', background_down = 'images/logo.png')
        self.logo_box.add_widget(self.logo)

        #buttons
        self.log_in_btn = Button(text = "Log In", border = (0, 0, 0, 0), on_release = self.log_in_press, size_hint=(1, None), height = Window.size[1] / 8, color = (0, 0, 0, 1), background_normal = './images/brick.png', background_down = './images/brick.png')
        self.main_box.add_widget(self.log_in_btn)

        self.register_btn = Button(text = "To register, no account yet", size_hint=(1, None), height = Window.size[1] / 10, color = (0, 0, 0, 1), background_normal = './images/brick.png', background_down = './images/brick.png')
        self.main_box.add_widget(self.register_btn)
        self.register_btn.bind(on_release = self.register)

    #log_in def
    def log_in_press(self, instance):
        con = self.connection
        print(self.username_text_input.text)
        user_info = con.get_user(functions.filter_chars(self.username_text_input.text))
        print(user_info)
        if user_info != {}:
            reconstruct = auth.login(user_info["private_key"], functions.filter_chars(self.username_text_input.text+self.password_text_input.text))
            print(reconstruct)
            if reconstruct == True:
                self.initiate(user_info)
            elif reconstruct == False:
                self.password_text_input.text = ""
                self.password_btn.text = "Repeat password:"
                self.log_in_btn.text = "Log In. Sorry, try again!"
        elif user_info == {}:
            self.username_btn.text = "Repeat username:"
            self.username_text_input.text = ""
            self.log_in_btn.text = "Log In. Sorry, try again!"

    def register(self, user):
        self.manager.transition = FallOutTransition()
        self.manager.current = "register"

    def initiate(self, info):
        #create jso file with my new info
        self.create_my_info_file(info)
        #registrate_user
        con = self.connection
        #create (add) the rest of the main screens
        my_profile_screen = profile_screen.ProfileScreen(con, name = "profile")
        my_profile_screen = profile_screen.ProfileScreen(con, name = "profile")
        my_search_screen = search_screen.SearchScreen(con, name = "search")
        my_chat_screen = chat_screen.ChatScreen(con, name = "chat")
        other_profile_screen = other_user_profile_screen.OtherProfileScreen(con, name = "other_profile")
        create_post_scrn = create_post_screen.PostUserScreen(con, name = "create")
        follow_screen = following_screen.FollowingScreen(con, name = "following")
        self.manager.add_widget(home_screen.MainScreen(con, my_profile_screen, my_search_screen, my_chat_screen, create_post_scrn, other_profile_screen, follow_screen, name = "main"))
        self.manager.add_widget(add_encrypted.AddEncrypted(name = "add_encrypted"))
        self.manager.add_widget(my_chat_screen)
        self.manager.add_widget(my_search_screen)
        self.manager.add_widget(create_post_scrn)
        self.manager.add_widget(my_profile_screen)
        self.manager.add_widget(user_image_screen.ImageScreen(my_profile_screen, con, name = "image"))
        self.manager.add_widget(other_profile_screen)
        self.manager.add_widget(follow_screen)
        try:
            f = open("aes_key.bin", "r")
            f.close()
            self.manager.add_widget(show_crypto_key.ShowCryptoKey(name = "show_key"))
        except FileNotFoundError:
            pass
        self.manager.transition = FallOutTransition()
        self.manager.current = "main"
    
    def create_my_info_file(self, info):
        dictionary = {}
        dictionary["basic_info"] = {}
        dictionary["semi_basic_info"] = {}
        dictionary["basic_info"]["user_id"] = info["user_name"]
        dictionary["basic_info"]["password"] = self.password_text_input.text
        dictionary["semi_basic_info"]["profile_picture"] = info["profile_picture"]
        dictionary["semi_basic_info"]["description"] = info["info"]
        dictionary["semi_basic_info"]["user_following"] = []
        dictionary["semi_basic_info"]["liked_posts_id"] = []
        dictionary["semi_basic_info"]["disliked_posts_id"] = []
        my_info_file = open("my_info.json", "w")
        my_info_file.write(json.dumps(dictionary))
        my_info_file.close


