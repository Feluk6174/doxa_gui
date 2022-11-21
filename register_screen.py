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

import user_image_register_screen, auth, home_screen, search_screen, chat_screen, create_post_screen, profile_screen, user_image_screen, access_my_info, other_user_profile_screen, following_screen, functions


def check_my_info_exists():
    try:
        my_user_info = json.loads(open("my_info.json", "r").read())
        return True
    except FileNotFoundError:
        return False

def check_my_user_exists(connection):
    my_user_info = json.loads(open("my_info.json", "r").read())
    username = my_user_info["basic_info"]["user_id"]
    check = check_user_exists(connection, username)
    return check

def check_user_exists(connection, user):
    check_user = connection.get_user(user)
    if check_user != {}:
        return True
    elif check_user == {}:
        return False

#gotta change this!!!!!!!!!!!!!
def register(connection):
    user_name = access_my_info.get_user_name()
    public_key = access_my_info.get_pub_key()
    profile_picture = access_my_info.get_profile_image()
    info = access_my_info.get_description()
    connection.register_user(user_name, public_key, "rsa_key.bin", profile_picture, info)

class RegisterScreen (Screen):
    def __init__(self, conn, sm, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

        #import info
        self.connection = conn
        self.sm = sm
        

        #llista imatges de fons ((inicials)
        #self.my_list_of_background_images = ['images/username_register.png', 'images/password_register.png', 'images/repeat_password_register.png', 'images/description_register.png', 'images/following_register.png']

        self.main_box = BoxLayout()
        self.main_box.orientation = "vertical"
        self.add_widget(self.main_box)


        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_box.add_widget(self.banner)

        #cos de la pantalla. text inputs i boto
        self.username_box = BoxLayout(orientation = 'vertical')
        self.main_box.add_widget(self.username_box)

        self.username_btn = Button(text = "Username:", border = (0, 0, 0, 0))
        self.username_box.add_widget(self.username_btn)

        self.username_text_input = TextInput(multiline = False)
        #self.username_text_input.bind(keyboard_on_key_down = self.username_text_input_background_image_f)
        self.username_box.add_widget(self.username_text_input)

        self.password_box = BoxLayout(orientation = 'vertical')
        self.main_box.add_widget(self.password_box)

        self.password_btn = Button(text = "Password:", border = (0, 0, 0, 0))
        self.password_box.add_widget(self.password_btn)

        self.password_text_input = TextInput(multiline = False, password = True)
        #self.password_text_input.bind(keyboard_on_key_down = self.password_text_input_background_image_f)
        self.password_box.add_widget(self.password_text_input)

        self.repeat_password_box = BoxLayout(orientation = 'vertical')
        self.main_box.add_widget(self.repeat_password_box)

        self.repeat_password_btn = Button(text = "Repeat password:", border = (0, 0, 0, 0))
        self.repeat_password_box.add_widget(self.repeat_password_btn)
        
        self.repeat_password_text_input = TextInput(multiline = False, password = True)
        #self.repeat_password_text_input.bind(keyboard_on_key_down = self.repeat_password_text_input_background_image_f)
        self.repeat_password_box.add_widget(self.repeat_password_text_input)
        
        self.description_box = BoxLayout(orientation = 'vertical', size_hint_y = 2)
        self.main_box.add_widget(self.description_box)

        self.description_btn = Button(text = "Description:", border = (0, 0, 0, 0))
        self.description_box.add_widget(self.description_btn)
        
        self.description_text_input = TextInput(multiline = False, size_hint_y = 3)
        #self.description_text_input.bind(keyboard_on_key_down = self.description_text_input_background_image_f)
        self.description_box.add_widget(self.description_text_input)
        
        self.image_button = Button(text = "Make your profile image", on_press = self.to_image_making)
        self.main_box.add_widget(self.image_button)

        self.advanced_options_button = Button( size_hint = (1, 0.5), text = "Advanced options", on_release = self.advanced_options)
        self.main_box.add_widget(self.advanced_options_button)

        self.register_btn = Button(size_hint = (1, 1), text = "Register")
        self.main_box.add_widget(self.register_btn)
        self.register_btn.bind(on_release = self.register)
        
        self.log_in_btn = Button(size_hint_y = 0.666666, text = "Log In", border = (0, 0, 0, 0), on_release = self.log_in_press)
        self.main_box.add_widget(self.log_in_btn)

        """
        self.following_box = BoxLayout(orientation = 'vertical')
        self.main_box.add_widget(self.following_box)

        self.following_btn = Button(text = "Following:", border = (0, 0, 0, 0))
        self.following_box.add_widget(self.following_btn)

        self.following_text_input = TextInput(multiline = False)
        #self.following_text_input.bind(keyboard_on_key_down = self.following_text_input_background_image_f)
        self.following_box.add_widget(self.following_text_input)"""

        
    def advanced_options(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "advanced"

    #creem o modifiquem la imatge de perfil 
    def to_image_making(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "image_register"

    #log_in def
    def log_in_press(self, insance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "log_in"

    #register user f
    def register(self, instance):
        #comprovar username, password i image que son correctes
        #check user_name is legal
        self.other_users = check_user_exists(self.connection, functions.filter_chars(self.username_text_input.text))
        if self.other_users == True:
            self.username_btn.text = "Username incorrect:"
            self.username_text_input.text = ""
            self.register_btn.text = "Register. Sorry, try again"
        elif self.other_users == False:
            self.password_check = self.check_password()
            self.image_str = user_image_register_screen.get_my_image()
            self.color_check = self.check_image()
            if self.password_check == False:
                self.password_btn.text = "Password incorrect:"
                self.password_text_input.text = ""
                self.register_btn.text = "Register. Sorry, try again"
            elif self.password_text_input.text != self.repeat_password_text_input.text:
                self.repeat_password_btn.text = "Repeat password incorrect"
                self.repeat_password_text_input.text = ""
                self.register_btn.text = "Register. Sorry, try again"
            elif self.color_check == False:
                self.image_button.text = "MAKE YOUR PROFILE IMAGE!"
                self.register_btn.text = "Register. Sorry, try again"
            elif self.password_check == True and self.color_check == True and self.password_text_input.text == self.repeat_password_text_input.text:
                auth.gen_aes_key()

                #guardar la informacio
                self.username_text = self.username_text_input.text
                self.password_text = self.password_text_input.text
                print("pwd", self.password_text)
                self.description_text = functions.filter_chars(self.description_text_input.text)
                #self.following_text = self.following_text_input.text
                #self.following_list = self.following_text.split(", ")

                #crear pantalla d'espera
                self.clear_widgets()
                self.main_box_load = BoxLayout(orientation = "vertical")
                self.add_widget(self.main_box_load)

                self.black_box_1_load = BoxLayout(size_hint_y = None, height = (Window.size[0] * 0.2))
                self.main_box_load.add_widget(self.black_box_1_load)

                self.banner_load = Button(border = (0, 0, 0, 0), size_hint = (None, None), background_normal = 'images/banner.png', background_down = 'images/banner.png', size = (Window.size[0] * 0.7, Window.size[0] * 0.7), pos_hint = {"center_x":0.5})   
                self.main_box_load.add_widget(self.banner_load)

                self.text_load = Label(text = "Creating user...", size_hint = (1, 0.12))
                self.main_box_load.add_widget(self.text_load)

                #Clock.shedule_once()
                self.create_user()


    #creating user keys and starting session
    def create_user(self):
        #create public and private key
        auth.gen_key(self.username_text + self.password_text)
        
        #create jso file with my new info
        self.create_my_info_file()
        #registrate_user
        con = self.connection
        register(con)
        #create (add) the rest of the main screens
        my_profile_screen = profile_screen.ProfileScreen(con, name = "profile")
        my_profile_screen = profile_screen.ProfileScreen(con, name = "profile")
        my_search_screen = search_screen.SearchScreen(con, name = "search")
        my_chat_screen = chat_screen.ChatScreen(con, name = "chat")
        other_profile_screen = other_user_profile_screen.OtherProfileScreen(con, name = "other_profile")
        create_post_scrn = create_post_screen.PostUserScreen(con, name = "create")
        follow_screen = following_screen.FollowingScreen(con, name = "following")
        self.manager.add_widget(home_screen.MainScreen(con, my_profile_screen, my_search_screen, my_chat_screen, create_post_scrn, other_profile_screen, follow_screen, name = "main"))
        self.manager.add_widget(my_chat_screen)
        self.manager.add_widget(my_search_screen)
        self.manager.add_widget(create_post_scrn)
        self.manager.add_widget(my_profile_screen)
        self.manager.add_widget(user_image_screen.ImageScreen(my_profile_screen, con, name = "image"))
        self.manager.add_widget(other_profile_screen)
        self.manager.add_widget(follow_screen)
        self.manager.transition = FallOutTransition()
        self.manager.current = "main"
    
    def create_my_info_file(self):
        dictionary = {}
        dictionary["basic_info"] = {}
        dictionary["semi_basic_info"] = {}
        dictionary["basic_info"]["user_id"] = self.username_text
        dictionary["basic_info"]["password"] = self.password_text
        #dictionary["basic_info"]["user_pub_key"] = pub_key
        #dictionary["basic_info"]["user_priv_key"] = priv_key
        #dictionary["basic_info"]["user_key_storage"] = "rsa_key.bin"
        dictionary["semi_basic_info"]["profile_picture"] = self.image_str
        dictionary["semi_basic_info"]["description"] = self.description_text
        dictionary["semi_basic_info"]["user_following"] = ["doxa"]
        dictionary["semi_basic_info"]["liked_posts_id"] = []
        my_info_file = open("my_info.json", "w")
        my_info_file.write(json.dumps(dictionary))
        my_info_file.close
    
    def check_password(self):
        word = self.password_text_input.text

        #characters to include
        minuscule_letters = "qwertyuiopasdfghjklzxcvbnm"
        majuscule_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        numbers = "01234567889"
        special_caracters = "!|@·#$~%&/()?^[]+*_<>€"
        
        #list of character types in password
        word_cheme = []

        #check if each character type is in the password
        for _ in range (len(word)):
            word_cheme.append(0)
        for l in range (len(minuscule_letters)):
            for p in range (len(word)):
                if minuscule_letters[l] == word[p]:
                    word_cheme[p] = 1
        for l in range (len(majuscule_letters)):
            for p in range (len(word)):
                if majuscule_letters[l] == word[p]:
                    word_cheme[p] = 2
        for l in range (len(numbers)):
            for p in range (len(word)):
                if numbers[l] == word[p]:
                    word_cheme[p] = 3
        for l in range (len(special_caracters)):
            for p in range (len(word)):
                if special_caracters[l] == word[p]:
                    word_cheme[p] = 4
        if not 0 in word_cheme:

            #check if uses all character types
            if 1 in word_cheme and 2 in word_cheme and 3 in word_cheme and 4 in word_cheme:
                return True
            else:
                return False
        else:
            return False

    def check_image(self):
        image = self.image_str

        #hexadecimal characters
        all_hexadecimal_characters = "0123456789ABCDEF"

        #number that counts correct characters
        check_characters = 0
        if len(image) == 64:
            for a in range (len(all_hexadecimal_characters)):
                for b in range (len(image)):
                    if all_hexadecimal_characters[a] == image[b]:
                        check_characters = check_characters + 1
        
        #check all characters are correct
        if check_characters == 64:
            return True
        if check_characters != 64:
            return False

