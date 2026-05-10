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
import socket
import time
import urllib.parse
import os
import subprocess

class RoundButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#1A1A1A'))
            Ellipse(pos=self.pos, size=self.size)

class SwillWayVPN(App):
    def build(self):
        self.is_connected = False
        self.server_widgets = []
        
        root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        # Заголовок
        root.add_widget(Label(
            text="SWILL WAY VPN", 
            bold=True, 
            font_size='24sp', 
            size_hint_y=None, 
            height=dp(60),
            color=get_color_from_hex('#FFFFFF')
        ))
        
        self.status = Label(
            text="STATUS: READY", 
            size_hint_y=None, 
            height=dp(30), 
            bold=True,
            color=get_color_from_hex('#AAAAAA')
        )
        root.add_widget(self.status)

        # Круглая кнопка
        self.btn_power = RoundButton(
            text="START", 
            size_hint=(None, None), 
            size=(dp(160), dp(160)),
            pos_hint={'center_x': 0.5},
            color=get_color_from_hex('#00FF00'), 
            bold=True, 
            font_size='26sp'
        )
        self.btn_power.bind(on_release=self.toggle_vpn)
        root.add_widget(self.btn_power)

        # Список серверов
        scroll = ScrollView(size_hint=(1, 1), bar_width=dp(4))
        self.grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        # Нижние кнопки
        bottom = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(12))
        
        btn_add = Button(text="ADD ALL", background_color=get_color_from_hex('#222222'), bold=True)
        btn_add.bind(on_release=self.add_from_clip)
        
        btn_ping = Button(text="CHECK PING", background_color=get_color_from_hex('#222222'), bold=True)
        btn_ping.bind(on_release=self.run_ping)
        
        bottom.add_widget(btn_add)
        bottom.add_widget(btn_ping)
        root.add_widget(bottom)

        return root

    def toggle_vpn(self, instance):
        try:
            # Вызов системного окна Android для разрешения VPN (Ключик)
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            VpnService = autoclass('android.net.VpnService')
            activity = PythonActivity.mActivity
            intent = VpnService.prepare(activity)
            
            if intent:
                activity.startActivityForResult(intent, 0)
            else:
                if not self.is_connected:
                    self.start_connection()
                else:
                    self.stop_connection()
        except Exception as e:
            self.status.text = "ANDROID ERROR"

    def start_connection(self):
        # Тут должна быть команда запуска бинарника xray
        self.is_connected = True
        self.status.text = "STATUS: ACTIVE"
        self.status.color = get_color_from_hex('#00FF00')
        self.btn_power.text = "STOP"
        self.btn_power.color = get_color_from_hex('#FF0000')

    def stop_connection(self):
        self.is_connected = False
        self.status.text = "STATUS: DISCONNECTED"
        self.status.color = get_color_from_hex('#AAAAAA')
        self.btn_power.text = "START"
        self.btn_power.color = get_color_from_hex('#00FF00')

    def add_from_clip(self, instance):
        data = Clipboard.paste()
        # Регулярка для поиска всех типов ссылок (vless, vmess, ss)
        links = re.findall(r'(vless|vmess|ss|trojan)://[^\s]+', data)
        
        if not links:
            self.status.text = "NO LINKS FOUND"
            return

        for link in links:
            # Очистка имени от иероглифов и декодирование
            raw_name = link.split("#")[-1] if "#" in link else "Unknown Server"
            name = urllib.parse.unquote(raw_name).encode('latin1').decode('utf-8', 'ignore')
            
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), padding=dp(10))
            with card.canvas.before:
                Color(rgba=get_color_from_hex('#222222'))
                from kivy.graphics import RoundedRectangle
                self.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10),])
            
            card.add_widget(Label(text="SERVR", size_hint_x=0.2, bold=True))
            
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=name[:20], bold=True, halign='left', font_size='16sp'))
            p_lab = Label(text="Ping: ---", font_size='12sp', color=get_color_from_hex('#00FF00'))
            info.add_widget(p_lab)
            
            card.add_widget(info)
            card.p_lab = p_lab
            self.grid.add_widget(card)
            self.server_widgets.append(card)

    def run_ping(self, instance):
        for card in self.server_widgets:
            try:
                start = time.time()
                socket.create_connection(("8.8.8.8", 53), timeout=1.0)
                ms = int((time.time() - start) * 1000)
                card.p_lab.text = f"Ping: {ms}ms"
            except:
                card.p_lab.text = "Offline"

if __name__ == '__main__':
    SwillWayVPN().run()
