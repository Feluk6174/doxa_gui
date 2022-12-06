#import kivy
from multiprocessing import connection
from kivy.app import App
from functools import partial
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
from datetime import datetime
#import pyperclip

import access_my_info, functions, search_screen, home_screen, chat_screen



class ProfileScreen (Screen):
    def __init__(self, connection, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        print (5)
        print(555)
        self.connection = connection

        print(59)

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png', on_release = self.refresh_profile_screen)
        self.main_all_box.add_widget(self.banner)
        
        print(57)

        
        
        print(53)

        self.content_box = BoxLayout (orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        self.user_image_name_box = BoxLayout(orientation = "horizontal", size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.content_grid.add_widget(self.user_image_name_box)

        self.user_image_box = BoxLayout(size_hint_x = None, width = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.user_image_name_box.add_widget(self.user_image_box)
        
        print(54)

        self.user_image_grid = functions.build_image(self, access_my_info.get_profile_image(), -1, (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.user_image_box.add_widget(self.user_image_grid)

        self.user_name_btn = Button(text = access_my_info.get_user_name(), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.user_image_name_box.add_widget(self.user_name_btn)
        #self.user_name_btn.bind(on_release = self.user_name_press)

        print(52)

        self.description_box = BoxLayout(size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5 * 2)
        self.content_grid.add_widget(self.description_box)

        text = access_my_info.get_description()
        text = functions.adapt_text_to_window(text, 14, Window.size[0])
        self.user_description_btn = Button(halign = 'center', font_size = 14, text=text, size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5 * 2, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.description_box.add_widget(self.user_description_btn)
        self.user_description_btn.bind(on_release = self.user_description_press)

        print(55)

        self.user_following_btn = Button(text = "Following", size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 10, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.content_grid.add_widget(self.user_following_btn)
        self.user_following_btn.bind(on_release = self.user_following_press)
        
        self.following_box = BoxLayout(orientation = "horizontal", size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 10)
        self.content_grid.add_widget(self.following_box)

        self.add_encrypted = Button(text = "Add encryption", size_hint = (1, 1), on_release = self.add_encrypted_func, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.following_box.add_widget(self.add_encrypted)

        try:
            f = open("aes_key.bin", "r")
            f.close()
            self.show_cryto_key = Button(text = "Show key", size_hint = (1, 1), on_release = self.show_key, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
            self.following_box.add_widget(self.show_cryto_key)
        except FileNotFoundError:
            pass

        self.user_posts_header_box = BoxLayout(size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.content_grid.add_widget(self.user_posts_header_box)

        self.user_posts_btn = Button(text = "My Posts", on_release = self.user_posts_press, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.user_posts_header_box.add_widget(self.user_posts_btn)
        
        self.favourite_posts_btn = Button (text = "Favourites", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.user_posts_header_box.add_widget(self.favourite_posts_btn)
        self.favourite_posts_btn.bind(on_release = self.user_favourites_press)

        #firstposts
        #current: 1 = my, 2 = fav
        self.current_posts = 0
        self.time_variable = 0

        self.zero_favourite_box = BoxLayout()
        self.all_liked_displayed_posts_list = []

        self.zero_my_box = BoxLayout()
        self.all_my_displayed_posts_list = []

        print(51)
        
        #self.user_posts_press(0)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (border = (0, 0, 0, 0), background_normal = './images/mentions.png', background_down = './images/mentions.png')
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_btn = Button (border = (0, 0, 0, 0), background_normal = './images/search.png', background_down = './images/search.png')
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_btn = Button (border = (0, 0, 0, 0), background_normal = './images/home.png', background_down = './images/home.png')
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_label = Button (border = (0, 0, 0, 0), background_normal = './images/profile_white.png', background_down = './images/profile_white.png')
        self.ground_box.add_widget(self.user_profile_label)

        print (50)

    def add_encrypted_func(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "add_encrypted"

    def show_key(self, instance):
        self.manager.transition = FallOutTransition()
        self.manager.current = "show_key"

    def user_description_press(self, instance):
        self.text_description = functions.adapt_text_to_server(self.user_description_btn.text)
        self.description_box.clear_widgets()

        self.user_description_input = TextInput(text = self.text_description, multiline = False, on_text_validate = self.change_description, background_normal = './images/paper_base.png', background_disabled_normal = './images/paper_base.png')
        self.description_box.add_widget(self.user_description_input)

    def change_description(self, instance):
        self.text_description = functions.adapt_text_to_window(functions.filter_chars(self.user_description_input.text), 14, Window.size[0])
        self.connection.change_info(access_my_info.get_user_name(), functions.filter_chars(self.user_description_input.text), access_my_info.get_priv_key())
        self.description_box.clear_widgets()

        functions.change_my_description(self.text_description)

        self.user_description_btn = Button(text = self.text_description, on_release = self.user_description_press, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.description_box.add_widget(self.user_description_btn)

    def user_following_press(self, instance):
        following_screen = self.following_screen
        following_screen.refresh_following()
        self.manager.transition = FallOutTransition()
        self.manager.current = "following"
        

    def refresh_profile_screen(self, instance):
        #self.user_image_box.clear_widgets()

        #self.user_image_grid = functions.build_image(self, access_my_info.get_image(), 0, Window.size[0] / 1.61 / 6)
        #self.user_image_box.add_widget(self.user_image_grid)
        self.create_my_posts()
        self.create_liked_posts()
        if self.current_posts != 1:
            self.user_posts_press(0)
        elif self.current_posts == 1:
            self.user_favourites_press(0)
            

    def user_posts_press(self, instance):
        #self.my_posts_list = access_my_info.get_my_posts()
        #self.my_posts_list = []
        #self.my_posts_list = functions.order_posts_by_timestamp(self.my_posts_list)
        print(3333)
        if self.current_posts == 2:
            self.favourite_posts_box.clear_widgets()
            self.content_grid.remove_widget(self.favourite_posts_box)
        
        if self.current_posts !=1:

            self.user_posts_header_box.clear_widgets()

            self.user_posts_label = Button(text = "My Posts", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick_dark.png", background_down = "./images/brick_dark.png")
            self.user_posts_header_box.add_widget(self.user_posts_label)
            
            self.favourite_posts_btn = Button (text = "Favourites", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
            self.user_posts_header_box.add_widget(self.favourite_posts_btn)
            self.favourite_posts_btn.bind(on_release = self.user_favourites_press)


            #my posts
            self.display_my_posts()

            self.current_posts = 1

    def display_my_posts(self):
        self.my_posts_box = BoxLayout(orientation='vertical', size_hint_y=None, height = len(self.all_my_displayed_posts_list) * (Window.size[1]-Window.size[0]*(1/5 + 1/5.08)))
        for post in self.all_my_displayed_posts_list:
            self.my_posts_box.add_widget(post[1])
        self.content_grid.add_widget(self.my_posts_box)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def user_favourites_press(self, instance):
        print(4444)
        if self.current_posts == 1:
            self.my_posts_box.clear_widgets()
            self.content_grid.remove_widget(self.my_posts_box)

        if self.current_posts != 2:
            self.user_posts_header_box.clear_widgets()

            self.user_posts_btn = Button(text = "My Posts", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
            self.user_posts_header_box.add_widget(self.user_posts_btn)
            self.user_posts_btn.bind(on_release = self.user_posts_press)

            self.favourite_posts_label = Button (text = "Favourites", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick_dark.png", background_down = "./images/brick_dark.png")
            self.user_posts_header_box.add_widget(self.favourite_posts_label)


            #favourite posts
            self.display_liked_posts()

            self.current_posts = 2

    def display_liked_posts(self):
        self.favourite_posts_box = BoxLayout(orientation='vertical', size_hint_y=None, height = len(self.all_liked_displayed_posts_list) * (Window.size[1]-Window.size[0]*(1/5 + 1/5.08)))
        for post in self.all_liked_displayed_posts_list:
            self.favourite_posts_box.add_widget(post[1])
        self.content_grid.add_widget(self.favourite_posts_box)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def create_my_posts(self):
        print(1111)
        conn = self.connection
        self.my_posts_list = conn.get_posts(user_name = self.user_name_btn.text, sort_by = "time_posted", sort_order = 'desc')
        print(559)
        self.zero_my_box = BoxLayout(size_hint_y = None, height = len(self.my_posts_list) * (Window.size[1] - Window.size[0] * (1/5+1/5.08)), orientation = "vertical")
        #self.content_grid.add_widget(self.my_posts_box)

        my_liked_posts_id = access_my_info.get_liked_id()
        self.all_my_displayed_posts_list = []
        for a in range (len(self.my_posts_list)):
            actual_maybe_like = 0
            try:
                for liked_id in my_liked_posts_id:
                    if liked_id == self.my_posts_list[a]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            print(560)
            self.post_btn = functions.make_post_btn(self, self.my_posts_list[a]["user_id"], self.my_posts_list[a]["content"], self.my_posts_list[a]["time_posted"], actual_maybe_like, a, self.my_posts_list[a]["background_color"])
            #self.zero_my_box.add_widget(self.post_btn)
            self.all_my_displayed_posts_list.append([self.my_posts_list[a]["id"], self.post_btn, actual_maybe_like, self.my_posts_list[a]["user_id"]])
        print(561)
        #self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
    
    def create_liked_posts(self):
        print(2222)
        conn = self.connection
        #with connection or in phone memory
        self.my_liked_list_id = access_my_info.get_liked_id()
        self.my_liked_list = conn.get_posts(id=self.my_liked_list_id)
        #self.my_liked_posts_list = []
        self.my_liked_posts_list = functions.order_posts_by_timestamp(self.my_liked_list)

        self.zero_favourite_box = BoxLayout(size_hint_y = None, height = len(self.my_liked_posts_list) * (Window.size[1] - Window.size[0] * (1/5+1/5.08)), orientation = "vertical")
        #self.content_grid.add_widget(self.favourite_posts_box)

        self.all_liked_displayed_posts_list = []

        actual_maybe_like = 1
        for b in range (len(self.my_liked_posts_list)):
            #user_liked_info = conn.get_user(self.my_liked_posts_list[b]["user_id"])        
            self.post_btn = functions.make_post_btn(self, self.my_liked_posts_list[b]["user_id"], self.my_liked_posts_list[b]["content"], self.my_liked_posts_list[b]["time_posted"], actual_maybe_like, b, self.my_liked_posts_list[b]["background_color"])
            #self.zero_favourite_box.add_widget(self.post_btn)
            self.all_liked_displayed_posts_list.append([self.my_liked_posts_list[b]["id"], self.post_btn, actual_maybe_like, self.my_liked_posts_list[b]["user_id"]])

        #self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
    
    def image_press(self, order_number, instance):
        if order_number == -1:
            self.manager.transition = FallOutTransition()
            self.manager.current = "image"
        elif order_number >= 0:
            self.go_to_user_profile(order_number)

    def like_press_2(self, order_number, instance):
        #num = int(instance.text)
        num = order_number
        like = (self.all_liked_displayed_posts_list[num][2] + 1) % 2
        if like == 1:
            instance.background_normal = 'images/heart2.png'
            access_my_info.add_or_remove_liked_post(self.all_liked_displayed_posts_list[num][0], like)
        if like == 0:
            instance.background_normal = 'images/heart.png'
            access_my_info.add_or_remove_liked_post(self.all_liked_displayed_posts_list[num][0], like)
        
        self.all_liked_displayed_posts_list[num][2] = like

    def go_to_user_profile_2(self, order_number):
        con = self.connection
        other_user_profile_screen = self.other_profile_screen
        user = con.get_post(self.all_displayed_posts_list[order_number][0])["user_id"]
        other_user_profile_screen.refresh_profile_screen(user)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    def name_press(self, order_number,instance):
        self.go_to_user_profile(order_number)

    def content_post_press(self, order_number, instance):
        #pyperclip.copy(instance.text)
        pass

    def second_post_press(self, instance):
        print(self.time_variable)
        self.time_variable = 2
        self.like_press(instance)

    def first_post_press(self, instance):
        #self.go_to_user_profile(order_number)
        print(self.time_variable)
        self.time_variable = 1
        self.post_instance = instance
        Clock.schedule_once(self.clock_def, 1)
        print(self.time_variable)
        print(7)
    
    def clock_def(self, instance):
        print("a")
        print(self.time_variable)
        if self.time_variable == 0:
            self.go_to_screen(self.post_instance)
        elif self.time_variable == 1:
            self.reply_post(self.post_instance)
        self.time_variable = 0

    def release_post(self, instance):
        print(10)
        print(self.time_variable)
        if self.time_variable == 1:
            self.time_variable = 0
        
    def go_to_screen(self, instance):
        print(11)
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(instance.user_name)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"
    
    def reply_post(self, instance):
        post_screen = self.post_screen
        post_screen.reply(instance.user_name)
        self.manager.transition = SlideTransition()
        self.manager.current = "create"
        self.manager.transition.direction = "left"
    
    def like_press(self, instance):
        print(3)
        order_number = instance.order_number
        print(9, order_number)
        background = instance.background
        print(77, background)
        if self.current_posts == 1:
            num = self.all_my_displayed_posts_list[order_number][2]
            num = (num + 1) % 2
            instance.background_normal = functions.get_post_image(background, num)
            access_my_info.add_or_remove_liked_post(self.all_my_displayed_posts_list[order_number][0], num)
            self.all_my_displayed_posts_list[order_number][2] = num
        elif self.current_posts == 2:
            num = self.all_liked_displayed_posts_list[order_number][2]
            num = (num + 1) % 2
            instance.background_normal = functions.get_post_image(background, num)
            access_my_info.add_or_remove_liked_post(self.all_liked_displayed_posts_list[order_number][0], num)
            self.all_liked_displayed_posts_list[order_number][2] = num

    def press_chat_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "chat"
        self.manager.transition.direction = "right"

    def press_search_btn(self, instance):
        #search_screen = self.search_screen
        #search_screen.refresh_search_screen()
        self.manager.transition = SlideTransition()
        self.manager.current = "search"
        self.manager.transition.direction = "right"

    def press_home_btn(self, instance):
        #home_screen = self.home_screen
        #home_screen.get_my_posts(0)
        self.manager.transition = SlideTransition()
        self.manager.current = "main"
        self.manager.transition.direction = "right"

    def press_make_posts_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "create"
        self.manager.transition.direction = "right"

    #def press_user_profile_btn(self, instance):
        #pass

    def add_screens(self, home_screen, search_screen, other_profile_screen, following_screen, chat_screen, post_screen):
        self.home_screen = home_screen
        self.search_screen = search_screen
        self.other_profile_screen = other_profile_screen
        self.following_screen = following_screen
        self.post_screen = post_screen
        self.chat_screen = chat_screen