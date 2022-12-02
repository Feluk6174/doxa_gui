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



#inici tot blanc
my_colors_from_screen = "3333333333333333333333333333333333333333333333333333333333333333"

def get_my_image():
    global my_colors_from_screen
    return my_colors_from_screen

class ImageScreen (Screen):
    def __init__(self, **kwargs):
        super(ImageScreen, self).__init__(**kwargs)

        self.main_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_box)

        self.first_big_box = BoxLayout(size_hint_y = None, height = Window.size[0] * 0.7, orientation = "horizontal")
        self.main_box.add_widget(self.first_big_box)

        #box to add space
        self.black_box_1_1 = BoxLayout()
        self.first_big_box.add_widget(self.black_box_1_1)

        self.image_grid = GridLayout(spacing = 5, cols = 8, size_hint = (None, None), size = (Window.size[0] * 0.7, Window.size[0] * 0.7))
        self.first_big_box.add_widget(self.image_grid)

        self.color_list = []
        for x in range (64):
            #add collor white
            self.color_list.append("3")

        for y in range (64):
            self.my_image_btn = Button(background_normal = '', font_size = 1, text = str(y), background_color = (1, 1, 1, 1), on_press = self.my_image_button_1)
            self.image_grid.add_widget(self.my_image_btn)

        self.black_box_1_2 = BoxLayout()
        self.first_big_box.add_widget(self.black_box_1_2)

    
        self.second_big_box = BoxLayout()
        self.main_box.add_widget(self.second_big_box)

        self.return_to_back_btn = Button(text = "Done", on_release = self.go_back, border = (0, 0, 0, 0), color = (0, 0, 0, 1), background_normal = "./images/brick.png", background_down = "./images/brick.png")
        self.second_big_box.add_widget(self.return_to_back_btn)


        self.third_big_box = BoxLayout(size_hint_y = None, height = Window.size[0] * 0.7, orientation = "horizontal")
        self.main_box.add_widget(self.third_big_box)

        self.black_box_2_1 = BoxLayout()
        self.third_big_box.add_widget(self.black_box_2_1)

        self.change_color_grid = GridLayout(cols = 4, size_hint = (None, None), size = (Window.size[0] * 0.7, Window.size[0] * 0.7))
        self.third_big_box.add_widget(self.change_color_grid)

        #(number(order), color(hexadecimal))
        self.all_colors = [("0", '#1B1A1A'), ("1", '#7e7e7e'), ("2", '#bebebe'), ("3", '#ffffff'), ("4", '#7e0000'), ("5", '#fe0000'), ("6", '#047e00'), ("7", '#06ff04'), ("8", '#7e7e00'), ("9", '#ffff04'), ("A", '#00007e'), ("B", '#0000ff'), ("C", '#7e007e'), ("D", '#fe00ff'), ("E", '#047e7e'), ("F", '#06ffff')]

        for x in range (len(self.all_colors)):
            self.change_color_btn = Button(border = (0, 0, 0, 0), background_normal = '', font_size = 1, text = str(x), background_color = kivy.utils.get_color_from_hex(self.all_colors[x][1]), on_press = self.change_color_button_2)
            self.change_color_grid.add_widget(self.change_color_btn)

        self.black_box_2_2 = BoxLayout()
        self.third_big_box.add_widget(self.black_box_2_2)

        #starting point is last one
        self.actual_on_press_change_btn = self.change_color_btn
    
    def go_back(self, instance):
        color_str = ""
        for a in range (len(self.color_list)):
            color_str = color_str + self.color_list[a]
        global my_colors_from_screen 
        my_colors_from_screen= color_str
        self.manager.transition = FallOutTransition()
        self.manager.current = "register"

    def my_image_button_1(self, instance):
        instance.background_color = self.actual_on_press_change_btn.background_color
        self.color_list[int(instance.text)] = self.all_colors[int(self.actual_on_press_change_btn.text)][0]

    def change_color_button_2(self, instance):
        self.actual_on_press_change_btn.background_normal = ""
        instance.background_normal = "images/check_verd.png"
        self.actual_on_press_change_btn = instance