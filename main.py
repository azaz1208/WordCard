from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

Window.size = (400, 600)

class WordCard_layout(MDBoxLayout):
    text = StringProperty("")


class MainApp(MDApp):
    # buid MainApp (白話：用kivyMD就要照他的規則，所以一定得寫build)
    # build 可以決定整個 APP 的視窗內容長什麼樣子
    # return 什麼，就會長什麼樣子
    def build(self):  
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('my_layout.kv')

    # 設定當我按下某個btn的時候，我的APP視窗要增加一行 字卡格子
    def add_card(self,*arg):
        new_card = WordCard_layout(text = "New Card!")
        self.root.ids.wordCard_area.add_widget(new_card)

    # 關閉彈出視窗的效果
    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    # 彈出新增字卡的視窗
    def show_add_card_dialog(self):
        self.dialog = MDDialog(
            title = "Add new word",
            type = "custom",

            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text = "ADD",
                    on_release = self.add_card
                )
            ]
        )
        self.dialog.open()

        

if __name__ == '__main__':
    MainApp().run() 