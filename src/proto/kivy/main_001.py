# main.py
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp

from noaa_sdk import NOAA
import time

# --- CONFIG ---
ZIP_CODE = "10001"
COUNTRY = "US"
UPDATE_INTERVAL = 60
HISTORY_SIZE = 10

KV = '''
<WeatherCard@MDCard>:
    icon: ""
    title: ""
    value: ""
    orientation: "horizontal"
    size_hint_y: None
    height: "80dp"
    padding: "16dp"
    elevation: 2
    radius: [12]

    MDIcon:
        icon: root.icon
        font_size: "32sp"
        theme_text_color: "Primary"

    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: root.title
            font_style: "Subtitle1"
        MDLabel:
            id: value_label
            text: root.value
            font_style: "H6"
            theme_text_color: "Secondary"

<Chart@Widget>:
    values: []
    max_value: 100
    min_value: 0
    color: [0, 0.7, 1, 1]
    label: ""
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    canvas:
        Color:
            rgba: root.color
        Line:
            points: root.line_points
            width: 2
        Color:
            rgba: root.color[0], root.color[1], root.color[2], 0.4
        Line:
            points: root.bar_points
            width: dp(20)

Screen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "16dp"

        MDLabel:
            id: title_label
            text: "NOAA Weather"
            font_style: "H4"
            theme_text_color: "Primary"

        MDGridLayout:
            cols: 1
            spacing: "12dp"
            size_hint_y: None
            height: self.minimum_height

            WeatherCard:
                icon: "temperature-fahrenheit"
                title: "Temperature"
                value: "-- degrees Celsius"
                id: temp_card

            WeatherCard:
                icon: "water-percent"
                title: "Humidity"
                value: "-- %"
                id: humid_card

            WeatherCard:
                icon: "gauge"
                title: "Pressure"
                value: "-- hPa"
                id: press_card

        MDLabel:
            id: chart_label
            text: "Live Charts"
            font_style: "Subtitle1"

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: "16dp"
                padding: "8dp"

                Chart:
                    id: temp_chart
                    label: "Temperature (degrees Celsius)"
                    color: [1, 0.3, 0.3, 1]
                    size_hint_y: None
                    height: "200dp"

                Chart:
                    id: humid_chart
                    label: "Humidity (%)"
                    color: [0.3, 0.7, 1, 1]
                    size_hint_y: None
                    height: "200dp"

                Chart:
                    id: press_chart
                    label: "Pressure (hPa)"
                    color: [0.5, 1, 0.3, 1]
                    size_hint_y: None
                    height: "200dp"
'''

class WeatherCard(MDCard):
    icon = StringProperty("")
    title = StringProperty("")
    value = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.update_value_label)

    def update_value_label(self, instance, value):
        for child in self.children:
            if isinstance(child, MDBoxLayout):
                for subchild in child.children:
                    if hasattr(subchild, 'id') and subchild.id == 'value_label':
                        subchild.text = value
                        break

class Chart(Widget):
    values = ListProperty([])
    max_value = NumericProperty(100)
    min_value = NumericProperty(0)
    color = ListProperty([0, 0.7, 1, 1])
    label = StringProperty("")
    line_points = ListProperty([])
    bar_points = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(values=self.update_graphics)
        self.bind(min_value=self.update_graphics)
        self.bind(max_value=self.update_graphics)

    def update_graphics(self, *args):
        self.canvas.clear()
        self.canvas.after.clear()

        if len(self.values) == 0:
            return

        w, h = self.size
        if w <= 0 or h <= 0:
            return

        pad = 40
        graph_h = h - pad * 2
        graph_w = w - pad * 2

        v_range = self.max_value - self.min_value
        if v_range <= 0:
            v_range = 1

        n = len(self.values)
        step = graph_w / max(n - 1, 1)

        line_pts = []
        bar_pts = []

        for i, val in enumerate(self.values):
            x = pad + i * step
            y = pad + (val - self.min_value) / v_range * graph_h
            y = max(pad, min(pad + graph_h, y))

            line_pts.extend([x, y])

            bar_h = (val - self.min_value) / v_range * graph_h
            bar_h = max(0, min(graph_h, bar_h))
            bar_x = x - 10
            bar_pts.extend([
                bar_x, pad,
                bar_x, pad + bar_h,
                bar_x + 20, pad + bar_h,
                bar_x + 20, pad
            ])

        with self.canvas:
            Color(*self.color)
            Line(points=line_pts, width=2)
            Color(self.color[0], self.color[1], self.color[2], 0.4)
            if bar_pts:
                Line(points=bar_pts, close=True)

        with self.canvas.after:
            Color(1, 1, 1, 0.8)
            from kivy.core.text import Label as CoreLabel
            lbl = CoreLabel(text=self.label, font_size=14)
            lbl.refresh()
            texture = lbl.texture
            if texture:
                Rectangle(texture=texture, pos=(pad, h - 30), size=texture.size)

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)

        self.screen.ids.title_label.text = f"NOAA Weather for ZIP {ZIP_CODE}"
        self.screen.ids.chart_label.text = f"Live Charts (last {HISTORY_SIZE} readings)"

        self.noaa = NOAA()
        self.history = {'temp': [], 'humid': [], 'press': []}

        Clock.schedule_once(lambda dt: self.start_updater(), 1)
        return self.screen

    def start_updater(self):
        Clock.schedule_interval(self.update_weather, UPDATE_INTERVAL)
        self.update_weather()

    def fetch_weather(self):
        try:
            # get_observations returns a GENERATOR
            observations = self.noaa.get_observations(ZIP_CODE, COUNTRY)
            for obs in observations:  # Take FIRST valid observation
                temp_f = obs.get('temperature', {}).get('value')
                humidity = obs.get('relativeHumidity', {}).get('value')
                pressure_pa = obs.get('barometricPressure', {}).get('value')

                if temp_f is not None:
                    temp_c = (float(temp_f) - 32) * 5 / 9
                    humidity = float(humidity) if humidity is not None else 0
                    pressure_hpa = float(pressure_pa) / 100 if pressure_pa is not None else 0
                    return temp_c, humidity, pressure_hpa
        except Exception as e:
            print(f"NOAA Error: {e}")
        return None

    def update_weather(self, *args):
        data = self.fetch_weather()
        if not data:
            print("No valid NOAA data received")
            return

        temp, humid, press = data

        # Update cards
        self.screen.ids.temp_card.value = f"{temp:.1f} degrees Celsius"
        self.screen.ids.humid_card.value = f"{humid:.0f} %"
        self.screen.ids.press_card.value = f"{press:.0f} hPa"

        # Update history and charts
        for key, val, chart_id, max_v in [
            ('temp', temp, 'temp_chart', 40),
            ('humid', humid, 'humid_chart', 100),
            ('press', press, 'press_chart', 1050)
        ]:
            self.history[key].append(val)
            if len(self.history[key]) > HISTORY_SIZE:
                self.history[key].pop(0)

            chart = self.screen.ids[chart_id]
            chart.values = self.history[key][:]
            chart.min_value = min(self.history[key]) - 2 if self.history[key] else 0
            chart.max_value = max_v
            chart.label = f"{key.capitalize()}: {val:.1f}"

        print(f"Updated: T={temp:.1f}degrees Celsius, H={humid:.0f}%, P={press:.0f}hPa")

WeatherApp().run()


