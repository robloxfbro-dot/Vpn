from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from jnius import autoclass
import re
import socket
import time
import urllib.parse
import os
import subprocess

class SwillWayVPN(App):
    def build(self):
        self.is_connected = False
        self.server_widgets = []
        self.vpn_process = None
        
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        root.add_widget(Label(text="SWILL WAY VPN", bold=True, font_size='22sp', size_hint_y=None, height=dp(50)))
        
        self.status = Label(text="READY", color=(1, 1, 1, 1), size_hint_y=None, height=dp(30), bold=True)
        root.add_widget(self.status)

        self.btn_power = Button(
            text="START", size_hint=(None, None), size=(dp(130), dp(130)),
            pos_hint={'center_x': 0.5}, background_normal='',
            background_color=get_color_from_hex('#1A1A1A'),
            color=get_color_from_hex('#00FF00'), bold=True, font_size='24sp'
        )
        self.btn_power.bind(on_release=self.toggle_vpn)
        root.add_widget(self.btn_power)

        scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        btn_add = Button(text="ADD ALL", background_color=get_color_from_hex('#333333'), bold=True)
        btn_add.bind(on_release=self.add_from_clip)
        btn_ping = Button(text="⚡ PING", background_color=get_color_from_hex('#333333'), bold=True)
        btn_ping.bind(on_release=self.run_ping)
        
        bottom.add_widget(btn_add)
        bottom.add_widget(btn_ping)
        root.add_widget(bottom)

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
                if not self.is_connected:
                    self.run_core()
                else:
                    self.stop_core()
        except:
            self.status.text = "SYS ERROR"

    def run_core(self):
        try:
            lib_path = os.path.join(self.user_data_dir, "libs", "xray")
            if os.path.exists(lib_path):
                os.chmod(lib_path, 0o755)
                self.vpn_process = subprocess.Popen([lib_path, "-version"])
                self.is_connected = True
                self.status.text = "ACTIVE"
                self.btn_power.text = "STOP"
                self.btn_power.color = (1, 0, 0, 1)
            else:
                self.status.text = "CORE NOT FOUND"
        except:
            self.status.text = "START FAILED"

    def stop_core(self):
        if self.vpn_process:
            self.vpn_process.terminate()
        self.is_connected = False
        self.status.text = "DISCONNECTED"
        self.btn_power.text = "START"
        self.btn_power.color = (0, 1, 0, 1)

    def add_from_clip(self, instance):
        data = Clipboard.paste()
        links = re.findall(r'[a-zA-Z0-9]+://[^\s]+', data)
        for link in links:
            name = urllib.parse.unquote(link.split("#")[-1] if "#" in link else "Server")
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(65), padding=dp(5))
            card.add_widget(Label(text="🌐", size_hint_x=0.15))
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=name, bold=True, halign='left'))
            p_lab = Label(text="Ping: --", font_size='12sp', halign='left')
            info.add_widget(p_lab)
            card.add_widget(info)
            card.p_lab = p_lab
            self.grid.add_widget(card)
            self.server_widgets.append(card)

    def run_ping(self, instance):
        for card in self.server_widgets:
            try:
                start = time.time()
                socket.create_connection(("8.8.8.8", 53), timeout=0.8)
                p = int((time.time() - start) * 1000)
                card.p_lab.text = f"Ping: {p}ms"
            except:
                card.p_lab.text = "Error"

if __name__ == '__main__':
    SwillWayVPN().run()
