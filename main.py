from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
import socket
import time
import re

class SwillWayApp(App):
    def build(self):
        self.is_connected = False
        self.server_widgets = []

        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), canvas_before=None)
        
        # Заголовок
        root.add_widget(Label(text="SWILL WAY VPN", bold=True, font_size='22sp', size_hint_y=None, height=dp(50)))

        # Кнопка СТАРТ (Центральная)
        self.btn_power = Button(
            text="START", size_hint=(None, None), size=(dp(130), dp(130)),
            pos_hint={'center_x': 0.5}, background_normal='',
            background_color=get_color_from_hex('#222222'),
            color=get_color_from_hex('#00FF00'), bold=True, font_size='24sp'
        )
        self.btn_power.bind(on_release=self.toggle_vpn)
        root.add_widget(self.btn_power)

        # Контейнер для списка серверов
        scroll = ScrollView(size_hint=(1, 1), bar_width=dp(4))
        self.server_list = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.server_list.bind(minimum_height=self.server_list.setter('height'))
        scroll.add_widget(self.server_list)
        root.add_widget(scroll)

        # Нижнее меню
        bottom_menu = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(10))
        
        btn_clip = Button(text="ADD SERVER", background_color=get_color_from_hex('#333333'), bold=True)
        btn_clip.bind(on_release=self.add_from_clip)
        
        btn_ping = Button(text="⚡ PING ALL", background_color=get_color_from_hex('#333333'), bold=True)
        btn_ping.bind(on_release=self.mass_ping)

        bottom_menu.add_widget(btn_clip)
        bottom_menu.add_widget(btn_ping)
        root.add_widget(bottom_menu)

        return root

    def add_from_clip(self, instance):
        raw_data = Clipboard.paste()
        if "://" in raw_data:
            # Парсим имя сервера из заметки после #
            name = "New Server"
            if "#" in raw_data:
                name = raw_data.split("#")[-1]
            
            # Создаем "Карточку" сервера (BoxLayout вместо одной кнопки)
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), padding=dp(10))
            
            # Иконка (просто текст для начала)
            card.add_widget(Label(text="🌐", size_hint_x=0.2, font_size='20sp'))
            
            # Инфо о сервере
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=name, bold=True, halign='left', text_size=(dp(200), None)))
            
            ping_label = Label(text="Ping: --", color=(0.7, 0.7, 0.7, 1), halign='left', text_size=(dp(200), None))
            info.add_widget(ping_label)
            card.add_widget(info)
            
            # Кнопка выбора этого сервера
            select_btn = Button(text="USE", size_hint_x=0.25, background_color=get_color_from_hex('#444444'))
            card.add_widget(select_btn)

            # Сохраняем ссылки для пинга
            card.ping_label = ping_label
            card.raw_link = raw_data
            
            self.server_list.add_widget(card)
            self.server_widgets.append(card)
        else:
            print("No valid link in clipboard")

    def toggle_vpn(self, instance):
        self.is_connected = not self.is_connected
        self.btn_power.text = "STOP" if self.is_connected else "START"
        self.btn_power.color = (1, 0, 0, 1) if self.is_connected else (0, 1, 0, 1)

    def mass_ping(self, instance):
        for card in self.server_widgets:
            try:
                start = time.time()
                socket.create_connection(("8.8.8.8", 53), timeout=1)
                p = int((time.time() - start) * 1000)
                card.ping_label.text = f"Ping: {p}ms"
                card.ping_label.color = (0, 1, 0, 1) if p < 150 else (1, 1, 0, 1)
            except:
                card.ping_label.text = "Offline"
                card.ping_label.color = (1, 0, 0, 1)

if __name__ == '__main__':
    SwillWayApp().run()
