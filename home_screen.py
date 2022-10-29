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
import random
from datetime import datetime
from kivy.graphics import BorderImage
from kivy.lang import Builder
#import pyperclip

import chat_screen, search_screen, profile_screen, functions, access_my_info, other_user_profile_screen, create_post_screen, following_screen
#from gui_1.new_gui.following_screen import FollowingScreen
import api

class MainScreen (Screen):
    def __init__(self, conn:api.Connection, my_profile_screen:profile_screen.ProfileScreen, my_search_screen:search_screen.SearchScreen, my_chat_screen:chat_screen.ChatScreen, my_post_screen:create_post_screen.PostUserScreen, my_other_profile_screen:other_user_profile_screen.OtherProfileScreen, my_following_screen:following_screen.FollowingScreen, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        print(3)

        self.profile_screen = my_profile_screen
        self.search_screen = my_search_screen
        self.other_profile_screen = my_other_profile_screen
        self.following_screen = my_following_screen

        print(31)

        my_profile_screen.add_screens(self, self.search_screen, self.other_profile_screen, self.following_screen)
        my_search_screen.add_screens(self, self.profile_screen, self.other_profile_screen)
        my_other_profile_screen.add_screens(self, self.profile_screen, self.search_screen)
        my_chat_screen.add_screens(self, self.profile_screen, self.search_screen, self.other_profile_screen)
        my_post_screen.add_screens(self, self.profile_screen, self.search_screen, self.other_profile_screen)
        my_following_screen.add_screens(self, self.profile_screen, self.other_profile_screen)


        #my_search_screen.refresh_search_screen(0)
        #my_profile_screen.refresh_profile_screen(0)
        print(32)

        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/logo.png', background_down = 'images/logo.png', on_release = self.get_my_posts)
        self.header_box.add_widget(self.logo)
        
        self.header_text = Label(text = "Small brother", size_hint = (2, 1))
        self.header_box.add_widget(self.header_text)
        
        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)
        
        print (33)
        
        self.content_box = BoxLayout (size_hint = (1, 0.9))
        self.main_all_box.add_widget(self.content_box)
        
        self.posts_grid = GridLayout(cols = 1, size_hint_y = None, spacing = 20)
        self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        
        self.posts_grid_scroll = ScrollView()
        self.posts_grid_scroll.add_widget (self.posts_grid)
        self.content_box.add_widget (self.posts_grid_scroll)

        #self.post_btn_test = Button(size_hint_y = None, height = 100, text = "Refresh Posts", on_release = self.get_my_posts)
        #self.posts_grid.add_widget(self.post_btn_test)

        self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = 100)
        self.posts_grid.add_widget(self.posts_box)

        self.all_posts_i_get = []
        print(34)
        self.get_my_posts(0)

        print(35)

        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (text = ("C"))
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_btn = Button (text = ("S"))
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_label = Label (text = ("Home"))
        self.ground_box.add_widget(self.home_label)

        self.make_posts_btn = Button (text = ("P"))
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (text = ("U"))
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(30)
        

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

    #def press_home_btn(self, instance):
    #    mainscreen.get_my_posts(0)

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

    def get_my_posts(self, instance):
        self.all_posts_i_get = []
        self.posts_box.clear_widgets()
        self.posts_grid.remove_widget(self.posts_box)

        all_my_following = access_my_info.get_following()
        print(301)
        my_liked_posts = access_my_info.get_liked_id()
        print(302)
        my_posts = self.connection.get_posts(sort_by= "time_posted", user_name=all_my_following, include_background_color=1)
        print(my_posts)
        self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = (Window.size[1] * 0.9 - Window.size[0] / 5) * (len(my_posts)))
        self.posts_grid.add_widget(self.posts_box)
        print(38)
        for a in range(len(my_posts)):
            #user_info = connection.get_user(all_test_posts[a]["user_id"])
            #print(user_info)
            print(304)
            #0 none, 1 yes
            actual_maybe_like = 0
            print(305)
            for liked in my_liked_posts:
                    if liked == my_posts[a][0]["id"]:
                        print(306)
                        actual_maybe_like = 1
            self.post_btn = functions.make_post_btn(self, my_posts[a]["user_id"], my_posts[a]["content"], my_posts[a]["time_posted"], actual_maybe_like, a, my_posts[a]["background_color"])
            self.posts_box.add_widget(self.post_btn)
            self.all_posts_i_get.append([my_posts[a]["id"], self.post_btn, actual_maybe_like])
            print(307)
        print(308)
        self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        print(39)

    """
    def get_new_follower_posts(self, connection):
        all_my_following = access_my_info.get_following()
        print(301)
        my_liked_posts = access_my_info.get_liked_id()
        print(302)
        my_posts = self.connection.get_posts(sort_by= "time_posted", user_name=all_my_following)
        all_test_posts_1 = []
        all_posts = []
        self.all_users = []
        print(all_my_following)
        for b in range (len(all_my_following)):
            print(all_my_following[b])
            follower_posts = connection.get_posts(user_name = all_my_following[b])
            follower_info = connection.get_user(all_my_following[b])
            self.all_users.append(follower_info)
            for post in follower_posts:
                all_test_posts_1.append([post, b])
        all_test_posts = functions.order_posts_by_timestamp(all_test_posts_1)
        
        for a in range(len(my_posts)):
            #user_info = connection.get_user(all_test_posts[a]["user_id"])
            #print(user_info)
            print(304)
            #0 none, 1 yes
            actual_maybe_like = 0
            print(305)
            for liked in my_liked_posts:
                    if liked == my_posts[a][0]["id"]:
                        print(306)
                        actual_maybe_like = 1
            self.post_btn = functions.make_post_btn(self, my_posts[a]["user_id"], my_posts[a]["content"], my_posts[a]["time_posted"], actual_maybe_like, a, my_posts[a]["background"])
            self.posts_box.add_widget(self.post_btn)
            self.all_posts_i_get.append([my_posts[a]["id"], self.post_btn, actual_maybe_like])
            print(307)
        print(308)
        return
        """
    def name_press(self, order_number, background, instance):
        #self.go_to_user_profile(order_number)
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(instance.text)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    """
    def go_to_user_profile(self, order_number):
        con = self.connection
        other_user_profile_screen = self.other_profile_screen
        print(self.all_posts_i_get)
        user = self.all_posts_i_get[order_number][0]
        print(user)
        user = con.get_post(user)
        print(user)
        user = user["user_id"]
        other_user_profile_screen.refresh_profile_screen(user)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"
        """

    #def image_press(self, order_number, instance):
    #    self.go_to_user_profile(order_number)

    def content_post_press(self, order_number, instance):
        #con = self.connection
        #text = con.get_user(self.all_posts_i_get[order_number][0])["content"]
        #pyperclip.copy(instance.text)
        pass

    def like_press(self, order_number, background, instance):
        num = self.all_posts_i_get[order_number][2]
        num = (num + 1) % 2
        if num == 1:
            access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], 1)
        if num == 0:
            access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], 0)
        instance.background_normal = functions.get_post_image(background, num)
        self.all_posts_i_get[order_number][2] = num