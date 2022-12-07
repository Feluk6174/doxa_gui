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

import auth
connection = None

def set_connection(conn):
    connection = conn

def change_my_image(col_str):
    my_user_info = open_my_user_info()
    my_user_info["semi_basic_info"]["profile_picture"] = col_str
    file_my = open("my_info.json", "w")
    file_my.write(json.dumps(my_user_info))
    file_my.close()
    #cal enviar-ho

def change_my_description(description):
    my_user_info = open_my_user_info()
    my_user_info["semi_basic_info"]["description"] = description
    file_my = open("my_info.json", "w")
    file_my.write(json.dumps(my_user_info))
    file_my.close()
    #cal enviar-ho

def add_or_remove_following(id, foll):
    my_user_info = open_my_user_info()
    if foll == 0:
        my_user_info["semi_basic_info"]["user_following"].remove(id)
    elif foll == 1:
        my_user_info["semi_basic_info"]["user_following"].append(id)
    file_my = open("my_info.json", "w")
    file_my.write(json.dumps(my_user_info))
    file_my.close()

def add_or_remove_liked_post(post_id, like):
    my_user_info = open_my_user_info()
    if like == 0:
        my_user_info["semi_basic_info"]["liked_posts_id"].remove(post_id)
    elif like == 1:
        my_user_info["semi_basic_info"]["liked_posts_id"].append(post_id)
    file_my = open("my_info.json", "w")
    file_my.write(json.dumps(my_user_info))
    file_my.close()
    #cal enviar-ho

def open_my_user_info():
    try:
        my_user_info = json.loads(open("my_info.json", "r").read())
    except FileNotFoundError:
        my_user_info = ""
    return my_user_info


def get_user_name():
    my_user_info = open_my_user_info()
    username = my_user_info["basic_info"]["user_id"]
    return username

def get_password():
    my_user_info = open_my_user_info()
    password = my_user_info["basic_info"]["password"]
    return password

def get_profile_image():
    my_user_info = open_my_user_info()
    profileimage = my_user_info["semi_basic_info"]["profile_picture"]
    return profileimage

def get_priv_key():
    my_user_info = open_my_user_info()
    username = my_user_info["basic_info"]["user_id"]
    password = my_user_info["basic_info"]["password"]
    private_key, public_key = auth.get_keys(username + password)
    return private_key

def get_pub_key():
    my_user_info = open_my_user_info()
    username = my_user_info["basic_info"]["user_id"]
    password = my_user_info["basic_info"]["password"]
    private_key, public_key = auth.get_keys(username + password)
    return public_key

def get_description():
    my_user_info = open_my_user_info()
    user_description = my_user_info["semi_basic_info"]["description"]
    return user_description

def get_following():
    my_user_info = open_my_user_info()
    user_following = my_user_info["semi_basic_info"]["user_following"]
    return user_following

def get_liked():
    user_liked_id = get_liked_id
    user_liked = []
    for post in user_liked_id:
        actual_liked = connection.get_post(post)
        user_liked.append(actual_liked)
    return user_liked

def get_liked_id():
    my_user_info = open_my_user_info()
    user_liked_id = my_user_info["semi_basic_info"]["liked_posts_id"]
    return user_liked_id