from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex('#050505')

class SwillWayApp(App):
    def build(self):
        self.title = "Swill Way VPN"
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(
            text="SWILL WAY VPN", 
            font_size='32sp', 
            bold=True, 
            color=(1,1,1,1)
        ))
        
        self.btn = Button(
            text="START", 
            size_hint=(None, None), 
            size=(250, 250),
            pos_hint={'center_x': 0.5}, 
            background_normal='',
            background_color=get_color_from_hex('#111111'),
            font_size='24sp', 
            bold=True
        )
        self.btn.bind(on_press=self.toggle)
        layout.add_widget(self.btn)
        
        self.status = Label(
            text="ГОТОВ К ПОДКЛЮЧЕНИЮ", 
            color=get_color_from_hex('#00ff88')
        )
        layout.add_widget(self.status)
        
        return layout

    def toggle(self, instance):
        if self.btn.text == "START":
            self.btn.text = "STOP"
            self.btn.background_color = get_color_from_hex('#00ff88')
            self.btn.color = (0,0,0,1)
            self.status.text = "Впн подключен ✅"
        else:
            self.btn.text = "START"
            self.btn.background_color = get_color_from_hex('#111111')
            self.btn.color = (1,1,1,1)
            self.status.text = "Впн отключен ❌"

if __name__ == "__main__":
    SwillWayApp().run()
