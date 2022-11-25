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

        self.banner = Button (border = (0, 0, 0, 0), size_hint = (1, None), height = Window.size[0] / 5.08, background_normal = 'images/banner.png', background_down = 'images/banner.png', on_release = self.refresh_search_screen)
        self.main_all_box.add_widget(self.banner)
        

        self.content_box = BoxLayout (orientation = "vertical")
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

        #self.all_flags = ['images/check_verd.png', 'images/red_cross.png', 'images/pink.jpeg']
        #self.sort_list = [0, 0]

        #firstposts
        #current: 1 = new, 2 = search
        self.current_posts = 0
        self.time_variable = 0 
        
        self.all_displayed_new_posts_list = []
        self.new_posts_box=BoxLayout()

        #self.new_posts_header_press(0)
        
        self.search_header_display_btn = Button (text = "Search")
        self.display_header_box.add_widget(self.search_header_display_btn)
        self.search_header_display_btn.bind(on_release = self.search_header_press)

        self.new_posts_header_display_btn = Button(text = "New")
        self.display_header_box.add_widget(self.new_posts_header_display_btn)
        self.search_header_press(0)


        self.ground_box = BoxLayout (size_hint_y = None, height = Window.size[0] / 5)
        self.main_all_box.add_widget(self.ground_box)

        self.chat_btn = Button (border = (0, 0, 0, 0), background_normal = './images/mentions.png', background_down = './images/mentions.png')
        self.ground_box.add_widget(self.chat_btn)
        self.chat_btn.bind(on_release = self.press_chat_btn)

        self.search_label = Button (border = (0, 0, 0, 0), background_normal = './images/search_white.png', background_down = './images/search_white.png')
        self.ground_box.add_widget(self.search_label)

        self.home_btn = Button (border = (0, 0, 0, 0), background_normal = './images/home.png', background_down = './images/home.png')
        self.ground_box.add_widget(self.home_btn)
        self.home_btn.bind(on_release = self.press_home_btn)

        self.make_posts_btn = Button (border = (0, 0, 0, 0), background_normal = './images/post.png', background_down = './images/post.png')
        self.ground_box.add_widget(self.make_posts_btn)
        self.make_posts_btn.bind(on_release = self.press_make_posts_btn)

        self.user_profile_btn = Button (border = (0, 0, 0, 0), background_normal = './images/profile.png', background_down = './images/profile.png')
        self.ground_box.add_widget(self.user_profile_btn)
        self.user_profile_btn.bind(on_release = self.press_user_profile_btn)

        print(20)


    def search_header_press(self, instance):
        if self.current_posts == 1:
            self.content_in_scroll_box.clear_widgets()

        self.display_header_box.clear_widgets()

        #self.sort_list = [0, 0]

        self.search_header_display_label = Label (text = "Search")
        self.display_header_box.add_widget(self.search_header_display_label)

        self.new_posts_header_display_btn = Button(text = "New")
        self.display_header_box.add_widget(self.new_posts_header_display_btn)
        self.new_posts_header_display_btn.bind(on_release = self.new_posts_header_press)


        self.search_header_btn = Button(size_hint_y = None, height = Window.size[1] / 15 / 2, text = "Search @user or #hashtag: ")
        self.content_in_scroll_box.add_widget(self.search_header_btn)

        self.search_input = TextInput(multiline = False, size_hint_y = None, height = Window.size[1] / 15)
        self.content_in_scroll_box.add_widget(self.search_input)
        #self.search_user_input.bind(on_text_validate = self.search_user_def)

        """
        self.search_hastags_header_btn = Button(text = "Search hashtag:", size_hint_y = None, height = Window.size[1] / 15 / 2)
        self.content_in_scroll_box.add_widget(self.search_hastags_header_btn)

        self.search_post_hastags_input = TextInput(multiline = False, size_hint_y = None, height = Window.size[1] / 15)
        self.content_in_scroll_box.add_widget(self.search_post_hastags_input)
        #self.search_post_hastags.bind(on_text_validate = self.search_hastags_def)
        """

        self.search_btn_box = BoxLayout(size_hint_y = None, height = Window.size[1] / 8)
        self.content_in_scroll_box.add_widget(self.search_btn_box)

        self.search_btn = Button(on_release = self.search_def, border = (0, 0, 0, 0), text = "Search")
        self.search_btn_box.add_widget(self.search_btn)

        self.clear_search_btn = Button(size_hint_y = None, height = Window.size[1] / 12, on_release = self.clear_search_def, border = (0, 0, 0, 0), text = "Clear")
        self.content_in_scroll_box.add_widget(self.clear_search_btn)

        self.searched_box = BoxLayout(size_hint_y = None, height = 0, orientation = "vertical")
        self.content_in_scroll_box.add_widget(self.searched_box)


        self.content_in_scroll_box.height = Window.size[1] / 8 + Window.size[1] * 3 / 30 + Window.size[1] / 12
        # +(Window.size[1] - Window.size[0] / 5) * 0.9 / 12
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.current_posts = 2
    
    def new_posts_header_press(self, instance):
        if self.current_posts == 2:
            self.content_in_scroll_box.clear_widgets()

        self.display_header_box.clear_widgets()


        self.search_header_display_btn = Button (text = "Search")
        self.display_header_box.add_widget(self.search_header_display_btn)
        self.search_header_display_btn.bind(on_release = self.search_header_press)

        self.new_posts_header_display_label = Label(text = "New")
        self.display_header_box.add_widget(self.new_posts_header_display_label)


        self.content_in_scroll_box.height = len(self.all_displayed_new_posts_list) * (Window.size[1]  - Window.size[0] * ( 1 / 5 + 1 / 5.08))

        #new posts
        self.content_in_scroll_box.add_widget(self.new_posts_box)

        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.current_posts = 1

    def new_posts_refresh(self, instance):
        connection = self.connection
        self.all_newest_posts_info = connection.get_posts(sort_by = "time_posted", sort_order = "desc", num = 10)
        #include_background_color = str(1)

        #self.all_newest_posts_info = functions.order_posts_by_timestamp(self.all_new_posts_info)
        #print(self.all_newest_posts_info)
        #create a list with users searched. in next def we get info from list

        self.new_posts_box = BoxLayout(orientation = 'vertical')
        #self.content_in_scroll_box.add_widget(self.new_posts_box)

        self.all_displayed_new_posts_list = []

        my_liked_posts_id = access_my_info.get_liked_id()
        for t in range(len(self.all_newest_posts_info)):
            actual_maybe_like = 0
            try:
                for liked in my_liked_posts_id:
                    if liked == self.all_newest_posts_info[t]["id"]:
                        actual_maybe_like = 1
            except KeyError:
                pass
            print(self.all_newest_posts_info[t]["background_color"])
            self.post_btn = functions.make_post_btn(self, self.all_newest_posts_info[t]["user_id"], self.all_newest_posts_info[t]["content"], self.all_newest_posts_info[t]["time_posted"], actual_maybe_like, t, self.all_newest_posts_info[t]["background_color"])
            self.new_posts_box.add_widget(self.post_btn)
            self.all_displayed_new_posts_list.append([self.all_newest_posts_info[t]["id"], self.post_btn, actual_maybe_like, self.all_newest_posts_info[t]["user_id"]])
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))
        self.new_posts_header_press(0)
        self.search_header_press(0)

    #def display_newest_posts(self):
    #    self.content_in_scroll_box.add_widget(self.new_posts_box)

    def refresh_search_screen(self, instance):
        if self.current_posts == 2:
            self.new_posts_refresh(0)
        
        elif self.current_posts == 1 or self.current_posts == 0:
            self.search_header_press(0)
            self.new_posts_refresh(0)

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
        if self.current_posts == 1:
            num = self.all_displayed_new_posts_list[order_number][2]
            num = (num + 1) % 2
            instance.background_normal = functions.get_post_image(background, num)
            access_my_info.add_or_remove_liked_post(self.all_displayed_new_posts_list[order_number][0], num)
            self.all_displayed_new_posts_list[order_number][2] = num
        elif self.current_posts == 2:
            num = self.all_displayed_searched_posts_list[order_number][2]
            num = (num + 1) % 2
            instance.background_normal = functions.get_post_image(background, num)
            access_my_info.add_or_remove_liked_post(self.all_displayed_searched_posts_list[order_number][0], num)
            self.all_displayed_searched_posts_list[order_number][2] = num
        
    
    def name_press_user(self, instance):
        other_user_profile_screen = self.other_profile_screen
        other_user_profile_screen.refresh_profile_screen(instance.text)
        self.manager.transition = SlideTransition()
        self.manager.current = "other_profile"
        self.manager.transition.direction = "right"
    
    def clear_search_def(self, instance):
        self.new_posts_header_press(0)
        self.search_header_press(0)
        """self.search_btn_box.clear_widgets()
        self.search_btn = Button(text = "Search", on_release = self.search_def, border = (0, 0, 0, 0))
        self.search_btn_box.add_widget(self.search_btn)

        self.search_user_input.text = ""
        self.search_post_hastags_input.text = ""

        #self.sort_list = [0, 0]

        self.searched_box.clear_widgets()

        self.content_in_scroll_box.height = Window.size[1] / 8 + Window.size[1] / 6 + Window.size[1] * 3 / 15
        # + (Window.size[1] - Window.size[0] / 5) * 0.9 / 12
        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))"""

    def image_press(self, order_number, instance):
        pass

    def search_def(self, instance):
        conn = self.connection

        self.search_btn_box.clear_widgets()
        self.search_label_no_press = Label(text = "Search")
        self.search_btn_box.add_widget(self.search_label_no_press)
        #self.searched_box.clear_widgets()
        if self.search_input.text != "":
            if self.search_input.text[0] == "#":
                print(1)
                searched_posts = conn.get_posts(hashtag = functions.filter_chars(self.search_input.text), sort_by = "time_posted", sort_order = "desc")
                #exclude_flags = self.get_filter_flags()
                if searched_posts != ():
                    self.all_displayed_searched_posts_list = []
                    my_liked_posts_id = access_my_info.get_liked_id()
                    for t in range(len(searched_posts)):
                        actual_maybe_like = 0
                        try:
                            for liked in my_liked_posts_id:
                                if liked == searched_posts[t]["id"]:
                                    actual_maybe_like = 1
                        except KeyError:
                            pass
                        self.post_btn = functions.make_post_btn(self, searched_posts[t]["user_id"], searched_posts[t]["content"], searched_posts[t]["time_posted"], actual_maybe_like, t, searched_posts[t]["background_color"])
                        self.searched_box.add_widget(self.post_btn)
                        self.all_displayed_searched_posts_list.append([searched_posts[t]["id"], self.post_btn, actual_maybe_like, searched_posts[t]["user_id"]])
                    self.searched_box.height = (Window.size[1] - Window.size[0] * (1 / 5 + 1 / 5.08)) * len(searched_posts)
                    self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
                else:
                    self.not_found_label = Label(text = "Hashtag not found", size_hint_y = None, height = Window.size[1]/8)
                    self.searched_box.add_widget(self.not_found_label)
                    self.searched_box.height = Window.size[1]/8
                    self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
            
            elif self.search_input.text[0] == "@":
                print(2)
                searched_user = conn.get_user(functions.filter_chars(self.search_input.text[1::]))
                print(searched_user)
                if searched_user != {}:
                    self.searched_user_box = BoxLayout(orientation = 'horizontal', size_hint_y = None, height = Window.size[1]/6)
                    self.searched_box.add_widget(self.searched_user_box)

                    self.searched_user_image_grid = functions.build_image(self, searched_user["profile_picture"], -1, Window.size[1]/6)
                    self.searched_user_box.add_widget(self.searched_user_image_grid)

                    self.searched_user_name_btn = Button(text = searched_user["user_name"], on_release = partial(self.name_press_user))
                    self.searched_user_box.add_widget(self.searched_user_name_btn)

                    self.searched_box.height = Window.size[1]/6
                    self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
                else:
                    self.not_found_label = Label(text = "Nothing found", size_hint_y = None, height = Window.size[1]/8)
                    self.searched_box.add_widget(self.not_found_label)
                    self.searched_box.height = Window.size[1]/8
                    self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height
            else:
                self.not_found_label = Label(text = "Nothing found", size_hint_y = None, height = Window.size[1]/8)
                self.searched_box.add_widget(self.not_found_label)
                self.searched_box.height = Window.size[1]/8
                self.content_in_scroll_box.height = self.content_in_scroll_box.height + self.searched_box.height

        self.content_grid.bind(minimum_height=self.content_grid.setter('height'))

    


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
    
    def add_screens(self, home_screen, profile_screen, other_profile_screen, chat_screen, post_screen):
        self.home_screen = home_screen
        self.profile_screen = profile_screen
        self.other_profile_screen = other_profile_screen
        self.chat_screen = chat_screen
        self.post_screen = post_screen
