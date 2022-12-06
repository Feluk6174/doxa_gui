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
import  kivy.core.text.markup


import access_my_info, home_screen, search_screen, profile_screen, functions

#profile_screen inport screen

class PostUserScreen (Screen):
    def __init__(self, conn, **kwargs):
        super(PostUserScreen, self).__init__(**kwargs)
        print(4)

        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png')
        self.main_all_box.add_widget(self.banner)
        

        self.content_box = BoxLayout (size_hint = (1, 0.9), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)

        self.main_post_content_input = TextInput(multiline = True, size_hint = (1, 5), background_normal = './images/paper_base.png', background_disabled_normal = './images/paper_base.png')
        self.content_box.add_widget(self.main_post_content_input)

        self.background_box = BoxLayout(size_hint = (1, 0.5))
        self.content_box.add_widget(self.background_box)

        #backgrounds
        #self.fl_bt = Button(text = "backgrounds to add")
        #self.background_box.add_widget(self.fl_bt)

        self.background_grid = GridLayout(rows = 1, size_hint_x = None, spacing = 1)
        self.background_grid.bind(minimum_width=self.background_grid.setter('width'))
        
        self.background_grid_scroll = ScrollView ()
        self.background_grid_scroll.add_widget (self.background_grid)
        self.background_box.add_widget (self.background_grid_scroll)

        self.all_backgrounds = ['images/check_verd.png', 'images/paper_yellow.png', 'images/paper_green.png', 'images/paper_purple.png', 'images/paper_pink.png', 'images/paper_blue.png']
        self.all_background_buttons = []
        self.background_status = 1
        
        for x in range (len(self.all_backgrounds) - 1):
            self.background_btn = Button(border = (0, 0, 0, 0), font_size = 1, size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12, text = str(x + 1), on_release = self.background_press, background_normal = self.all_backgrounds[x + 1])
            self.all_background_buttons.append(self.background_btn)
            self.background_grid.add_widget(self.background_btn)
        
        self.nothing_btn = Button(size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 * (1 - 5/12), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.background_grid.add_widget(self.nothing_btn)

        self.main_post_content_input.background_normal = self.all_backgrounds[1]
        self.main_post_content_input.background_active = self.all_backgrounds[1]

        self.send_post_btn = Button (text = "Publish", size_hint = (1, 1), border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.content_box.add_widget(self.send_post_btn)
        self.send_post_btn.bind(on_press = self.send_post_press)

        #self.last = Button (text = "All your posts", size_hint = (1, 0.67))
        #self.grid.add_widget(self.last)
        #self.last.bind(on_press = self.LastPosts)


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

        self.make_posts_label = Button (border = (0, 0, 0, 0), background_normal = './images/post_white.png', background_down = './images/post_white.png')
        self.ground_box.add_widget(self.make_posts_label)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(40)


    def header_btn_press(self, instance):
        pass
    
    def background_press(self, instance):
        background_number = int(instance.text)
        self.background_status = background_number
        self.main_post_content_input.background_normal = self.all_backgrounds[background_number]
        self.main_post_content_input.background_active = self.all_backgrounds[background_number]
        instance.background_normal = self.all_backgrounds[0]
        for x in range (len(self.all_backgrounds)-1):
            if x+1 != background_number:
                self.all_background_buttons[x].background_normal = self.all_backgrounds[x+1]

    def reply(self, user):
        self.main_post_content_input.text = "@" + user + ' \n'

    def send_post_press(self, instance):
        if self.main_post_content_input.text != "" and len(self.main_post_content_input.text) < 255:
            text_content = functions.adapt_text_to_server(functions.filter_chars(self.main_post_content_input.text))
            conn = self.connection
            user_name = access_my_info.get_user_name()
            private_key = access_my_info.get_priv_key()
            post_background = str(self.background_status)
            #post_likes = nlikes
            #date = int(time.time())
            post_id = abs(hash(str(text_content) + str(user_name) + str(post_background) + str(time.time())))
            conn.post(text_content, post_id, user_name, post_background, private_key)    
            
            self.main_post_content_input.text = ""
            for x in range (len(self.all_backgrounds)-1):
                self.all_background_buttons[x].background_normal = self.all_backgrounds[x+1]

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
    
    def add_screens(self, home_screen, profile_screen, search_screen, other_profile_screen, chat_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.search_screen = search_screen
        self.other_profile_screen = other_profile_screen
        self.chat_screen = chat_screen