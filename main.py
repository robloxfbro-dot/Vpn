from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
import socket
import time

class SwillWayApp(App):
    def build(self):
        self.servers = []
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # Заголовок в стиле Swill Way
        layout.add_widget(Label(
            text="SWILL WAY VPN [V1.0]", 
            font_size='25sp', 
            bold=True,
            color=get_color_from_hex('#FF0000') # Красный агрессивный
        ))

        self.status = Label(text="СИСТЕМА ГОТОВА", font_size='18sp')
        layout.add_widget(self.status)

        # Кнопка добавления серверов
        btn_clip = Button(
            text="ДОБАВИТЬ ИЗ БУФЕРА", 
            bold=True,
            background_color=get_color_from_hex('#444444')
        )
        btn_clip.bind(on_release=self.add_from_clip)
        layout.add_widget(btn_clip)

        # Кнопка Пинга
        btn_ping = Button(
            text="ПРОВЕРИТЬ ПИНГ", 
            bold=True,
            background_color=get_color_from_hex('#222222')
        )
        btn_ping.bind(on_release=self.check_network)
        layout.add_widget(btn_ping)

        return layout

    def add_from_clip(self, instance):
        data = Clipboard.paste()
        if "://" in data:
            self.servers.append(data)
            self.status.text = f"ДОБАВЛЕНО СЕРВЕРОВ: {len(self.servers)}"
            self.status.color = (0, 1, 0, 1) # Зеленый
        else:
            self.status.text = "В БУФЕРЕ НЕТ КЛЮЧА!"
            self.status.color = (1, 0, 0, 1) # Красный

    def check_network(self, instance):
        # Простая проверка связи с Google для теста пинга
        self.status.text = "ПРОВЕРКА СВЯЗИ..."
        try:
            start = time.time()
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            ping = int((time.time() - start) * 1000)
            self.status.text = f"СВЯЗЬ ЕСТЬ! ПИНГ: {ping}ms"
            self.status.color = (0, 1, 0, 1)
        except:
            self.status.text = "ОШИБКА СЕТИ (ПРОВЕРЬ ИНТЕРНЕТ)"
            self.status.color = (1, 0, 0, 1)

if __name__ == '__main__':
    SwillWayApp().run()

