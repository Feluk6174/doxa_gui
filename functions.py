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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.clock import Clock
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
import _markupbase
import unicodedata
#import emoji


import access_my_info



def change_time(date):
    date_post = int(date)
    dt_obj = datetime.fromtimestamp(date_post).strftime('%d-%m-%y')
    return dt_obj



def hex_color(hex_num):
    if hex_num == "0":
        col = '#000000'
    if hex_num == "1":
        col = '#7e7e7e'
    if hex_num == "2":
        col = '#bebebe'
    if hex_num == "3":
        col = '#ffffff'
    if hex_num == "4":
        col = '#7e0000'
    if hex_num == "5":
        col = '#fe0000'
    if hex_num == "6":
        col = '#047e00'
    if hex_num == "7":
        col = '#06ff04'
    if hex_num == "8":
        col = '#7e7e00'
    if hex_num == "9":
        col = '#ffff04'
    if hex_num == "A":
        col = '#00007e'
    if hex_num == "B":
        col = '#0000ff'
    if hex_num == "C":
        col = '#7e007e'
    if hex_num == "D":
        col = '#fe00ff'
    if hex_num == "E":
        col = '#047e7e'
    if hex_num == "F":
        col = '#06ffff'
    return col

class MyButton(Button):
    def __init__(self, screen, order_number, background, user, like, date, content, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.markup = True
        self.background_normal = get_post_image(background, like)
        self.screen = screen
        self.order_number = order_number
        self.background = background
        self.text = "[size=15]" + str(change_time(date)) + "[/size]                                                            " + "\n \n \n" + "[size=20]" + adapt_text_to_window(content, 20, Window.size[0]) + "[/size]" + " \n \n " + "                                [b][size=20]- " + user +"[/b][/size]"
        self.color = (0, 0, 0, 1)
        #self.font_size = 20
        self.shorten = True
        #self.split_str = True
        self.halign = 'center'
        self.size_hint_y = None 
        self.height = Window.size[1]- Window.size[0] * (1 / 5 + 1 / 3.855)
        self.orientation = "vertical"
        self.user_name = user
        self.last_clicked = 1

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            print(6)
            screen = self.screen
            screen.release_post(self)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            screen = self.screen
            if touch.is_double_tap:
                screen = self.screen
                print(1)
                screen.second_post_press(self)
                #screen variable of clicks
                #screen.time_pressed *= -1
            else:
                print(8)
                screen = self.screen
                screen.first_post_press(self)
                #partial(screen.name_press, self)
                
                (print(2))
                #screen.name_press(self.order_number, self.background, self)

def build_image(screen, user_image, order_number, width):
    image_grid = GridLayout(cols = 8, size_hint_x = None)
    image_grid.width = width
    for x in range (64):
        color_bit = Button(background_normal = '', background_color = kivy.utils.get_color_from_hex(hex_color(user_image[x])), on_release = partial(screen.image_press, order_number))
        image_grid.add_widget(color_bit)
    return image_grid

def filter_chars(text:str):
    invalid_chars = ["\\", "\'", "\"", "\n", "\t", "\r", "\0", "%", "\b", ";", "=", "\u259e"]

    for char in invalid_chars:
        if char in text:
            text = text.split(char)
            text = "".join(text)
    return text

def get_post_image(num, like):
    num = int(num)
    like = int(like)
    if like == 0:
        if num == 1:
            return "./images/paper_yellow.png"
        elif num == 2:
            return "./images/paper_green.png"
        elif num == 3:
            return "./images/paper_purple.png"
        elif num == 4:
            return "./images/paper_pink.png"
        elif num == 5:
            return "./images/paper_blue.png"
    elif like == 1:
        if num == 1:
            return "./images/paper_yellow_heart.png"
        elif num == 2:
            return "./images/paper_green_heart.png"
        elif num == 3:
            return "./images/paper_purple_heart.png"
        elif num == 4:
            return "./images/paper_pink_heart.png"
        elif num == 5:
            return "./images/paper_blue_heart.png"

#def crear botó
def make_post_btn(screen, user_name, text_content, date, like_self, order_number, background):
    
    #post = BoxLayout(size_hint_y = None, height = Window.size[1] * 0.9 - Window.size[0] / 5, orientation = "vertical")
    
    main_btn = MyButton(screen=screen, order_number= order_number, background=background, user = user_name, like = like_self, date=date, content = text_content)
    #post.add_widget(main_btn)

    #text = str(change_time(date)) + "               " + "\n" + adapt_text_to_window(text_content, 30, Window.size[0]) + "\n" + "           - " + user_name
    #main_btn.text = text

    return main_btn


def order_posts_by_timestamp(posts_to_order):
    length = len(posts_to_order)
    how_big_list = []
    final_list = []
    for a in range (length):
        how_big_list.append(0)
        for b in range (length):
            #if posts_to_order[a]["time_stamp"] > posts_to_order[b]["time_stamp"]:
            #    how_big_list[a][1] = how_big_list[a][1] + 1
            print(posts_to_order)
            print(a, b, posts_to_order[a])
            if posts_to_order[a]["time_posted"] > posts_to_order[b]["time_posted"]:
                how_big_list[a] = how_big_list[a] + 1
    for c in range (length):
        for d in range (length):
            if how_big_list[c] == d:
                final_list.append(posts_to_order[c])
    return final_list


def check_new_chat_alarm():
    pass

def change_my_description(description):
    access_my_info.change_my_description(description)
    #enviar a conn

def change_my_profile_image(color_string):
    access_my_info.change_my_image(color_string)
    #enviar a conn

def adapt_text_to_server(text:str):
    text = text.split("\n")
    text = " ".join(text)
    return text

def adapt_text_to_window(text:str, text_size, window_size):
    text_to_cut_lenght = len(text)
    letters_per_line = int(window_size / text_size)
    jump_done = 0

    final_text = []

    words = text.split(" ")
    i = 0
    while i < len(words):
        if len(words[i]) >= letters_per_line:
            final_text.append(words[i])
            i += 1
        else:
            working_words = words[i]
            j = 1
            while not len(working_words) >= letters_per_line:
                try:
                    working_words += " " + words[i+j]
                except IndexError:
                    final_text.append(working_words)
                    i = len(words)
                    break
                j += 1
            else:
                final_text.append(working_words)
                i += j
            
    print("f_t", final_text)
    final_text = "\n".join(final_text)
    print("f_t", final_text)
    return final_text



