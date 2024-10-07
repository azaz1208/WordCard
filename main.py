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
class Plus_WordCard_layout(MDBoxLayout):
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
        LabelBase.register(name="MSJH", fn_regular="./fonts/blackH1.otf")

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
                    on_release = lambda x : self.show_last_card_dialog(card_id)
                ),
                MDFlatButton(
                    text = "Next",
                    on_release = lambda x : self.show_next_card_dialog(card_id)
                ),
                MDFlatButton(
                    text = "Edit",
                    on_release = lambda x : self.show_edit_card_dialog(card_id)
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
    def show_edit_card_dialog(self,card_id):
        # close any open dialog first
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        # 取得原有字卡的資料
        card_data = self.sum_dict.get(card_id,{})

        # 如果找不到資料就不做任何事
        if not card_data:
            return

        # 產生一個已經填好原有資料的內容
        content = AddCardDialog_Content()
        content.ids.word_input.text = card_data.get("word", "")
        content.ids.meaning_input.text = card_data.get("meaning", "")
        content.ids.sentence_input.text = card_data.get("sentence", "")


        self.dialog = MDDialog(
            title = "Edit word",
            type = "custom",
            content_cls = content,
            buttons = [
                MDFlatButton(
                    text="CANCEL",
                    # theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    # theme_text_color="Custo
                    on_release = lambda x :self.save_edited_card(card_id)
                )
            ],
        )

        self.dialog.open()
    def save_edited_card(self,card_id):

        # get the data user edited
        word_card = self.getTextInput()

        # update sum_dict 
        self.sum_dict[card_id] = word_card

        # update wordcard label
        for card in self.root.ids.wordCard_area.children:
            if card.card_id == card_id:
                card.text = word_card.get("word","")
                break
        print(f"card Data updated: {self.sum_dict}")

        self.close_dialog()
        self.dialog = None
        self.on_wordCard_label_press(card_id)
    def show_next_card_dialog(self,card_id):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        # 先取得所有的card_id
        all_card_id = list(self.sum_dict.keys())

        if all_card_id == []:
            return

        # 找出當前這張卡是第幾張
        current_card_index = all_card_id.index(card_id)

        # (狀況一：當前的卡是最後一張)
        if current_card_index == len(all_card_id)-1:
            next_card_index = 0
        else:
            # 找出下一張 (狀況二：當前的卡不是最後一張)
            next_card_index = current_card_index +1 

        # 找出下一張卡的card id
        next_card_id = all_card_id[next_card_index]

        self.on_wordCard_label_press(next_card_id)

    def show_last_card_dialog(self,card_id):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        # 先取得所有的card_id
        all_card_id = list(self.sum_dict.keys())

        if all_card_id == []:
            return

        # 找出當前這張卡是第幾張
        current_card_index = all_card_id.index(card_id)

        # (狀況一：當前的卡是第一張)
        if current_card_index == 0 :
            last_card_index = -1
        else:
            # 找出上一張 (狀況二：當前的卡不是第一張)
            last_card_index = current_card_index -1 

        # 找出上一張卡的card id
        last_card_id = all_card_id[last_card_index]

        self.on_wordCard_label_press(last_card_id)









if __name__ == '__main__':
    MainApp().run() 