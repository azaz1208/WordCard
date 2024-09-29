from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.core.text import LabelBase
import uuid

Window.size = (400, 600)

class WordCard_layout(MDBoxLayout):
    text = StringProperty("")
    card_id = StringProperty("")
class AddCardDialog_Content(MDBoxLayout):
    pass

class MainApp(MDApp):
    # 初始化一個字典用來儲存使用者存的資料
    sum_dict = {}

    # buid MainApp (白話：用kivyMD就要照他的規則，所以一定得寫build)
    # build 可以決定整個 APP 的視窗內容長什麼樣子
    # return 什麼，就會長什麼樣子
    def build(self):  
        LabelBase.register(name="MSJH", fn_regular="./fonts/MSJH.TTC")

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('my_layout.kv')


    # 設定當我按下某個btn的時候，我的APP視窗要增加一行 字卡格子
    # 同時還要把使用者打的資料存起來
    def add_card(self,*arg):
        newCardData = self.getTextInput()
        if newCardData["word"] != "":
            # generate an unique id for every card
            card_id = str(uuid.uuid4())
            
            new_card = WordCard_layout(text = newCardData["word"], card_id = card_id)
            self.root.ids.wordCard_area.add_widget(new_card)

            # 存資料
            self.save_card_data(card_id, newCardData)

    def save_card_data(self, card_id, data):
        self.sum_dict[ card_id ] = data
        print(f'Data recorded: {self.sum_dict}')

    # 關閉彈出視窗的效果
    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    # 彈出新增字卡的視窗
    def show_add_card_dialog(self):
        self.dialog = MDDialog(
            title = "Add new word",
            content_cls =  AddCardDialog_Content(),
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
    
    def getTextInput(self, *args):
        word = self.dialog.content_cls.ids.word_input.text
        meaning = self.dialog.content_cls.ids.meaning_input.text
        sentence = self.dialog.content_cls.ids.sentence_input.text
        
        self.close_dialog() 
       
        data = {
            "word": word,
            "meaning": meaning,
            "sentence": sentence
        }
        
        print(data)
        return data
    
    def on_wordCard_label_press(self, card_id):
        # get card data based on card_id
        card_data = self.sum_dict.get(card_id, {})

        # get word as title
        # word = card_data.get("word", "unknown word")

        self.dialog = MDDialog(
            # title = word,
            type = "custom",
            content_cls = self.create_card_detail_content(card_data),
            text = f'Meaning: {card_data.get("meaning", "NA")}\n\nsentence: {card_data.get("sentence", "NA")}',
            buttons = [
                MDFlatButton(
                    text = "Last",
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text = "Next",
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text = "Edit",
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text = "Close",
                    on_release = self.close_dialog
                ),
            ],
        )

        self.dialog.open()

    def create_card_detail_content(self,card_data):
        content = MDBoxLayout(orientation ='vertical',spacing = "12dp",padding ="12dp",size_hint_y = None, height = "250dp")

        title = MDLabel(
            text = card_data.get("word","unknown word"),
            font_style = "H2",
            height = "80dp",
            halign = "center",
            theme_text_color="Custom",
            text_color=(0, 128/255, 255/255, 1),
        )
        content.add_widget(title)
        
        meaning = MDLabel(
            text = card_data.get("meaning",""),
            font_style = "H5",
            height = "48dp",
            theme_text_color="Custom",
            text_color=(1,1,1,1),
        )
        content.add_widget(meaning)

        sentence = MDLabel(
            text = card_data.get("sentence",""),
            font_style = "H5",
            height = "36dp",
            theme_text_color="Custom",
            text_color=(1,1,1,1),
        )
        content.add_widget(sentence)

        return content



if __name__ == '__main__':
    MainApp().run() 