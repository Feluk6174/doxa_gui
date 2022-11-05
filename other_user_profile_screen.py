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

import access_my_info, home_screen, search_screen, profile_screen, functions, chat_screen

#profile_screen inport screen

class OtherProfileScreen (Screen):
    def __init__(self, conn, **kwargs):
        super(OtherProfileScreen, self).__init__(**kwargs)
        print(6)

        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/logo.png', background_down = 'images/logo.png', on_release = self.press_home_btn)
        self.header_box.add_widget(self.logo)

        self.header_text = Label(text = "Small brother", size_hint = (2, 1))
        self.header_box.add_widget(self.header_text)

        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)


        self.content_box = BoxLayout (size_hint = (1, 0.9), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        self.user_image_name_box = BoxLayout(size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 5)
        self.content_grid.add_widget(self.user_image_name_box)

        self.user_image_box = BoxLayout(size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 / 5)
        self.user_image_name_box.add_widget(self.user_image_box)

        self.user_name_box =BoxLayout()
        self.user_image_name_box.add_widget(self.user_name_box)
        #

        self.description_box = BoxLayout(size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 2 * 0.9 / 5)
        self.content_grid.add_widget(self.description_box)

        #

        self.following_box = BoxLayout(size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 5)
        self.content_grid.add_widget(self.following_box)

        self.posts_header_btn = Button(border = (0, 0, 0, 0), text = "Posts", size_hint_y = None, height = Window.size[0] / 1.61 / 3)
        self.content_grid.add_widget(self.posts_header_btn)

        #

        self.user_posts_box = BoxLayout(size_hint_y = None, height = 0, orientation = "vertical")
        self.content_grid.add_widget(self.user_posts_box)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (text = ("C"))
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_label = Label (text = ("Search"))
        self.ground_box.add_widget(self.search_label)

        self.home_btn = Button (text = ("H"))
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (text = ("P"))
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (text = ("U"))
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(60)

    
    def user_description_press(self, instance):
        #pyperclip.copy(instance.text)
        pass

    def user_following_press(self, instance):
        #follow or unfollow
        pass

    def refresh_profile_screen(self, user_id):
        con = self.connection
        self.user_id = user_id
        self.user_info = con.get_user(self.user_id)
        print("--")
        print(self.user_info)
        print("--")
        self.following_user = 0
        self.my_following = access_my_info.get_following()
        print(1, self.my_following)
        for following in self.my_following:
            if following == self.user_id:
                self.following_user = 1
        print(2, self.following_user)

        self.user_image_box.clear_widgets()
        self.user_image_grid = functions.build_image(self, self.user_info["profile_picture"],-1, (Window.size[1]  - Window.size[0] / 5) * 0.9 / 5)
        self.user_image_box.add_widget(self.user_image_grid)

        self.user_name_box.clear_widgets()
        self.user_name_btn = Button(text = self.user_id)
        self.user_name_box.add_widget(self.user_name_btn)
        #self.user_name_btn.bind(on_release = self.user_name_press)

        self.description_box.clear_widgets()
        self.user_description_btn = Button(text = self.user_info["info"], size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 2 * 0.9 / 5)
        self.description_box.add_widget(self.user_description_btn)
        self.user_description_btn.bind(on_release = self.user_description_press)

        if self.following_user == 0:
            self.user_following_btn = Button(text = "Follow")
        elif self.following_user == 1:
            self.user_following_btn = Button(text = "Unfollow")
        self.following_box.clear_widgets()
        self.following_box.add_widget(self.user_following_btn)
        self.user_following_btn.bind(on_release = self.user_following_press)

        self.user_posts_box.clear_widgets()
        self.create_posts()
        print(10)

    def create_posts(self):
        print(11)
        conn = self.connection
        self.posts_list = conn.get_posts(user_name = self.user_id)
        print(124)
        #self.my_posts_list = []
        self.posts_list = functions.order_posts_by_timestamp(self.posts_list)

        print(125)
        self.user_posts_box.clear_widgets()
        self.user_posts_box.height = len(self.posts_list) * Window.size[0] / 1.61

        print(12)
        my_liked_posts_id = access_my_info.get_liked_id()
        self.all_displayed_posts_list = []
        user_image = self.user_info["profile_picture"]
        for a in range (len(self.posts_list)):
            actual_maybe_like = 0
            try:
                for liked_id in my_liked_posts_id:
                    if liked_id == self.posts_list[a]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            self.post_btn = functions.make_post_btn(self, self.posts_list[a]["user_id"], user_image, self.posts_list[a]["flags"], self.posts_list[a]["content"], self.posts_list[a]["time_posted"], self.posts_list[a]["id"], actual_maybe_like, a)
            self.user_posts_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.posts_list[a]["id"], self.post_btn, actual_maybe_like])

        self.user_posts_box.height = len(self.all_displayed_posts_list) * Window.size[0] / 1.61
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        print(13)

    def image_press(self, order_number, instance):
        pass

    def like_press(self, order_number, instance):
        #num = int(instance.text)
        num = order_number
        like = (self.all_displayed_posts_list[num][2] + 1) % 2
        if like == 1:
            instance.background_normal = 'images/heart2.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[num][0], like)
        elif like == 0:
            instance.background_normal = 'images/heart.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[num][0], like)
        
        self.all_displayed_posts_list[num][2] = like
    
    def user_following_press(self, instance):
        foll = (self.following_user + 1) % 2
        if foll == 1:
            instance.text = "Unfollow"
            access_my_info.add_or_remove_following(self.user_id, foll)
        elif foll == 0:
            instance.text = "Follow"
            access_my_info.add_or_remove_following(self.user_id, foll)
        
        self.following_user = foll

    def name_press(self, order_number,instance):
        pass

    def image_press(self, order_number, instance):
        pass

    def content_post_press(self, order_number, instance):
        #copy
        pass


    def header_btn_press(self, instance):
        pass

    def press_chat_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "chat"
        self.manager.transition.direction = "right"
    
    #def press_search_btn(self, instance):
    #   pass

    def press_home_btn(self, instance):
        #home_screen = self.home_screen
        #home_screen.get_my_posts(0)
        self.manager.transition = SlideTransition()
        self.manager.current = "main"
        self.manager.transition.direction = "left"

    def press_make_posts_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "create"
        self.manager.transition.direction = "left"

    def press_user_profile_btn(self, instance):
        #profile_screen = self.profile_screen
        #profile_screen.refresh_profile_screen()
        self.manager.transition = SlideTransition()
        self.manager.current = "profile"
        self.manager.transition.direction = "left"
    
    def add_screens(self, home_screen, profile_screen, search_screen, chat_screen, post_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.search_screen = search_screen
        self.chat_screen = chat_screen
        self.post_screen = post_screen
