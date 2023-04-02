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
import  kivy.core.text.markup
#import pyperclip

import chat_screen, search_screen, profile_screen, functions, access_my_info, other_user_profile_screen, create_post_screen, following_screen
#from gui_1.new_gui.following_screen import FollowingScreen
import api

class MainScreen (Screen):
    def __init__(self, conn, my_profile_screen:profile_screen.ProfileScreen, my_search_screen:search_screen.SearchScreen, my_chat_screen:chat_screen.ChatScreen, my_post_screen:create_post_screen.PostUserScreen, my_other_profile_screen:other_user_profile_screen.OtherProfileScreen, my_following_screen:following_screen.FollowingScreen, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        print(3)

        self.profile_screen = my_profile_screen
        self.search_screen = my_search_screen
        self.other_profile_screen = my_other_profile_screen
        self.following_screen = my_following_screen
        self.chat_screen = my_chat_screen
        self.post_screen = my_post_screen

        print(31)

        my_profile_screen.add_screens(self, self.search_screen, self.other_profile_screen, self.following_screen, self.chat_screen, self.post_screen)
        my_search_screen.add_screens(self, self.profile_screen, self.other_profile_screen, self.chat_screen, self.post_screen)
        my_other_profile_screen.add_screens(self, self.profile_screen, self.search_screen, self.chat_screen, self.post_screen)
        my_chat_screen.add_screens(self, self.profile_screen, self.search_screen, self.other_profile_screen, self.post_screen)
        my_post_screen.add_screens(self, self.profile_screen, self.search_screen, self.other_profile_screen, self.chat_screen)
        my_following_screen.add_screens(self, self.profile_screen, self.other_profile_screen, self.chat_screen, self.post_screen)


        #my_search_screen.refresh_search_screen(0)
        #my_profile_screen.refresh_profile_screen(0)
        #my_chat_screen.refresh_chat(0)
        print(32)

        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png', on_release = self.banner_press)
        self.main_all_box.add_widget(self.banner)
        
        print (33)
        
        self.content_box = BoxLayout (size_hint = (1, None), height = (Window.size[1]- Window.size[0] * (1 / 5 + 1 / 5.08)))
        self.main_all_box.add_widget(self.content_box)
        
        self.posts_grid = GridLayout(cols = 1, size_hint_y = None)
        self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        
        self.posts_grid_scroll = ScrollView()
        #on_touch_stop()
        self.posts_grid_scroll.add_widget (self.posts_grid)
        self.content_box.add_widget (self.posts_grid_scroll)

        #self.post_btn_test = Button(size_hint_y = None, height = 100, text = "Refresh Posts", on_release = self.get_my_posts)
        #self.posts_grid.add_widget(self.post_btn_test)

        #self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = 100)
        #self.posts_grid.add_widget(self.posts_box)

        self.all_posts_i_get = []
        print(34)
        self.get_my_posts(0)
        self.time_variable = 0
        self.thinking = 0
        

        print(35)

        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (border = (0, 0, 0, 0), background_normal = './images/mentions.png', background_down = './images/mentions.png')
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_btn = Button (border = (0, 0, 0, 0), background_normal = './images/search.png', background_down = './images/search.png')
        self.ground_box.add_widget(self.search_btn)
        self.search_btn.bind(on_release = self.press_search_btn)

        self.home_bn = Button (border = (0, 0, 0, 0), background_normal = './images/home_white.png', background_down = './images/home_white.png', on_release = self.banner_press)
        self.ground_box.add_widget(self.home_bn)

        self.make_posts_btn = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(30)


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

    def banner_press(self, instance):
        self.thinking = 1
        self.think()
        Clock.schedule_once(self.get_my_posts)

    def get_my_posts(self, instance):
        self.all_posts_i_get = []
        self.posts_users_list = []
        self.posts_grid.clear_widgets()
        #self.posts_grid.remove_widget(self.posts_box)

        all_my_following = access_my_info.get_following()
        print(all_my_following)
        my_liked_posts = access_my_info.get_liked_id()
        my_disliked_posts = access_my_info.get_disliked_id()
        print(302)
        if not all_my_following == []:
            my_posts = self.connection.get_posts(sort_by= "time_posted", user_name=all_my_following, sort_order="desc", num = 5)
        else:
            my_posts = []
        #include_background_color=str(1)
        print(my_posts)
        self.posts_box = BoxLayout(orientation = "vertical", size_hint_y = None, height = (Window.size[1]- Window.size[0] * (1 / 5 + 1 / 5.08)) * (len(my_posts)) + Window.size[1]/10)
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
                    if liked == my_posts[a]["id"]:
                        print(306)
                        actual_maybe_like = 1
            for disliked in my_disliked_posts:
                    if disliked == my_posts[a]["id"]:
                        print(306)
                        actual_maybe_like = -1
            self.post_btn = functions.make_post_btn(self, my_posts[a]["user_id"], my_posts[a]["content"], my_posts[a]["time_posted"], actual_maybe_like, a, my_posts[a]["background_color"])
            self.posts_box.add_widget(self.post_btn)
            self.all_posts_i_get.append([my_posts[a]["id"], self.post_btn, actual_maybe_like, my_posts[a]["user_id"]])
            print(307)
            print(308)
            self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))
        print(39)

        if len(self.all_posts_i_get) != 0:
            self.next_post_btn = Button(size_hint_y = None, height = Window.size[1]/10, border = (0, 0, 0, 0), background_normal = "images/brick.png", background_down = "images/brick.png", on_release = self.next_post, text = "Next")
            self.posts_box.add_widget(self.next_post_btn)

        self.thinking = 0
        self.think()

    def next_post(self, instance):
        self.thinking = 1
        self.think()
        Clock.schedule_once(self.get_new_posts)
    
    def get_new_posts(self, instance):
        self.new_posts_i_get = []
        self.posts_users_list = []

        self.posts_box.remove_widget(self.next_post_btn)

        all_my_following = access_my_info.get_following()
        my_liked_posts = access_my_info.get_liked_id()
        my_disliked_posts = access_my_info.get_disliked_id()
        print(302)
        if not all_my_following == []:
            my_posts = self.connection.get_posts(sort_by= "time_posted", user_name=all_my_following, sort_order="desc", num = 1, offset = len(self.all_posts_i_get))
        else:
            my_posts = []
        #include_background_color=str(1)
        print(my_posts)
        print(len(my_posts))
        if my_posts != [{}]:
            self.posts_box.height = self.posts_box.height + (Window.size[1]- Window.size[0] * (1 / 5 + 1 / 5.08))
            print(38)
            actual_maybe_like = 0
            for liked in my_liked_posts:
                    if liked == my_posts[-1]["id"]:
                        print(306)
                        actual_maybe_like = 1
            for disliked in my_disliked_posts:
                    if disliked == my_posts[-1]["id"]:
                        print(306)
                        actual_maybe_like = -1
            self.post_btn = functions.make_post_btn(self, my_posts[-1]["user_id"], my_posts[-1]["content"], my_posts[-1]["time_posted"], actual_maybe_like, len(self.all_posts_i_get), my_posts[-1]["background_color"])
            self.posts_box.add_widget(self.post_btn)
            self.all_posts_i_get.append([my_posts[-1]["id"], self.post_btn, actual_maybe_like, my_posts[-1]["user_id"]])
            print(308)
            self.posts_grid.bind(minimum_height=self.posts_grid.setter('height'))

        self.next_post_btn = Button(size_hint_y = None, height = Window.size[1]/10, border = (0, 0, 0, 0), background_normal = "images/brick.png", background_down = "images/brick.png", on_release = self.next_post, text = "Next")
        self.posts_box.add_widget(self.next_post_btn)

        self.thinking = 0
        self.think()


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

    def think(self):
        print(88)
        if self.thinking == 1:
            self.banner.background_normal = "images/banner_loading.png"
        elif self.thinking == 0:
            self.banner.background_normal = "images/banner.png"
        #Clock.schedule_once(self.wait)

    """
    def name_press_2(self, order_number, background, instance):
        #self.go_to_user_profile(order_number)
        self.thinking = 1
        self.think()

        Clock.schedule_once(partial(self.name_press, order_number, background, instance), 0.01)        

    def name_press(self, order_number, background, instance, dt):
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(self.posts_users_list[order_number])

        self.thinking = 0
        self.think()

        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    
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

    def like_press_2(self, order_number, background, instance):
        num = self.all_posts_i_get[order_number][2]
        num = (num + 1) % 2
        if num == 1:
            access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], 1)
        if num == 0:
            access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], 0)
        instance.background_normal = functions.get_post_image(background, num)
        self.all_posts_i_get[order_number][2] = num

    def second_post_press(self, instance):
        print("b", self.time_variable)
        self.time_variable = 2
        print("c", self.time_variable)
        
    
    def third_post_press(self, instance):
        print(self.time_variable)
        self.time_variable = 3

    def first_post_press(self, instance):
        #self.go_to_user_profile(order_number)
        #print(self.time_variable)
        self.time_variable = 1
        self.post_instance = instance
        Clock.schedule_once(self.clock_def, 0.5)
        print(self.time_variable)
        print(7)
    
    def clock_def(self, instance):
        print("a")
        print(self.time_variable)
        if self.time_variable == 0:
            pass
            #self.thinking = 1
            #self.think()
            #Clock.schedule_once(partial(self.go_to_screen, self.post_instance))
        elif self.time_variable == 1:
            self.reply_post(self.post_instance)
        elif self.time_variable == 2:
            self.like_press(self.post_instance)
        elif self.time_variable == 3:
            self.dislike_press(self.post_instance)
        self.time_variable = 0

    def release_post(self, instance):
        print(10)
        print("d", self.time_variable)
        if self.time_variable == 1:
            self.time_variable = 0

    def go_to_screen(self, instance, dt):
        print(11)
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(instance.user_name)

        self.thinking = 0
        self.think()

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
        num = self.all_posts_i_get[order_number][2]
        if num == 1:
            num = 0
        else:
            num = 1
        instance.background_normal = functions.get_post_image(background, num)
        access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], num)
        self.all_posts_i_get[order_number][2] = num
    
    def dislike_press(self, instance):
        order_number = instance.order_number
        background = instance.background
        num = self.all_posts_i_get[order_number][2]
        if num == -1:
            num = 0
        elif num > -1:
            num = -1
        instance.background_normal = functions.get_post_image(background, num)
        access_my_info.add_or_remove_liked_post(self.all_posts_i_get[order_number][0], num)
        self.all_posts_i_get[order_number][2] = num
