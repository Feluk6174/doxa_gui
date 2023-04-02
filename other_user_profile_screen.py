#import kivy

from textwrap import shorten
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
from kivy.metrics import sp

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

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)


        self.content_box = BoxLayout (size_hint = (1, 1), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        self.user_image_name_box = BoxLayout(size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.content_grid.add_widget(self.user_image_name_box)

        self.user_image_box = BoxLayout(size_hint_x = None, width = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.user_image_name_box.add_widget(self.user_image_box)

        self.user_name_box =BoxLayout()
        self.user_image_name_box.add_widget(self.user_name_box)
        #

        self.description_box = BoxLayout(size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) * 2 / 5)
        self.content_grid.add_widget(self.description_box)

        #

        self.following_box = BoxLayout(size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.content_grid.add_widget(self.following_box)

        self.posts_header_btn = Button(text = "Posts", size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5, on_release = self.create_posts, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.content_grid.add_widget(self.posts_header_btn)

        #

        self.user_posts_box = BoxLayout(size_hint_y = None, height = 0, orientation = "vertical")
        self.content_grid.add_widget(self.user_posts_box)

        self.time_variable = 0
        self.thinking = 0
        self.posts_are_displayed = 0


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (border = (0, 0, 0, 0), background_normal = './images/mentions.png', background_down = './images/mentions.png')
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_bn = Button (border = (0, 0, 0, 0), background_normal = './images/search_white.png', background_down = './images/search_white.png', on_release = self.press_search_btn)
        self.ground_box.add_widget(self.search_bn)

        self.home_btn = Button (border = (0, 0, 0, 0), background_normal = './images/home.png', background_down = './images/home.png')
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
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
        self.posts_are_displayed = 0
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
        self.user_image_grid = functions.build_image(self, self.user_info["profile_picture"],-1, (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) / 5)
        self.user_image_box.add_widget(self.user_image_grid)

        self.user_name_box.clear_widgets()
        self.user_name_btn = Button(text = self.user_id, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.user_name_box.add_widget(self.user_name_btn)
        #self.user_name_btn.bind(on_release = self.user_name_press)

        self.description_box.clear_widgets()
        text = self.user_info["info"]
        print(text)
        text = functions.adapt_text_to_window(text, sp(15), Window.size[0])
        print(text)
        self.user_description_btn = Button(halign = 'center', text = text, size_hint_y = None, height = (Window.size[1]  - Window.size[0]*(1 / 5 + 1/5.08)) * 2 / 5, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.description_box.add_widget(self.user_description_btn)
        self.user_description_btn.bind(on_release = self.user_description_press)

        if self.following_user == 0:
            self.user_following_btn = Button(text = "Follow", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        elif self.following_user == 1:
            self.user_following_btn = Button(text = "Unfollow", border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.following_box.clear_widgets()
        self.following_box.add_widget(self.user_following_btn)
        self.user_following_btn.bind(on_release = self.user_following_press)

        self.user_posts_box.clear_widgets()
        self.content_grid.remove_widget(self.user_posts_box)
        #self.create_posts()
        print(10)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def think(self):
        print(88)
        if self.thinking == 1:
            self.banner.background_normal = "images/banner_loading.png"
        elif self.thinking == 0:
            self.banner.background_normal = "images/banner.png"

    def follow_posts_press(self, instance):
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def create_posts(self, instance):
        if self.posts_are_displayed == 0:
            self.thinking = 1
            self.think()
            Clock.schedule_once(self.create_posts_2)

    def create_posts_2(self, dt):
        print(11)
        conn = self.connection
        self.posts_list = conn.get_posts(user_name = self.user_id, sort_by = 'time_posted', sort_order = 'desc', num = 5)
        print(124)
        #self.my_posts_list = []
        #self.posts_list = functions.order_posts_by_timestamp(self.posts_list)

        print(125)
        #self.user_posts_box.clear_widgets()
        self.user_posts_box = BoxLayout(size_hint_y = None, height = 0, orientation = "vertical")
        #self.user_posts_box.height = len(self.posts_list) * (Window.size[1] - Window.size[0] * (1 / 5 + 1 / 5.08))
        self.content_grid.add_widget(self.user_posts_box)
        #self.content_grid.remove_widget(self.user_posts_box)
        print(12)
        my_liked_posts_id = access_my_info.get_liked_id()
        self.all_displayed_posts_list = []
        for a in range (len(self.posts_list)):
            actual_maybe_like = 0
            try:
                for liked_id in my_liked_posts_id:
                    if liked_id == self.posts_list[a]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            self.post_btn = functions.make_post_btn(self, self.posts_list[a]["user_id"], self.posts_list[a]["content"], self.posts_list[a]["time_posted"], actual_maybe_like, a, self.posts_list[a]["background_color"])
            self.user_posts_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.posts_list[a]["id"], self.post_btn, actual_maybe_like, self.posts_list[a]["user_id"]])

        self.next_post_btn = Button(size_hint_y = None, height = Window.size[1]/10, border = (0, 0, 0, 0), background_normal = "images/brick.png", background_down = "images/brick.png", on_release = self.create_new_posts, text = "Next")
        self.user_posts_box.add_widget(self.next_post_btn)

        self.user_posts_box.height = len(self.all_displayed_posts_list) * (Window.size[1] - Window.size[0] * (1 / 5 + 1 / 5.08)) + Window.size[1]/10
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        print(13)
        
        self.posts_are_displayed = 1

        self.thinking = 0
        self.think()
    
    def create_new_posts(self, instance):
        self.thinking = 1
        self.think()
        Clock.schedule_once(self.create_new_posts_2)
    
    def create_new_posts_2(self, dt):
        print(11)
        conn = self.connection
        self.posts_list = conn.get_posts(user_name = self.user_id, sort_by = 'time_posted', sort_order = 'desc', num = 1, offset = len(self.all_displayed_posts_list))
        print(124)
        #self.my_posts_list = []
        #self.posts_list = functions.order_posts_by_timestamp(self.posts_list)

        if self.posts_list != [{}]:
            self.posts_list = self.posts_list[0]
            self.user_posts_box.remove_widget(self.next_post_btn)
            print(125)
            #self.user_posts_box.clear_widgets()
            print(12)
            my_liked_posts_id = access_my_info.get_liked_id()
            actual_maybe_like = 0
            try:
                for liked_id in my_liked_posts_id:
                    if liked_id == self.posts_list["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            self.post_btn = functions.make_post_btn(self, self.posts_list["user_id"], self.posts_list["content"], self.posts_list["time_posted"], actual_maybe_like, len(self.all_displayed_posts_list), self.posts_list["background_color"])
            self.user_posts_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.posts_list["id"], self.post_btn, actual_maybe_like, self.posts_list["user_id"]])

            self.next_post_btn = Button(size_hint_y = None, height = Window.size[1]/10, border = (0, 0, 0, 0), background_normal = "images/brick.png", background_down = "images/brick.png", on_release = self.create_new_posts, text = "Next")
            self.user_posts_box.add_widget(self.next_post_btn)

            self.user_posts_box.height = self.user_posts_box.height + (Window.size[1] - Window.size[0] * (1 / 5 + 1 / 5.08))
            self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
            print(13)

        self.thinking = 0
        self.think()

    def image_press(self, order_number, instance):
        pass

    def like_press_2(self, order_number, instance):
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
    
    def second_post_press(self, instance):
        print(self.time_variable)
        self.time_variable = 2
    
    def third_post_press(self, instance):
        print(self.time_variable)
        self.time_variable = 3

    def first_post_press(self, instance):
        #self.go_to_user_profile(order_number)
        print(self.time_variable)
        self.time_variable = 1
        self.post_instance = instance
        Clock.schedule_once(self.clock_def, 0.5)
        print(self.time_variable)
        print(7)
    
    def clock_def(self, instance):
        print("a")
        print(self.time_variable)
        if self.time_variable == 0:
            self.go_to_screen(self.post_instance)
        elif self.time_variable == 1:
            self.reply_post(self.post_instance)
        elif self.time_variable == 2:
            self.like_press(self.post_instance)
        elif self.time_variable == 3:
            self.dislike_press(self.post_instance)
        self.time_variable = 0

    def release_post(self, instance):
        print(10)
        print(self.time_variable)
        if self.time_variable == 1:
            self.time_variable = 0
        
    def go_to_screen(self, instance):
        print(11)
    
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
        num = self.all_displayed_posts_list[order_number][2]
        if num == 1:
            num = 0
        else:
            num = 1
        instance.background_normal = functions.get_post_image(background, num)
        access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[order_number][0], num)
        self.all_displayed_posts_list[order_number][2] = num

    def dislike_press(self, instance):
        order_number = instance.order_number
        background = instance.background
        num = self.all_displayed_posts_list[order_number][2]
        if num == -1:
            num = 0
        elif num > -1:
            num = -1
        instance.background_normal = functions.get_post_image(background, num)
        access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[order_number][0], num)
        self.all_displayed_posts_list[order_number][2] = num

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
