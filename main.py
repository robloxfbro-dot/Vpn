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

class SwillWayVPN(App):
    def build(self):
        self.is_connected = False
        self.server_widgets = []
        
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        top_bar = BoxLayout(size_hint_y=None, height=dp(50))
        top_bar.add_widget(Label(text="SWILL WAY VPN", bold=True, font_size='22sp'))
        top_bar.add_widget(Label(text="📑", font_size='25sp', size_hint_x=0.2))
        root.add_widget(top_bar)

        self.status = Label(text="DISCONNECTED", color=(1, 0, 0, 1), size_hint_y=None, height=dp(30), bold=True)
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
        btn_add = Button(text="ADD SERVER", background_color=get_color_from_hex('#333333'), bold=True)
        btn_add.bind(on_release=self.add_server)
        btn_ping = Button(text="⚡ PING", background_color=get_color_from_hex('#333333'), bold=True)
        btn_ping.bind(on_release=self.mass_ping)
        
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
                self.is_connected = not self.is_connected
                if self.is_connected:
                    self.status.text = "CONNECTED"
                    self.status.color = (0, 1, 0, 1)
                    self.btn_power.text = "STOP"
                    self.btn_power.color = (1, 0, 0, 1)
                else:
                    self.status.text = "DISCONNECTED"
                    self.status.color = (1, 0, 0, 1)
                    self.btn_power.text = "START"
                    self.btn_power.color = (0, 1, 0, 1)
        except:
            self.status.text = "PLATFORM ERROR"

    def add_server(self, instance):
        data = Clipboard.paste()
        if "://" in data:
            name = data.split("#")[-1] if "#" in data else f"Server {len(self.server_widgets)+1}"
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), padding=dp(5))
            card.add_widget(Label(text="🌐", size_hint_x=0.2))
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=name, bold=True, halign='left', text_size=(dp(200), None)))
            ping_lab = Label(text="Ping: --", font_size='12sp', halign='left', text_size=(dp(200), None))
            info.add_widget(ping_lab)
            card.add_widget(info)
            card.ping_lab = ping_lab
            self.grid.add_widget(card)
            self.server_widgets.append(card)

    def mass_ping(self, instance):
        import socket
        import time
        for card in self.server_widgets:
            try:
                start = time.time()
                socket.create_connection(("8.8.8.8", 53), timeout=1)
                p = int((time.time() - start) * 1000)
                card.ping_lab.text = f"Ping: {p}ms"
            except:
                card.ping_lab.text = "Offline"

if __name__ == '__main__':
    SwillWayVPN().run()
