import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivy.lang import Builder
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout
# from kivy.app import Builder
# from kivy.uix.button import Button
# from kivymd.uix.button import MDRectangleFlatButton
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.icon_definitions import md_icons
from kivy_garden.mapview import MapView, MapMarker

#business name, address, zip code, website

Window.size = (350, 600)


class Welcome(Screen):
    pass

class Location(Screen):
    pass

class ContactInfo(Screen):
    pass

class Complete(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class textinput(Widget):
    pass


precise_geo = {}
display_dict = {}
global_city = ""

data = pd.read_csv('venv/DEP_Cleanup_Sites.csv')
raw_data = pd.DataFrame(data)
count = 0
ppl = 0

class MyApp(MDApp):
    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)

    def getCity(self):
        user_input = self.root.get_screen("welcome").ids.city_input.text
        print(user_input)
        user_input = user_input.upper()[0] + user_input.lower()[1:]
        self.root.get_screen("locations").ids.toolbar.title = "Clean up Sites in " + user_input

        potential_locs = raw_data.loc[(raw_data['CITY'] == user_input.upper())]
        potential_locs = potential_locs.drop_duplicates(subset=['ADDRESS1'], keep=False)
        global_city = user_input

        # reading csv file
        print("potential locs: " , potential_locs)
        address_list = potential_locs['ADDRESS1'].values.tolist()

        add_coord = {}
        print("potential cleanup sites: ")
        for i in address_list:
            try:
                add_coord[i] = (potential_locs.loc[potential_locs['ADDRESS1'] == i, 'LATITUDE_DD'].values[0],
                                potential_locs.loc[potential_locs['ADDRESS1'] == i, 'LONGITUDE_DD'].values[0])
                print(i, ":", add_coord[i])
            except:
                continue

        # presicse cords
        for i in address_list:
            if len(precise_geo) > 10:
                break
            geolocator = Nominatim(user_agent='my_application')
            location = geolocator.geocode(i, timeout=None)
            try:
                print(location.address)
                coordinates = (location.latitude, location.longitude)
            except:
                continue
            reverse = geolocator.reverse(coordinates)
            try:
                city_name = reverse.raw['address']['city']
                print(city_name)
            except:
                continue

            if city_name.upper() == user_input.upper():
                try:
                    business_name = potential_locs.loc[potential_locs['ADDRESS1'] == i, 'BUSINESS_NAME'].values[0]
                    biz_name = potential_locs.loc[potential_locs['ADDRESS1'] == i, 'BUSINESS_NAME'].values[0]
                    website = potential_locs.loc[potential_locs['ADDRESS1'] == i, 'DOCUMENTS'].values[0]
                    zip_code = int(potential_locs.loc[potential_locs['ADDRESS1'] == i, 'ZIP5'].values[0])
                    precise_geo[business_name] = tuple((coordinates, i, website, zip_code))
                    print("Business name: ", business_name, "Address: ", i, "Coordinates: ", precise_geo[i])

                except:
                    sleep(1)
                    try:
                        business_name = potential_locs.loc[potential_locs['ADDRESS1'] == i, 'BUSINESS_NAME'].values[0]
                        website = potential_locs.loc[potential_locs['ADDRESS1'] == i, 'DOCUMENTS'].values[0]
                        zip_code = int(potential_locs.loc[potential_locs['ADDRESS1'] == i, 'ZIP5'].values[0])
                        precise_geo[business_name] = tuple((coordinates, i, website, zip_code))
                        print("Business name: ", business_name, "Address: ", i, "Coordinates: ", precise_geo[i])

                    except:
                        continue
        return precise_geo

    def getPotential(self):
        print("global city: ", global_city)
        print(raw_data)
        potential_locs = raw_data.loc[(raw_data['CITY'] == global_city.upper())]
        potential_locs = potential_locs.drop_duplicates(subset=['ADDRESS1'], keep=False)
        return potential_locs


    def addPerson(self):
        ppl = self.root.get_screen("locations").ids.person.text
        ppl = int(ppl[0])
        ppl += 1
        self.root.get_screen("locations").ids.person.text = str(ppl) + " / 8"



    def getMap(self):
        precise_geo = self.getCity()
        print("Length: ", len(precise_geo))
        keys_list = list(precise_geo.keys())
        if len(keys_list) == 0:
            print("City not in dataset. Choose another location")
            exit()
        my_tuple = precise_geo[keys_list[0]]
        lat_val, lon_val = my_tuple[0]
        lat_val = float(lat_val)
        lon_val = float(lon_val)
        print(lat_val, lon_val)

        self.root.get_screen("locations").ids.map.lat = lat_val
        self.root.get_screen("locations").ids.map.lon = lon_val

        ten_keys = keys_list[0:9]
        # self.outputDict(ten_keys)


        counter = 0

        for i in keys_list:
            if counter > 9:
                break
            print("counter: " + str(counter) )
            a_tuple = precise_geo[i]
            lat_val, lon_val = a_tuple[0]
            # print(precise_geo[i])
            if counter == 0:
                self.root.get_screen("locations").ids.marker0.lat = lat_val
                self.root.get_screen("locations").ids.marker0.lon = lon_val
                # # business name
                add = str(i)
                self.root.get_screen("locations").ids.swiper1.business += add
                # addys
                self.root.get_screen("locations").ids.swiper1.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                #website
                self.root.get_screen("locations").ids.swiper1.info += a_tuple[2]
                print(lat_val, lon_val)
            if counter == 1:
                self.root.get_screen("locations").ids.marker1.lat = lat_val
                self.root.get_screen("locations").ids.marker1.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper2.business += add
                # addys
                self.root.get_screen("locations").ids.swiper2.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper2.info += a_tuple[2]

            if counter == 2:
                self.root.get_screen("locations").ids.marker2.lat = lat_val
                self.root.get_screen("locations").ids.marker2.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper3.business += add
                # addys
                self.root.get_screen("locations").ids.swiper3.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper3.info += a_tuple[2]

            if counter == 3:
                self.root.get_screen("locations").ids.marker3.lat = lat_val
                self.root.get_screen("locations").ids.marker3.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper4.business += add
                # addys
                self.root.get_screen("locations").ids.swiper4.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper4.info += a_tuple[2]

            if counter == 4:
                self.root.get_screen("locations").ids.marker4.lat = lat_val
                self.root.get_screen("locations").ids.marker4.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper5.business += add
                # addys
                self.root.get_screen("locations").ids.swiper5.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper5.info += a_tuple[2]

            if counter == 5:
                self.root.get_screen("locations").ids.marker5.lat = lat_val
                self.root.get_screen("locations").ids.marker5.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper6.business += add
                # addys
                self.root.get_screen("locations").ids.swiper6.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper6.info += a_tuple[2]

            if counter == 6:
                self.root.get_screen("locations").ids.marker6.lat = lat_val
                self.root.get_screen("locations").ids.marker6.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper7.business += add
                # addys
                self.root.get_screen("locations").ids.swiper7.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper7.info += a_tuple[2]

            if counter == 7:
                self.root.get_screen("locations").ids.marker7.lat = lat_val
                self.root.get_screen("locations").ids.marker7.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper8.business += add
                # addys
                self.root.get_screen("locations").ids.swiper8.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper8.info += a_tuple[2]

            if counter == 8:
                self.root.get_screen("locations").ids.marker8.lat = lat_val
                self.root.get_screen("locations").ids.marker8.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper9.business += add
                # addys
                self.root.get_screen("locations").ids.swiper9.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper9.info += a_tuple[2]

            if counter == 9:
                self.root.get_screen("locations").ids.marker9.lat = lat_val
                self.root.get_screen("locations").ids.marker9.lon = lon_val
                print(lat_val, lon_val)
                add = str(i)
                self.root.get_screen("locations").ids.swiper10.business += add
                # addys
                self.root.get_screen("locations").ids.swiper10.address += str(a_tuple[1] + ", " + str(a_tuple[3]))
                # website
                self.root.get_screen("locations").ids.swiper10.info += a_tuple[2]
                self.root.get_screen("locations").ids.map.on_zoom(self, self.root.get_screen("locations").ids.map._zoom)
                self.root.get_screen("locations").ids.map.center_on(lat_val, lon_val)

            counter += 1

    def exitCode(self):
        exit()

    def build(self):
        self.title = 'Keep it Green'
        return Builder.load_file('textsave.kv')
    def reset(self):
        self.root.get_screen("locations").ids.swiper1.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper1.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper1.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper2.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper2.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper2.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper3.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper3.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper3.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper4.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper4.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper4.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper5.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper5.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper5.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper6.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper6.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper6.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper7.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper7.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper7.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper8.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper8.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper8.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper9.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper9.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper9.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("locations").ids.swiper10.business = "[color=#000000][b]"
        self.root.get_screen("locations").ids.swiper10.address = "\n[size=26][color=#bebebe]  "
        self.root.get_screen("locations").ids.swiper10.info = "[size=28]\n[color=#3f3f3f][i]"
        self.root.get_screen("welcome").ids.city_input.text = ""

        precise_geo.clear()
        display_dict.clear()
        global_city = ""
        count = 0
        ppl = 0




MyApp().run()