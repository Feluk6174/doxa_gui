#import kivy
from kivy.app import App
from functools import partial
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
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

import functions, access_my_info


class ConversationScreen (Screen):
    def __init__(self, connection, chat_info, **kwargs):
        super(ConversationScreen, self).__init__(**kwargs)

        self.connection = connection
        self.type = chat_info["type"]
        if self.type == 0:
            self.user = chat_info["users"]
            self.user_info = connection.get_user(self.user)

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        self.image_box = BoxLayout()
        self.header_box.add_widget(self.image_box)

        self.header_name_btn = Button(size_hint = (2, 1), on_release = self.user_name_press)
        self.header_box.add_widget(self.header_name_btn)
        
        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 10) * 0.1, (Window.size[1] - Window.size[0] / 10) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)
        
        
        if self.type == 0:
            self.chat_image_grid = functions.build_image(self, self.user_info["profile_image"], 0, (Window.size[1] - Window.size[0] / 10) * 0.1)
            self.header_name_btn.text = self.user_info["user_name"]
            self.image_box.add_widget(self.chat_image_grid)
        elif self.type == 1:
            self.chat_image_grid = functions.build_image(self, chat_info["profile_image"], 0, (Window.size[1] - Window.size[0] / 10) * 0.1)
            self.header_name_btn.text = chat_info["chat_name"]
            self.image_box.add_widget(self.chat_image_grid)


        self.float_content_layout = FloatLayout()
        self.main_all_box.add_widget(self.float_content_layout)

        self.content_box = BoxLayout(size_hint_y = 0.9, pos_hint = {"x" : 0, "y" : Window.size[0] / 10})
        self.float_content_layout.add_widget(self.content_box)

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        self.content_grid_scroll = ScrollView ()
        self.content_grid_scroll.add_widget (self.content_grid)
        self.content_box.add_widget (self.content_grid_scroll)

        #create_conversation(0, 50)
        #go to bottom to conversation

        self.ground_box = BoxLayout(size_hint_y = None, height = Window.size[0] / 10, pos_hint = {"x" : 0, "y" : 0})
        self.float_content_layout.add_widget(self.ground_box)

        self.write_message_input = TextInput(multiline = True)
        self.ground_box.add_widget(self.write_message_input)
        #self.write_message_input.bind(on_select = self.text_pressed)

        self.send_message_btn = Button(border = (0, 0, 0, 0), background_normal = 'images/check_verd', on_release = self.send_message_press, size_hint = (None, None), size = (Window.size[0] / 10, Window.size[0] / 10))
        self.ground_box.add_widget(self.send_message_btn)


    def image_press(self, instance):
        self.user_press()

    def user_name_press(self, instance):
        self.user_press

    def user_press():
        #go to user profile
        pass

    def send_message_press(self, instance):
        conn = self.connection
        if self.write_message_input.text != "":
            conn.send_message(self.write_message_input.text, access_my_info.get_user_name, )

    def header_btn_press(self, instance):
        pass

    def text_pressed(self):
        #self.write_message_input.pos_hint = {"x" : 0, "y" : 0}
        pass

    def refresh_chat():
        pass

