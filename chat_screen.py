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

import access_my_info, functions

class ChatScreen (Screen):
    def __init__(self, connection, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        print(1)

        self.connection = connection

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/logo.png', background_down = 'images/logo.png', on_release = self.refresh_chat)
        self.header_box.add_widget(self.logo)
        
        self.header_text = Label(text = "Small brother", size_hint = (2, 1))
        self.header_box.add_widget(self.header_text)
        
        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)


        self.content_box = BoxLayout (size_hint = (1, None), height = (Window.size[1]- Window.size[0] * (1 / 5 + 1 / 3.855)))
        self.main_all_box.add_widget(self.content_box)
        
        self.posts_grid = GridLayout(cols = 1, size_hint_y = None, spacing = 20)
        #self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        
        self.posts_grid_scroll = ScrollView()
        self.posts_grid_scroll.add_widget (self.posts_grid)
        self.content_box.add_widget (self.posts_grid_scroll)

        #self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = 100)
        #self.posts_grid.add_widget(self.posts_box)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_label = Label (text = ("Chat"))
        self.ground_box.add_widget(self.chat_label)

        self.search_btn = Button (text = ("S"))
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_btn = Button (text = ("H"))
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (text = ("P"))
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (text = ("U"))
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(10)

    def refresh_chat(self, instance):
        con = self.connection
        self.all_displayed_posts = []
        user = access_my_info.get_user_name()
        my_posts = con.get_posts(hashtag = "@" + user, sort_by = 'time_posted')
        my_liked_id = access_my_info.get_liked_id()
        for a in range(len(my_posts)):
            #user_info = connection.get_user(all_test_posts[a]["user_id"])
            #print(user_info)
            print(304)
            #0 none, 1 yes
            actual_maybe_like = 0
            print(305)
            for liked in my_liked_id:
                    if liked == my_posts[a]["id"]:
                        print(306)
                        actual_maybe_like = 1
            self.post_btn = functions.make_post_btn(self, my_posts[a]["user_id"], my_posts[a]["content"], my_posts[a]["time_posted"], actual_maybe_like, a, my_posts[a]["background_color"])
            self.posts_grid.add_widget(self.post_btn)
            self.all_displayed_posts.append([my_posts[a]["id"], self.post_btn, actual_maybe_like])
            #self.all_posts_i_get.append[my_posts[a]["user_id"]]
        self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
    
    def header_btn_press(self, instance):
        pass

    #def press_chat_btn(self, instance):
        #pass

    def press_search_btn(self, instance):
        #search_screen = self.search_screen
        #search_screen.refresh_search_screen()
        self.manager.transition = SlideTransition()
        self.manager.current = "search"
        self.manager.transition.direction = "left"

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
        self.manager.transition = SlideTransition()
        self.manager.current = "profile"
        self.manager.transition.direction = "left"

    def add_screens(self, home_screen, profile_screen, search_screen, other_profile_screen, post_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.search_screen = search_screen
        self.other_profile_screen = other_profile_screen
        self.post_screen = post_screen
