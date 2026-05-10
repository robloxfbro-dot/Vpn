from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse
from jnius import autoclass
import re
import urllib.parse
from kivy.clock import Clock

class RoundButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#2A2A2A'))
            Ellipse(pos=self.pos, size=self.size)

class SwillWayVPN(App):
    def build(self):
        self.is_connected = False
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        root.add_widget(Label(text="SWILL WAY VPN", font_size='22sp', bold=True, size_hint_y=None, height=dp(50)))
        self.status = Label(text="DISCONNECTED", color=get_color_from_hex('#AAAAAA'), size_hint_y=None, height=dp(30))
        root.add_widget(self.status)
        self.btn_power = RoundButton(text="START", size_hint=(None, None), size=(dp(160), dp(160)), pos_hint={'center_x': 0.5})
        self.btn_power.bind(on_release=self.toggle_vpn)
        root.add_widget(self.btn_power)
        scroll = ScrollView(bar_width=dp(4))
        self.grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)
        btn_add = Button(text="ADD ALL SERVERS", size_hint_y=None, height=dp(60), background_color=get_color_from_hex('#333333'))
        btn_add.bind(on_release=self.add_from_clip)
        root.add_widget(btn_add)
        return root

    def toggle_vpn(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            VpnService = autoclass('android.net.VpnService')
            activity = PythonActivity.mActivity
            intent = VpnService.prepare(activity)
            if intent:
                activity.startActivityForResult(intent, 0)
            else:
                self.start_service_logic()
        except:
            self.start_service_logic()

    def start_service_logic(self):
        if not self.is_connected:
            self.status.text = "CONNECTING..."
            self.status.color = get_color_from_hex('#FFFF00')
            Clock.schedule_once(self.finish_connect, 2)
        else:
            self.is_connected = False
            self.status.text = "DISCONNECTED"
            self.status.color = get_color_from_hex('#AAAAAA')
            self.btn_power.text = "START"

    def finish_connect(self, dt):
        self.is_connected = True
        self.status.text = "ACTIVE"
        self.status.color = get_color_from_hex('#00FF00')
        self.btn_power.text = "STOP"

    def add_from_clip(self, instance):
        data = Clipboard.paste()
        links = re.findall(r'(vless|vmess|ss|trojan)://[^\s]+', data)
        if not links: return
        for link in links:
            name_part = re.search(r'#(.+)$', link)
            name = urllib.parse.unquote(name_part.group(1)) if name_part else "Server"
            card = Button(text=f"SERVER: {name}", size_hint_y=None, height=dp(60), background_color=get_color_from_hex('#222222'))
            self.grid.add_widget(card)

if __name__ == '__main__':
    SwillWayVPN().run()
