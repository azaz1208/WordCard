from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
# from kivy.uix.label import Label
# from kivymd.uix.textfield import MDTextField
# from kivy.utils import get_color_from_hex
import uuid
import json


# Set window size
Window.size = (400, 600)

class Content(MDBoxLayout):
    pass

class MyCardLayout(MDBoxLayout):
    text = StringProperty()
    card_id = StringProperty()  # Add card_id property
    
class OrgCardLayout(MDBoxLayout):
    text = StringProperty()
    card_id = StringProperty()  # Add card_id property

class MainApp(MDApp):
    def build(self):
        LabelBase.register(name="MSJH", fn_regular="./fonts/MSJH.TTC")
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.accent_palette = "Red"
        return Builder.load_file('scroll_box2.kv')
    
    def on_wordcard_label_press(self, card_id):
        # Get card data based on ID
        card_data = self.card_data.get(card_id, {})
        
        # 使用字卡的 "word" 作為對話框的標題
        word = card_data.get("word", "Unknown Word")
        
        # Create a custom title label with larger font size
        custom_title = MDLabel(
            text=word,
            font_style="H2",  # You can use predefined font styles or set a custom font size
            halign="center",
            size_hint_y=None,
            height="80dp",
            # size_hint=(0.9, 0.7),
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            font_name="MSJH"
        )
        
        # Create and open dialog to display card data
        self.dialog = MDDialog(
            # title="",  # Leave the title empty to use custom title
            type="custom",
            content_cls=self.create_card_detail_content(card_data, custom_title),
            size_hint_x=0.9,
            size_hint_y=None,
            buttons=[
                MDFlatButton(
                    text="Last",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    size_hint_x=0.25,  # Set size hint to 1/5 of the dialog width
                    on_release=lambda btn: self.show_lastWordCard_dialog(card_id)
                ),
                MDFlatButton(
                    text="NEXT",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    size_hint_x=0.25,  # Set size hint to 1/5 of the dialog width
                    on_release=lambda btn: self.show_nextWordCard_dialog(card_id)
                ),
                MDFlatButton(
                    text="Edit",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    size_hint_x=0.25,  # Set size hint to 1/5 of the dialog width
                    on_release=lambda btn: self.show_editWordCard_dialog(card_id)
                ),
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    size_hint_x=0.25,  # Set size hint to 1/5 of the dialog width
                    on_release=self.close_dialog
                ),
            ],
        )
        
        self.dialog.open()
        
    def create_card_detail_content(self, card_data, custom_title):
        # Create content for the dialog based on card data
        content = MDBoxLayout(orientation='vertical', padding="12dp", spacing="12dp", size_hint_y=None, height="250dp")
        content.add_widget(custom_title)  # Add the custom title
        content.add_widget(MDLabel(
            text=f"{card_data.get('meaning', '')}", 
            font_size='48dp',
            font_name="MSJH",
            theme_text_color="Custom",  # 自定義顏色
            text_color=(137/255, 196/255, 244/255, 1)
            ))
        content.add_widget(MDLabel(
            text=f"{card_data.get('sentence', '')}", 
            font_size='36dp',
            font_name="MSJH",
            theme_text_color="Custom",  # 自定義顏色
            text_color=(1, 1, 1, 1)
            ))
        return content

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
                
    def show_addWordCard_dialog(self):
        # if not self.dialog:
        self.dialog = MDDialog(
            title="Add new word",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.add_card
                ),
            ],
        )
        self.dialog.open()
        
    def add_card(self, *args):
        WMS_data = self.get_text_inputs()  # 取得用戶輸入的資料
        if WMS_data["word"] != "":
            card_id = str(uuid.uuid4())  # 生成唯一的 ID
            
            # Create a new MyCardLayout instance
            new_card = MyCardLayout(text = WMS_data["word"], card_id=card_id)
            
            # Add the new card to the 'word_card_area' layout
            self.root.ids.word_card_area.add_widget(new_card)
            
            # 紀錄字卡資料
            self.record_card_data(card_id, WMS_data)
        
    def get_text_inputs(self, *args):
        # 取得 kv 文件中定義的 ID 並讀取相應的文字
        word = self.dialog.content_cls.ids.word_input.text
        meaning = self.dialog.content_cls.ids.meaning_input.text
        sentence = self.dialog.content_cls.ids.sentence_input.text

        self.close_dialog()   
        return {
            "word": word,
            "meaning": meaning,
            "sentence": sentence
        }
        
    def record_card_data(self, card_id, data):
        # 將每張字卡的資料儲存到字典中
        if not hasattr(self, 'card_data'):
            self.card_data = {}

        self.card_data.update({card_id: data})
        print(f"Card Data Recorded: {self.card_data}")
        
    def show_editWordCard_dialog(self, card_id):
        # Close any open dialogs first
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
            
        # 取得要編輯的字卡資料
        card_data = self.card_data.get(card_id, {})
        
        # 如果找不到資料則不做任何事
        if not card_data:
            return
        
        # 建立一個包含現有資料的自定義內容
        content = Content()
        content.ids.word_input.text = card_data.get("word", "")
        content.ids.meaning_input.text = card_data.get("meaning", "")
        content.ids.sentence_input.text = card_data.get("sentence", "")
        
        # 創建並開啟對話框以顯示字卡資料供編輯
        self.dialog = MDDialog(
            title="Edit Word",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda btn: self.save_edited_card(card_id)
                ),
            ],
        )
        self.dialog.open()

    def save_edited_card(self, card_id):
        # 取得編輯後的輸入資料
        WMS_data = self.get_text_inputs()
        
        self.card_data[card_id] = WMS_data
        
        # 更新對應字卡上的文字
        for card in self.root.ids.word_card_area.children:
            if hasattr(card, 'card_id') and card.card_id == card_id:
                card.text = WMS_data["word"]
                break

        print(f"Card Data Updated: {self.card_data}")
        
        # Close the dialog and refresh the display dialog
        self.close_dialog()
        # After closing, reset dialog and re-open the updated card
        self.dialog = None
        self.on_wordcard_label_press(card_id)  # Refresh the dialog to show updated data
    
    def show_lastWordCard_dialog(self, current_card_id):
        # Close any open dialogs first
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        
        # Get all card IDs
        all_card_ids = list(self.card_data.keys())
        
        if not all_card_ids:
            print("No cards available.")
            return
        
        # Find the index of the current card
        current_index = all_card_ids.index(current_card_id) if current_card_id in all_card_ids else -1
        
        # Determine the ID of the previous card
        if current_index > 0:
            last_card_id = all_card_ids[current_index - 1]
        else:
            last_card_id = all_card_ids[-1]
            print("No previous card. Show last card")
            
        self.on_wordcard_label_press(last_card_id)

    def show_nextWordCard_dialog(self, current_card_id):
        # Close any open dialogs first
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        
        # Get all card IDs
        all_card_ids = list(self.card_data.keys())
        
        if not all_card_ids:
            print("No cards available.")
            return
        
        # Find the index of the current card
        current_index = all_card_ids.index(current_card_id) if current_card_id in all_card_ids else -1
        
        # Determine the ID of the next card
        if current_index < len(all_card_ids) - 1:
            next_card_id = all_card_ids[current_index + 1]
        else:
            next_card_id = all_card_ids[0]
            print("No next card. Show first card")

        self.on_wordcard_label_press(next_card_id)
        
if __name__ == '__main__':
    MainApp().run()
    