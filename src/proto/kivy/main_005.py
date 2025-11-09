# main.py
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle  # ← ADDED Rectangle
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp

from noaa_sdk import NOAA
import time

# --- CONFIG ---
ZIP_CODE = "39503"
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

<LineChart@Widget>:
    values: []
    max_value: 100
    min_value: 0
    line_color: [1, 0.3, 0.3, 1]
    label: ""
    canvas.before:
        Color:
            rgba: 0.12, 0.12, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size

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
            text: "Live Line Charts"
            font_style: "Subtitle1"

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: "16dp"
                padding: "8dp"

                LineChart:
                    id: temp_chart
                    label: "Temperature (degrees Celsius)"
                    line_color: [1, 0.3, 0.3, 1]
                    size_hint_y: None
                    height: "220dp"

                LineChart:
                    id: humid_chart
                    label: "Humidity (%)"
                    line_color: [0.3, 0.7, 1, 1]
                    size_hint_y: None
                    height: "220dp"

                LineChart:
                    id: press_chart
                    label: "Pressure (hPa)"
                    line_color: [0.5, 1, 0.3, 1]
                    size_hint_y: None
                    height: "220dp"
'''

class WeatherCard(MDCard):
    icon = StringProperty("")
    title = StringProperty("")
    value = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self._update_label)

    def _update_label(self, instance, value):
        for child in self.children:
            if isinstance(child, MDBoxLayout):
                for sub in child.children:
                    if hasattr(sub, 'id') and sub.id == 'value_label':
                        sub.text = value

class LineChart(Widget):
    values = ListProperty([])
    max_value = NumericProperty(100)
    min_value = NumericProperty(0)
    line_color = ListProperty([1, 0.3, 0.3, 1])
    label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw)
        self.bind(values=self.redraw, min_value=self.redraw, max_value=self.redraw)

    def redraw(self, *args):
        self.canvas.after.clear()
        with self.canvas:
            self.canvas.clear()

        if len(self.values) < 2:
            return

        w, h = self.size
        if w < 50 or h < 50:
            return

        pad = 40
        graph_w = w - 2 * pad
        graph_h = h - 2 * pad

        v_range = self.max_value - self.min_value
        if v_range <= 0:
            v_range = 1

        n = len(self.values)
        step = graph_w / (n - 1)

        # === DRAW LINE ===
        with self.canvas:
            Color(*self.line_color)
            line_pts = []
            for i, val in enumerate(self.values):
                x = pad + i * step
                y = pad + (val - self.min_value) / v_range * graph_h
                y = max(pad, min(pad + graph_h, y))
                line_pts.extend([x, y])
            Line(points=line_pts, width=3, joint='round', cap='round')

        # === DRAW POINTS ===
        with self.canvas:
            Color(1, 1, 1, 1)
            for i, val in enumerate(self.values):
                x = pad + i * step
                y = pad + (val - self.min_value) / v_range * graph_h
                Line(circle=[x, y, 6], width=2)

        # === LABEL ===
        with self.canvas.after:
            Color(1, 1, 1, 0.9)
            from kivy.core.text import Label as CoreLabel
            lbl = CoreLabel(text=self.label, font_size=15, bold=True)
            lbl.refresh()
            texture = lbl.texture
            if texture:
                Rectangle(texture=texture, pos=(pad, h - 35), size=texture.size)

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)

        self.screen.ids.title_label.text = f"NOAA Weather for ZIP {ZIP_CODE}"
        self.screen.ids.chart_label.text = f"Live Line Charts (last {HISTORY_SIZE} readings)"

        self.noaa = NOAA()
        self.history = {'temp': [], 'humid': [], 'press': []}

        Clock.schedule_once(lambda dt: self.start_updater(), 1)
        return self.screen

    def start_updater(self):
        Clock.schedule_interval(self.update_weather, UPDATE_INTERVAL)
        self.update_weather()

    def fetch_weather(self):
        try:
            observations = self.noaa.get_observations(ZIP_CODE, COUNTRY)
            for obs in observations:
                temp_f = obs.get('temperature', {}).get('value')
                if temp_f is not None:
                    temp_c = (float(temp_f) - 32) * 5 / 9
                    humidity = float(obs.get('relativeHumidity', {}).get('value', 0))
                    pressure_pa = obs.get('barometricPressure', {}).get('value', 0)
                    pressure_hpa = float(pressure_pa) / 100 if pressure_pa else 0
                    return temp_c, humidity, pressure_hpa
        except Exception as e:
            print(f"NOAA Error: {e}")
        return None

    def update_weather(self, *args):
        data = self.fetch_weather()
        if not data:
            print("No data")
            return

        temp, humid, press = data

        # Update cards
        self.screen.ids.temp_card.value = f"{temp:.1f} degrees Celsius"
        self.screen.ids.humid_card.value = f"{humid:.0f} %"
        self.screen.ids.press_card.value = f"{press:.0f} hPa"

        # Update history & redraw
        for key, val, chart_id, max_v in [
            ('temp', temp, 'temp_chart', 40),
            ('humid', humid, 'humid_chart', 100),
            ('press', press, 'press_chart', 1050)
        ]:
            self.history[key].append(val)
            if len(self.history[key]) > HISTORY_SIZE:
                self.history[key].pop(0)

            chart = self.screen.ids[chart_id]
            chart.min_value = min(self.history[key]) - 2 if self.history[key] else 0
            chart.max_value = max_v
            chart.values = self.history[key][:]
            chart.label = f"{key.capitalize()}: {val:.1f}"

        print(f"Line chart updated: T={temp:.1f}degrees Celsius | H={humid:.0f}% | P={press:.0f}hPa")

WeatherApp().run()


