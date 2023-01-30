<img width="568" alt="IMG_6486" src="https://user-images.githubusercontent.com/74116694/215329396-cac41500-f045-4aa2-bc90-624abc3f65fc.png">


The app Keep It Green The app takes a user-input city name and parses an EPA dataset containing information pertaining to cleanup sites around the state of Florida. The program then plots a list of potential locations that the user could choose to volunteer at. The user can join a cleanup group at any of the locations listed. When a group has reached its capacity of eight members, registered users will be sent a notification containing the cleanup details. 

The project was built entirely using Python on the PyCharm IDE. We used the Pandas, GeoPy, Kivy, and KivyMD libraries. 

Demo Video: https://www.youtube.com/watch?v=LBrukxBMFlc

In order to run the code, make sure to import the following into main.py: 
  - import pandas as pd
  - from geopy.geocoders import Nominatim
  - from time import sleep
  - from kivy.uix.screenmanager import Screen, ScreenManager
  - from kivymd.app import MDApp
  - from kivy.lang.builder import Builder
  - from kivy.core.window import Window
  - from kivy.uix.widget import Widget
  
Also import the following into textsave.kv: 
  - #: import MapView kivy_garden.mapview.MapView
  - <MySwiper@MDSwiperItem>
  - <MagicButton@MagicBehavior+MDIconButton>

