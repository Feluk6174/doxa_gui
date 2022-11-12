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

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png', on_release = self.refresh_chat)
        self.main_all_box.add_widget(self.banner)


        self.content_box = BoxLayout (size_hint = (1, None), height = (Window.size[1]- Window.size[0] * (1 / 5 + 1 / 5.08)))
        self.main_all_box.add_widget(self.content_box)
        
        self.posts_grid = GridLayout(cols = 1, size_hint_y = None, spacing = 20)
        #self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        
        self.posts_grid_scroll = ScrollView()
        self.posts_grid_scroll.add_widget (self.posts_grid)
        self.content_box.add_widget (self.posts_grid_scroll)

        self.time_variable = 0

        #self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = 100)
        #self.posts_grid.add_widget(self.posts_box)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_label = Button (border = (0, 0, 0, 0), background_normal = './images/mentions_white.png', background_down = './images/mentions_white.png')
        self.ground_box.add_widget(self.chat_label)

        self.search_btn = Button (border = (0, 0, 0, 0), background_normal = './images/search.png', background_down = './images/search.png')
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_btn = Button (border = (0, 0, 0, 0), background_normal = './images/home.png', background_down = './images/home.png')
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
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
        self.manager.transition.direction = "left"
    
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
        num = self.all_displayed_posts[order_number][2]
        num = (num + 1) % 2
        instance.background_normal = functions.get_post_image(background, num)
        access_my_info.add_or_remove_liked_post(self.all_displayed_posts[order_number][0], num)
        self.all_displayed_posts[order_number][2] = num

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
