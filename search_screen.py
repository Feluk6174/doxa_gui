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
import home_screen, access_my_info
from datetime import datetime
#import pyperclip

import functions

if not __name__ == "home_screen":
    import home_screen


class SearchScreen (Screen):
    def __init__(self, conn, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        print(2)

        self.connection = conn

        self.main_all_box = BoxLayout(orientation = "vertical")
        self.add_widget(self.main_all_box)

        self.header_box = BoxLayout (size_hint = (1, 0.1))
        self.main_all_box.add_widget(self.header_box)

        self.logo = Button (border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/logo.png', background_down = 'images/logo.png', on_release = self.refresh_search_screen)
        self.header_box.add_widget(self.logo)
        
        self.header_text = Label(text = "Small brother", size_hint = (2, 1))
        self.header_box.add_widget(self.header_text)
        
        self.header_btn = Button(border = (0, 0, 0, 0), size_hint = (None, None), size = ((Window.size[1] - Window.size[0] / 5) * 0.1, (Window.size[1] - Window.size[0] / 5) * 0.1), background_normal = 'images/settings1.png', background_down = 'images/settings2.png')
        self.header_box.add_widget(self.header_btn)
        self.header_btn.bind(on_release = self.header_btn_press)
        

        self.content_box = BoxLayout (size_hint = (1, 0.9), orientation = "vertical")
        self.main_all_box.add_widget(self.content_box)
        
        self.content_box_scroll = ScrollView ()
        self.content_box.add_widget (self.content_box_scroll) 

        self.content_grid = GridLayout(cols = 1, size_hint_y = None)
        self.content_box_scroll.add_widget (self.content_grid)
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

        #self.content_grid.add_widget(Button(text = "a", size_hint_y = None, height = 100))
        
        self.display_header_box = BoxLayout(size_hint_y = None, height = Window.size[1] / 8)
        self.content_grid.add_widget(self.display_header_box)

        self.content_in_scroll_box = BoxLayout(orientation = 'vertical', size_hint_y = None)
        self.content_grid.add_widget(self.content_in_scroll_box)

        self.all_flags = [['images/check_verd.png'], ['images/red_cross.png'], ['images/age18.png'], ['images/blood.png'], ['images/fist.png'], ['images/soga.png'], ['images/art.png'], ['images/discuss.png'], ['images/politic.png'], ['images/sport.png'], ['images/videogame.png'], ['images/music.png']]
        for d in range(len(self.all_flags) - 2):
            self.all_flags[d + 2].append(str(d + 2))
        for x in range (len(self.all_flags) - 2):
            self.all_flags[x + 2].append(0)
        
        #firstposts
        #current: 1 = new, 2 = search
        self.current_posts = 0        

        #self.new_posts_header_press(0)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (text = ("C"))
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_label = Label (text = ("Search"))
        self.ground_box.add_widget(self.search_label)

        self.home_btn = Button (text = ("H"))
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (text = ("P"))
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (text = ("U"))
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(20)
        

    def header_btn_press(self, instance):
        pass

    def flag_press(self, instance):
        flag_number = int(instance.text)
        self.all_flags[flag_number][2] = (self.all_flags[flag_number][2] + 1) % 2 
        if self.all_flags[flag_number][2] == 1:
            instance.background_normal = self.all_flags[1][0]
        elif self.all_flags[flag_number][2] == 0:
            instance.background_normal = self.all_flags[flag_number][0]

    def search_header_press(self, instance):
        if self.current_posts == 1:
            self.content_in_scroll_box.clear_widgets()

        self.display_header_box.clear_widgets()

        for x in range (len(self.all_flags) - 2):
            self.all_flags[x + 2][2] = 0


        self.new_posts_header_display_btn = Button(text = "New")
        self.display_header_box.add_widget(self.new_posts_header_display_btn)
        self.new_posts_header_display_btn.bind(on_release = self.new_posts_header_press)

        self.search_header_display_label = Label (text = "Search")
        self.display_header_box.add_widget(self.search_header_display_label)

        self.search_user_header_btn = Button(size_hint_y = None, height = Window.size[1] / 15 / 2, text = "Search user:")
        self.content_in_scroll_box.add_widget(self.search_user_header_btn)

        self.search_user_input = TextInput(multiline = False, size_hint_y = None, height = Window.size[1] / 15)
        self.content_in_scroll_box.add_widget(self.search_user_input)
        #self.search_user_input.bind(on_text_validate = self.search_user_def)

        self.search_hastags_header_btn = Button(text = "Search hashtag:", size_hint_y = None, height = Window.size[1] / 15 / 2)
        self.content_in_scroll_box.add_widget(self.search_hastags_header_btn)

        self.search_post_hastags_input = TextInput(multiline = False, size_hint_y = None, height = Window.size[1] / 15)
        self.content_in_scroll_box.add_widget(self.search_post_hastags_input)
        #self.search_post_hastags.bind(on_text_validate = self.search_hastags_def)
   
        self.flag_filter_scroll = ScrollView (size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12)
        self.content_in_scroll_box.add_widget(self.flag_filter_scroll) 

        self.flag_grid = GridLayout(rows = 1, size_hint_x = None, size_hint_y = None, height = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12)
        self.flag_grid.bind(minimum_width = self.flag_grid.setter('width'))
        self.flag_filter_scroll.add_widget(self.flag_grid)
        
        for x in range (len(self.all_flags) - 2):
            self.flag_btn = Button(border = (0, 0, 0, 0), font_size = 1, size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12, text = str(self.all_flags[x + 2][1]), on_release = self.flag_press, background_normal = self.all_flags[x + 2][0])
            self.all_flags[x + 2].append(self.flag_btn)
            self.flag_grid.add_widget(self.flag_btn)
        self.flag_grid.bind(minimum_width = self.flag_grid.setter('width'))

        self.search_btn_box = BoxLayout(size_hint_y = None, height = Window.size[1] / 6)
        self.content_in_scroll_box.add_widget(self.search_btn_box)

        self.search_btn = Button(on_release = self.search_def, border = (0, 0, 0, 0), text = "Search")
        self.search_btn_box.add_widget(self.search_btn)

        self.clear_search_btn = Button(size_hint_y = None, height = Window.size[1] / 8, on_release = self.clear_search_def, border = (0, 0, 0, 0), text = "Clear")
        self.content_in_scroll_box.add_widget(self.clear_search_btn)

        self.searched_box = BoxLayout(size_hint_y = None, height = 0, orientation = "vertical")
        self.content_in_scroll_box.add_widget(self.searched_box)


        self.content_in_scroll_box.height = Window.size[1] / 8 + Window.size[1] / 6 + (Window.size[1] - Window.size[0] / 5) * 0.9 / 12 + Window.size[1] * 3 / 15
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.current_posts = 2
    
    def new_posts_header_press(self, instance):
        if self.current_posts == 2:
            self.content_in_scroll_box.clear_widgets()

        self.display_header_box.clear_widgets()


        self.new_posts_header_display_label = Label(text = "New")
        self.display_header_box.add_widget(self.new_posts_header_display_label)
        
        self.search_header_display_btn = Button (text = "Search")
        self.display_header_box.add_widget(self.search_header_display_btn)
        self.search_header_display_btn.bind(on_release = self.search_header_press)


        self.content_in_scroll_box.height = len(self.all_newest_posts_info) * Window.size[0] / 1.61

        #new posts
        self.create_newest_posts()
        
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.current_posts = 1

    def new_posts_refresh(self, instance):
        connection = self.connection
        self.all_new_posts_info = connection.get_posts(sort_by = "time_posted", sort_order = "desc", num = 10)
        self.all_newest_posts_info = functions.order_posts_by_timestamp(self.all_new_posts_info)
        print(self.all_newest_posts_info)

        self.create_newest_posts()
        #create a list with users searched. in next def we get info from list

    def create_newest_posts(self):
        self.all_displayed_posts_list = []
        conn = self.connection
        my_liked_posts_id = access_my_info.get_liked_id()
        for t in range(len(self.all_newest_posts_info)):
            user_post_info = conn.get_user(self.all_newest_posts_info[t]["user_id"])
            actual_maybe_like = 0
            try:
                for liked in my_liked_posts_id:
                    if liked == self.all_newest_posts_info[t]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            self.post_btn = functions.make_post_btn(self, self.all_newest_posts_info[t]["user_id"], user_post_info["profile_picture"], self.all_newest_posts_info[t]["flags"], self.all_newest_posts_info[t]["content"], self.all_newest_posts_info[t]["time_posted"], self.all_newest_posts_info[t]["id"], actual_maybe_like, t)
            self.content_in_scroll_box.add_widget(self.post_btn)
            self.all_displayed_posts_list.append([self.all_newest_posts_info[t]["id"], self.post_btn, actual_maybe_like])
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def refresh_search_screen(self, instance):
        if self.current_posts == 0 or self.current_posts == 2:
            self.new_posts_refresh(0)
        
        elif self.current_posts == 1:
            self.search_header_press(0)
            self.new_posts_refresh(0)

    def get_filter_flags(self):
        self.flag_list = ""
        for y in range (len(self.all_flags) - 2):
            self.flag_list = self.flag_list + str(self.all_flags[y + 2][2])
        return self.flag_list

    def name_press(self, order_number,instance):
        #self.go_to_user_profile(order_number)
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(instance.text)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    def image_press(self, order_number, instance):
        if order_number == -1:
            other_user_profile_screen = self.other_profile_screen
            other_user_profile_screen.refresh_profile_screen(self.actual_user)
            self.manager.transition = SlideTransition()
            self.manager.current = "profile"
            self.manager.transition.direction = "other_profile"
        elif order_number >= 0:
            self.go_to_user_profile(order_number)
    
    def go_to_user_profile(self, order_number):
        con = self.connection
        other_user_profile_screen = self.other_profile_screen
        post_id = self.all_displayed_posts_list[order_number][0]
        post = con.get_post(post_id)
        user = post["user_id"]
        other_user_profile_screen.refresh_profile_screen(user)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"

    def content_post_press(self, order_number, instance):
        #pyperclip.copy(instance.text)
        pass
    
    def clear_search_def(self, instance):
        self.search_btn_box.clear_widgets()
        self.search_btn = Button(text = "Search", on_release = self.search_def, border = (0, 0, 0, 0))
        self.search_btn_box.add_widget(self.search_btn)

        self.search_user_input.text = ""
        self.search_post_hastags_input.text = ""

        for x in range (len(self.all_flags) - 2):
            self.all_flags[x + 2][2] = 0
        
        self.flag_grid.clear_widgets()
        for x in range (len(self.all_flags) - 2):
            self.flag_btn = Button(border = (0, 0, 0, 0), font_size = 1, size_hint_x = None, width = (Window.size[1] - Window.size[0] / 5) * 0.9 / 12, text = str(self.all_flags[x + 2][1]), on_release = self.flag_press, background_normal = self.all_flags[x + 2][0])
            self.all_flags[x + 2].append(self.flag_btn)
            self.flag_grid.add_widget(self.flag_btn)
        self.flag_grid.bind(minimum_width = self.flag_grid.setter('width'))

        self.searched_box.clear_widgets()

        self.content_in_scroll_box.height = Window.size[1] / 8 + Window.size[1] / 6 + (Window.size[1] - Window.size[0] / 5) * 0.9 / 12 + Window.size[1] * 3 / 15
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def search_def(self, instance):
        conn = self.connection

        self.search_btn_box.clear_widgets()
        self.search_label_no_press = Label(text = "Search")
        self.search_btn_box.add_widget(self.search_label_no_press)
        #self.searched_box.clear_widgets()
        if self.search_post_hastags_input.text != "" or self.get_filter_flags() != "0000000000":
            print(1)
            searched_posts = conn.get_posts(hashtag = functions.filter_chars(self.search_post_hastags_input.text), exclude_flags = self.get_filter_flags(), num = 10)
            if searched_posts != ():
                self.all_displayed_posts_list = []
                my_liked_posts_id = access_my_info.get_liked_id()
                for t in range(len(searched_posts)):
                    user_post_info = conn.get_user(searched_posts[t]["user_id"])
                    actual_maybe_like = 0
                    try:
                        for liked in my_liked_posts_id:
                            if liked == searched_posts[t]["id"]:
                                actual_maybe_like = 1
                    except KeyError:
                        pass
                    self.post_btn = functions.make_post_btn(self, searched_posts[t]["user_id"], user_post_info["profile_picture"], searched_posts[t]["flags"], searched_posts[t]["content"], searched_posts[t]["time_posted"], searched_posts[t]["id"], actual_maybe_like, t)
                    self.searched_box.add_widget(self.post_btn)
                    self.all_displayed_posts_list.append([searched_posts[t]["id"], self.post_btn, actual_maybe_like])
                self.searched_box.height = Window.size[0]/1.61 * len(searched_posts)
                self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
            elif searched_posts == ():
                self.not_found_label = Label(text = "Nothing found", size_hint_y = None, height = Window.size[1]/8)
                self.searched_box.add_widget(self.not_found_label)
                self.searched_box.height = Window.size[1]/8
                self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
        elif self.search_post_hastags_input.text == "" and self.get_filter_flags() == "0000000000" and self.search_user_input.text != "":
            print(2)
            searched_user = conn.get_user(functions.filter_chars(self.search_user_input.text))
            print(searched_user)
            if searched_user == {}:
                self.not_found_label = Label(text = "Nothing found", size_hint_y = None, height = Window.size[1]/8)
                self.searched_box.add_widget(self.not_found_label)
                self.searched_box.height = Window.size[1]/8
                self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
            elif searched_user != {}:
                self.searched_user_box = BoxLayout(orientation = 'horizontal', size_hint_y = None, height = Window.size[1]/6)
                self.searched_box.add_widget(self.searched_user_box)

                self.searched_user_image_grid = functions.build_image(self, searched_user["profile_picture"], -1, Window.size[1]/6)
                self.searched_user_box.add_widget(self.searched_user_image_grid)

                self.searched_user_name_btn = Button(text = searched_user["user_name"], on_release = partial(self.name_press, 0))
                self.searched_user_box.add_widget(self.searched_user_name_btn)

                self.searched_box.height = Window.size[1]/6
                self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height

                self.actual_user = searched_user["user_name"]

        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    def like_press(self, order_number, instance):
        num = self.all_displayed_posts_list[order_number][2]
        num = (num + 1) % 2
        if num == 1:
            instance.background_normal = 'images/heart2.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[order_number][0], 1)
        if num == 0:
            instance.background_normal = 'images/heart.png'
            access_my_info.add_or_remove_liked_post(self.all_displayed_posts_list[order_number][0], 0)
        self.all_displayed_posts_list[order_number][2] = num

    def press_chat_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "chat"
        self.manager.transition.direction = "right"
    
    #def press_search_btn(self, instance):
    #   pass

    def press_home_btn(self, instance):
        #home_screen = self.home_screen
        #home_screen.get_my_posts(home_screen)
        self.manager.transition = SlideTransition()
        self.manager.current = "main"
        self.manager.transition.direction = "left"

    def press_make_posts_btn(self, instance):
        self.manager.transition = SlideTransition()
        self.manager.current = "create"
        self.manager.transition.direction = "left"

    def press_user_profile_btn(self, instance):
        #profile_screen = self.profile_screen
        #profile_screen.refresh_profile_screen(profile_screen)
        self.manager.transition = SlideTransition()
        self.manager.current = "profile"
        self.manager.transition.direction = "left"
    
    def add_screens(self, home_screen, profile_screen, other_profile_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.other_profile_screen = other_profile_screen
