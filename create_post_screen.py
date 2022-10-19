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

import access_my_info, home_screen, search_screen, profile_screen, functions

#profile_screen inport screen

class PostUserScreen (Screen):
    def __init__(self, conn, **kwargs):
        super(PostUserScreen, self).__init__(**kwargs)
        print(4)

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
        

        self.content_box = BoxLayout (size_hint = (1, 0.9))
        self.main_all_box.add_widget(self.content_box)
        
        self.content_grid = BoxLayout(orientation = "vertical")
        self.content_box.add_widget(self.content_grid)

        self.main_post_content_input = TextInput(multiline = True, size_hint = (1, 4))
        self.content_grid.add_widget(self.main_post_content_input)

        self.flag_box = BoxLayout(size_hint = (1, 0.5))
        self.content_grid.add_widget(self.flag_box)

        #flags
        #self.fl_bt = Button(text = "flags to add")
        #self.flag_box.add_widget(self.fl_bt)

        self.flag_grid = GridLayout(rows = 1, size_hint_x = None, spacing = 1)
        self.flag_grid.bind(minimum_width=self.flag_grid.setter('width'))
        
        self.flag_grid_scroll = ScrollView ()
        self.flag_grid_scroll.add_widget (self.flag_grid)
        self.flag_box.add_widget (self.flag_grid_scroll)

        self.all_flags = [['images/check_verd.png'], ['images/age18.png'], ['images/blood.png'], ['images/fist.png'], ['images/soga.png'], ['images/art.png'], ['images/discuss.png'], ['images/politic.png'], ['images/sport.png'], ['images/videogame.png'], ['images/music.png']]
        for d in range(len(self.all_flags) - 1):
            self.all_flags[d + 1].append(str(d + 1))
        
        for x in range (len(self.all_flags) - 1):
            self.flag_btn = Button(border = (0, 0, 0, 0), font_size = 1, size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12, text = str(self.all_flags[x + 1][1]), on_release = self.flag_press, background_normal = self.all_flags[x + 1][0])
            self.all_flags[x + 1].append(self.flag_btn)
            self.all_flags[x + 1].append(0)
            self.flag_grid.add_widget(self.flag_btn)
            
        self.send_post_btn = Button (text = "Publish", size_hint = (1, 1))
        self.content_grid.add_widget(self.send_post_btn)
        self.send_post_btn.bind(on_press = self.send_post_press)

        #self.last = Button (text = "All your posts", size_hint = (1, 0.67))
        #self.grid.add_widget(self.last)
        #self.last.bind(on_press = self.LastPosts)


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

        self.make_posts_label = Label (text = ("Post"))
        self.ground_box.add_widget(self.make_posts_label)

        self.user_profile_btn = Button (text = ("U"))
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(40)


    def header_btn_press(self, instance):
        pass
    
    def flag_press(self, instance):
        flag_number = int(instance.text)
        self.all_flags[flag_number][3] = (self.all_flags[flag_number][3] + 1) % 2
        if self.all_flags[flag_number][3] == 1:
            instance.background_normal = self.all_flags[0][0]
        if self.all_flags[flag_number][3] == 0:
            instance.background_normal = self.all_flags[flag_number][0]

    def send_post_press(self, instance):
        self.flag_list = ""
        for y in range (len(self.all_flags) - 1):
            self.flag_list = self.flag_list + str(self.all_flags[y + 1][3])
        self.send_post_final(self.flag_list, functions.adapt_text_to_server(functions.filter_chars(self.main_post_content_input.text)))
        self.main_post_content_input.text = ""
        for y in range (len(self.all_flags) - 1):
            if self.all_flags[y + 1][3] == 1:
                self.all_flags[y + 1][2].trigger_action(duration = 0)

    def send_post_final(self, post_flags, text_content):
        conn = self.connection
        user_name = access_my_info.get_user_name()
        private_key = access_my_info.get_priv_key()
        post_flags = str(post_flags)
        #post_likes = nlikes
        #date = int(time.time())
        post_id = abs(hash(str(text_content) + str(user_name) + str(post_flags) + str(time.time())))
        conn.post(text_content, post_id, user_name, post_flags, private_key)    

    def press_chat_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "chat"
        self.manager.transition.direction = "right"

    def press_search_btn(self, instance):
        #search_screen = self.search_screen
        #search_screen.popular_posts_header_press(0)
        self.manager.transition = SlideTransition()
        self.manager.current = "search"
        self.manager.transition.direction = "right"

    def press_home_btn(self, instance):
        #home_screen = self.home_screen
        #home_screen.get_my_posts(0)
        self.manager.transition = SlideTransition()
        self.manager.current = "main"
        self.manager.transition.direction = "right"

    #def press_make_posts_btn(self, instance):
    #    pass

    def press_user_profile_btn(self, instance):
        #profile_screen = self.profile_screen
        #profile_screen.refresh_profile_screen()
        self.manager.transition = SlideTransition()
        self.manager.current = "profile"
        self.manager.transition.direction = "left"
    
    def add_screens(self, home_screen, profile_screen, search_screen, other_profile_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.search_screen = search_screen
        self.other_profile_screen = other_profile_screen