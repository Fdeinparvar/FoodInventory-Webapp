import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests

API_URL = 'http://127.0.0.1:5000/items'
COLUMNS = ['item', 'dateofpurchase', 'weight', 'amount']

class InventoryApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.list_layout = GridLayout(cols=1, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.scroll.add_widget(self.list_layout)
        self.root.add_widget(self.scroll)
        btn_layout = BoxLayout(size_hint=(1, 0.1))
        add_btn = Button(text='Add New')
        add_btn.bind(on_release=self.add_item_popup)
        refresh_btn = Button(text='Refresh')
        refresh_btn.bind(on_release=lambda x: self.load_items())
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(refresh_btn)
        self.root.add_widget(btn_layout)
        self.status = Label(size_hint=(1, 0.1))
        self.root.add_widget(self.status)
        self.load_items()
        return self.root

    def load_items(self):
        self.list_layout.clear_widgets()
        try:
            resp = requests.get(API_URL)
            items = resp.json()
            for item in items:
                row = BoxLayout(size_hint_y=None, height=40)
                for col in COLUMNS:
                    row.add_widget(Label(text=str(item[col]), size_hint_x=0.2))
                edit_btn = Button(text='Edit', size_hint_x=0.1)
                edit_btn.bind(on_release=lambda btn, i=item: self.edit_item_popup(i))
                del_btn = Button(text='Delete', size_hint_x=0.1)
                del_btn.bind(on_release=lambda btn, i=item: self.delete_item(i['rowid']))
                row.add_widget(edit_btn)
                row.add_widget(del_btn)
                self.list_layout.add_widget(row)
            self.status.text = f'Loaded {len(items)} items.'
        except Exception as e:
            self.status.text = f'Error loading items: {e}'

    def add_item_popup(self, instance):
        self.open_item_popup('Add Item', {}, self.add_item)

    def edit_item_popup(self, item):
        self.open_item_popup('Edit Item', item, lambda vals: self.edit_item(item['rowid'], vals))

    def open_item_popup(self, title, item, on_save):
        content = BoxLayout(orientation='vertical')
        inputs = {}
        for col in COLUMNS:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            box.add_widget(Label(text=col, size_hint_x=0.4))
            ti = TextInput(text=str(item.get(col, '')), multiline=False, size_hint_x=0.6)
            box.add_widget(ti)
            content.add_widget(box)
            inputs[col] = ti
        btn_box = BoxLayout(size_hint_y=None, height=40)
        ok_btn = Button(text='OK')
        cancel_btn = Button(text='Cancel')
        btn_box.add_widget(ok_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        def save_and_close(instance):
            vals = {col: inputs[col].text for col in COLUMNS}
            on_save(vals)
            popup.dismiss()
        ok_btn.bind(on_release=save_and_close)
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def add_item(self, vals):
        try:
            resp = requests.post(API_URL, json=vals)
            if resp.status_code == 201:
                self.status.text = 'Item added.'
                self.load_items()
            else:
                self.status.text = f'Failed to add: {resp.text}'
        except Exception as e:
            self.status.text = f'Error: {e}'

    def edit_item(self, rowid, vals):
        try:
            resp = requests.put(f'{API_URL}/{rowid}', json=vals)
            if resp.status_code == 200:
                self.status.text = 'Item updated.'
                self.load_items()
            else:
                self.status.text = f'Failed to update: {resp.text}'
        except Exception as e:
            self.status.text = f'Error: {e}'

    def delete_item(self, rowid):
        try:
            resp = requests.delete(f'{API_URL}/{rowid}')
            if resp.status_code == 200:
                self.status.text = 'Item deleted.'
                self.load_items()
            else:
                self.status.text = f'Failed to delete: {resp.text}'
        except Exception as e:
            self.status.text = f'Error: {e}'

if __name__ == '__main__':
    InventoryApp().run() 