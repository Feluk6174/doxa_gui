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

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        print(56)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/logo.png', background_down = 'images/logo.png', on_release = self.refresh_profile_screen)
        self.header_box.add_widget(self.logo)
        
        print(57)

        self.header_text = Label(text = "Small brother", size_hint = (2, 1))
        self.header_box.add_widget(self.header_text)
        
        print(58)

        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)
        
        print(53)

        self.content_box = BoxLayout (size_hint = (1, 0.9), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        self.user_image_name_box = BoxLayout(orientation = "horizontal", size_hint_y = None, height = (Window.size[1]  - Window.size[0] / 5) * 0.9 / 5)
        self.content_grid.add_widget(self.user_image_name_box)

        self.user_image_box = BoxLayout(size_hint_x = None, width = (Window.size[1]  - Window.size[0] / 5) * 0.9 / 5)
        self.user_image_name_box.add_widget(self.user_image_box)
        
        print(54)

        self.user_image_grid = functions.build_image(self, access_my_info.get_profile_image(), -1, (Window.size[1]  - Window.size[0] / 5) * 0.9 / 5)
        self.user_image_box.add_widget(self.user_image_grid)

        self.user_name_btn = Button(text = access_my_info.get_user_name())
        self.user_image_name_box.add_widget(self.user_name_btn)
        #self.user_name_btn.bind(on_release = self.user_name_press)

        print(52)

        self.description_box = BoxLayout(size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 2 * 0.9 / 5)
        self.content_grid.add_widget(self.description_box)

        self.user_description_btn = Button(text = functions.adapt_text_to_window(access_my_info.get_description(), 15, Window.size[0]), size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 2 * 0.9 / 5)
        self.description_box.add_widget(self.user_description_btn)
        self.user_description_btn.bind(on_release = self.user_description_press)

        print(55)

        self.user_following_btn = Button(text = "Following", size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 5)
        self.content_grid.add_widget(self.user_following_btn)
        self.user_following_btn.bind(on_release = self.user_following_press)

        self.user_posts_header_box = BoxLayout(size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 5)
        self.content_grid.add_widget(self.user_posts_header_box)

        self.user_posts_btn = Button(text = "My Posts", on_release = self.user_posts_press)
        self.user_posts_header_box.add_widget(self.user_posts_btn)
        
        self.favourite_posts_btn = Button (text = "Favourites")
        self.user_posts_header_box.add_widget(self.favourite_posts_btn)
        self.favourite_posts_btn.bind(on_release = self.user_favourites_press)

        #firstposts
        #current: 1 = my, 2 = fav
        self.current_posts = 0
        
        print(51)
        
        #self.user_posts_press(0)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (text = ("C"))
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_btn = Button (text = ("S"))
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_btn = Button (text = ("H"))
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (text = ("P"))
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_label = Label (text = ("User"))
        self.ground_box.add_widget(self.user_profile_label)

        print (50)


    def user_description_press(self, instance):
        self.text_description = functions.adapt_text_to_server(self.user_description_btn.text)
        self.description_box.clear_widgets()

        self.user_description_input = TextInput(text = self.text_description, multiline = False, on_text_validate = self.change_description)
        self.description_box.add_widget(self.user_description_input)

    def change_description(self, instance):
        self.text_description = functions.adapt_text_to_window(functions.filter_chars(self.user_description_input.text), 15, Window.size[0])
        self.connection.change_info(access_my_info.get_user_name(), functions.filter_chars(self.user_description_input.text), access_my_info.get_priv_key())
        self.description_box.clear_widgets()

        functions.change_my_description(self.text_description)

        self.user_description_btn = Button(text = self.text_description, on_release = self.user_description_press)
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
        
        if self.current_posts != 1:
            self.user_posts_press(0)
        elif self.current_posts == 1:
            self.user_favourites_press(0)
            self.user_posts_press(0)

    def user_posts_press(self, instance):
        conn = self.connection
        self.my_posts_list = conn.get_posts(user_name = self.user_name_btn.text, sort_order = 'desc')
        #self.my_posts_list = access_my_info.get_my_posts()
        #self.my_posts_list = []
        #self.my_posts_list = functions.order_posts_by_timestamp(self.my_posts_list)

        if self.current_posts == 2:
            self.favourite_posts_box.clear_widgets()
            self.content_grid.remove_widget(self.favourite_posts_box)

        self.user_posts_header_box.clear_widgets()

        self.user_posts_label = Label(text = "My Posts")
        self.user_posts_header_box.add_widget(self.user_posts_label)
        
        self.favourite_posts_btn = Button (text = "Favourites")
        self.user_posts_header_box.add_widget(self.favourite_posts_btn)
        self.favourite_posts_btn.bind(on_release = self.user_favourites_press)


        #my posts
        self.create_my_posts()

        self.current_posts = 1

    def user_favourites_press(self, instance):
        conn = self.connection
        #with connection or in phone memory
        self.my_liked_list_id = access_my_info.get_liked_id()
        self.my_liked_list = []
        for post_id in self.my_liked_list_id:
            posts_to_include = conn.get_post(post_id)
            self.my_liked_list.append(posts_to_include)
        #self.my_liked_posts_list = []
        self.my_liked_posts_list = functions.order_posts_by_timestamp(self.my_liked_list)

        if self.current_posts == 1:
            self.my_posts_box.clear_widgets()
            self.content_grid.remove_widget(self.my_posts_box)

        self.user_posts_header_box.clear_widgets()

        self.user_posts_btn = Button(text = "My Posts")
        self.user_posts_header_box.add_widget(self.user_posts_btn)
        self.user_posts_btn.bind(on_release = self.user_posts_press)

        self.favourite_posts_label = Label (text = "Favourites")
        self.user_posts_header_box.add_widget(self.favourite_posts_label)


        #favourite posts
        self.create_liked_posts()

        self.current_posts = 2

    def create_my_posts(self):
        #conn = self.connection

        self.my_posts_box = BoxLayout(size_hint_y = None, height = len(self.my_posts_list) * Window.size[0] / 1.61, orientation = "vertical")
        self.content_grid.add_widget(self.my_posts_box)

        my_liked_posts_id = access_my_info.get_liked_id()
        self.all_displayed_posts_list = []
        my_image = access_my_info.get_profile_image()
        for a in range (len(self.my_posts_list)):
            actual_maybe_like = 0
            try:
                for liked_id in my_liked_posts_id:
                    if liked_id == self.my_posts_list[a]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            self.post_btn = functions.make_post_btn(self, self.my_posts_list[a]["user_id"], my_image, self.my_posts_list[a]["flags"], self.my_posts_list[a]["content"], self.my_posts_list[a]["time_posted"], self.my_posts_list[a]["id"], actual_maybe_like, a)
            self.my_posts_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.my_posts_list[a]["id"], self.post_btn, actual_maybe_like])

        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
    
    def create_liked_posts(self):
        conn = self.connection

        self.favourite_posts_box = BoxLayout(size_hint_y = None, height = len(self.my_liked_posts_list) * Window.size[0] / 1.61, orientation = "vertical")
        self.content_grid.add_widget(self.favourite_posts_box)

        actual_maybe_like = 1
        for b in range (len(self.my_liked_posts_list)):
            user_liked_info = conn.get_user(self.my_liked_posts_list[b]["user_id"])        
            self.post_btn = functions.make_post_btn(self, self.my_liked_posts_list[b]["user_id"], user_liked_info["profile_picture"], self.my_liked_posts_list[b]["flags"], self.my_liked_posts_list[b]["content"], self.my_liked_posts_list[b]["time_posted"], self.my_liked_posts_list[b]["id"], actual_maybe_like, b)
            self.favourite_posts_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.my_liked_posts_list[b]["id"], self.post_btn, actual_maybe_like])
        
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
    
    def image_press(self, order_number, instance):
        if order_number == -1:
            self.manager.transition = FallOutTransition()
            self.manager.current = "image"
        elif order_number >= 0:
            self.go_to_user_profile(order_number)

    def like_press(self, order_number, instance):
        #num = int(instance.text)
        num = order_number
        like = (self.all_displayed_posts_list[num][2] + 1) % 2
        if like == 1:
            instance.background_normal = 'images/heart2.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[num][0], like)
        if like == 0:
            instance.background_normal = 'images/heart.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[num][0], like)
        
        self.all_displayed_posts_list[num][2] = like

    def go_to_user_profile(self, order_number):
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

    def header_btn_press(self, instance):
        pass

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