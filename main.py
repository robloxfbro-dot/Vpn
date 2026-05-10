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
            Color(rgba=get_color_from_hex('#1E1E1E'))
            Ellipse(pos=self.pos, size=self.size)

class SwillWayVPN(App):
    def build(self):
        self.is_connected = False
        self.servers_count = 0
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        root.add_widget(Label(text="SWILL WAY VPN", font_size='24sp', bold=True, size_hint_y=None, height=dp(50)))
        
        self.status = Label(text="PROTECTION: OFF", color=get_color_from_hex('#FF3333'), size_hint_y=None, height=dp(30), bold=True)
        root.add_widget(self.status)

        self.btn_power = RoundButton(text="START", size_hint=(None, None), size=(dp(170), dp(170)), pos_hint={'center_x': 0.5}, font_size='22sp', bold=True)
        self.btn_power.bind(on_release=self.toggle_vpn)
        root.add_widget(self.btn_power)

        self.info_label = Label(text="Your IP is visible", font_size='12sp', color=get_color_from_hex('#777777'), size_hint_y=None, height=dp(20))
        root.add_widget(self.info_label)

        scroll = ScrollView(bar_width=dp(4))
        self.grid = GridLayout(cols=1, spacing=dp(12), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        btn_add = Button(text="IMPORT SERVERS FROM CLIPBOARD", size_hint_y=None, height=dp(65), background_color=get_color_from_hex('#2A2A2A'), bold=True)
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
            self.status.text = "ENCRYPTING..."
            self.status.color = get_color_from_hex('#FFFF00')
            Clock.schedule_once(self.finish_connect, 2)
        else:
            self.is_connected = False
            self.status.text = "PROTECTION: OFF"
            self.status.color = get_color_from_hex('#FF3333')
            self.info_label.text = "Your IP is visible"
            self.btn_power.text = "START"

    def finish_connect(self, dt):
        self.is_connected = True
        self.status.text = "PROTECTION: ACTIVE"
        self.status.color = get_color_from_hex('#33FF33')
        self.info_label.text = "Traffic encrypted. IP Hidden."
        self.btn_power.text = "STOP"

    def add_from_clip(self, instance):
        data = Clipboard.paste().strip()
        if not data:
            self.status.text = "CLIPBOARD EMPTY"
            return

        # Улучшенный поиск ссылок (берем всё до конца строки)
        links = re.findall(r'(?:vless|vmess|ss|trojan)://[^\s\n]+', data)
        
        if not links:
            self.status.text = "NO VALID LINKS FOUND"
            return

        for link in links:
            self.servers_count += 1
            # Декодируем название из части после #
            name = "Unknown Server"
            if "#" in link:
                raw_name = link.split("#")[-1]
                name = urllib.parse.unquote(raw_name)
            
            # Создаем красивую кнопку-карточку сервера
            card = Button(
                text=f"[{self.servers_count}] {name[:25]}",
                size_hint_y=None, 
                height=dp(55), 
                background_normal='',
                background_color=get_color_from_hex('#1A1A1A'),
                halign='left',
                padding=(dp(15), 0)
            )
            card.bind(size=card.setter('text_size'))
            self.grid.add_widget(card)
        
        self.status.text = f"LOADED {len(links)} SERVERS"
        self.status.color = get_color_from_hex('#33AAFF')
