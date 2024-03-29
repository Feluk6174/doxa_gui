#import kivy
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

import access_my_info, home_screen, search_screen, profile_screen, functions

#profile_screen inport screen

class FollowingScreen (Screen):
    def __init__(self, conn, **kwargs):
        super(FollowingScreen, self).__init__(**kwargs)
        
        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)
        

        self.content_box = BoxLayout (size_hint = (1, 0.9), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        #self.refresh_following()
        self.thinking = 0

        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (border = (0, 0, 0, 0), background_normal = './images/mentions.png', background_down = './images/mentions.png')
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_btn = Button (border = (0, 0, 0, 0), background_normal = './images/search_white.png', background_down = './images/search_white.png', on_release = self.press_search_btn)
        self.ground_box.add_widget(self.search_btn)

        self.home_btn = Button (border = (0, 0, 0, 0), background_normal = './images/home.png', background_down = './images/home.png')
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_label = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_label)
        self.make_posts_label.bind(on_release = self.press_user_profile_btn)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)


    def refresh_following(self):
        conn = self.connection
        self.users_info_list = []
        following_users = access_my_info.get_following()
        print(following_users)
        if following_users != {}:
            self.content_grid.clear_widgets()
            for x in range (len(following_users)):
                user_info = conn.get_user(following_users[x])
                print(user_info)
                print(user_info)

                self.user_box = BoxLayout(size_hint_y = None, height = Window.size[0]/1.61/2)
                self.content_grid.add_widget(self.user_box)

                self.image_grid = functions.build_image(self, user_info["profile_picture"], x, Window.size[0]/1.61/2)
                self.user_box.add_widget(self.image_grid)

                self.user_name_btn = Button(text = user_info["user_name"], on_release = self.go_to_user_profile_screen, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
                self.user_box.add_widget(self.user_name_btn)

                self.users_info_list.append([user_info, self.user_box])

    def header_btn_press(self, instance):
        pass

    def think(self):
        print(88)
        if self.thinking == 1:
            self.banner.background_normal = "images/banner_loading.png"
        elif self.thinking == 0:
            self.banner.background_normal = "images/banner.png"
    
    def go_to_user_profile_screen(self, instance):
        self.thinking = 1
        self.think()
        Clock.schedule_once(partial(self.go_to_user_profile_screen_2, instance))
        

    def go_to_user_profile_screen_2(self, instance, dt):
        con = self.connection
        other_user_profile_screen = self.other_profile_screen
        #user = self.users_info_list[order_number][0]["user_name"]
        other_user_profile_screen.refresh_profile_screen(instance.text)

        self.thinking = 0
        self.think()
        
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    def image_press(self, order_number, instance):
        #self.go_to_user_profile_screen(order_number, instance)
        pass

    def press_chat_btn(self, instance):
        #chat_screen.create_my_chats
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
        #home_screen.get_my_posts(0)
        self.manager.transition = SlideTransition()
        self.manager.current = "main"
        self.manager.transition.direction = "right"

    def press_make_posts_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "create"
        self.manager.transition.direction = "left"

    def press_user_profile_btn(self, instance):
        #profile_screen.refresh_profile_screen(profile_screen)
        self.manager.transition = SlideTransition()
        self.manager.current = "profile"
        self.manager.transition.direction = "left"

    def add_screens(self, home_screen, profile_screen, other_profile_screen, chat_screen, post_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.other_profile_screen = other_profile_screen
        self.chat_screen = chat_screen
        self.post_screen = post_screen