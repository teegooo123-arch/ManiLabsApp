import os, shutil, sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window

NAVY = (0.055, 0.11, 0.20, 1)
TEAL = (0.00, 0.58, 0.57, 1)
PALE = (0.95, 0.97, 0.98, 1)
TEXT = (0.10, 0.16, 0.23, 1)
MUTED = (0.40, 0.47, 0.54, 1)
WHITE = (1, 1, 1, 1)

KV = r'''
#:import dp kivy.metrics.dp

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(0)
        canvas.before:
            Color:
                rgba: .95,.97,.98,1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(104)
            padding: dp(18),dp(14)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: .055,.11,.20,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(3)
                Label:
                    text: 'MANI LABS SOLUTION'
                    bold: True
                    font_size: '20sp'
                    color: 1,1,1,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                Label:
                    text: 'TEST DIRECTORY  •  OFFLINE SEARCH'
                    font_size: '11sp'
                    color: .55,.83,.84,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
            Button:
                text: '+  ADD TEST'
                size_hint: None,None
                size: dp(104),dp(42)
                pos_hint: {'center_y': .5}
                background_normal: ''
                background_color: 0,.58,.57,1
                color: 1,1,1,1
                bold: True
                font_size: '12sp'
                on_release: app.open_editor(None)
        BoxLayout:
            orientation: 'vertical'
            padding: dp(16),dp(14),dp(16),dp(8)
            spacing: dp(10)
            BoxLayout:
                size_hint_y: None
                height: dp(52)
                padding: dp(12),0
                spacing: dp(8)
                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(12)]
                Label:
                    text: '⌕'
                    size_hint_x: None
                    width: dp(26)
                    font_size: '28sp'
                    color: .0,.58,.57,1
                TextInput:
                    id: search
                    hint_text: 'Search by code or test name'
                    multiline: False
                    font_size: '16sp'
                    foreground_color: .10,.16,.23,1
                    hint_text_color: .52,.58,.64,1
                    background_normal: ''
                    background_active: ''
                    background_color: 1,1,1,0
                    cursor_color: 0,.58,.57,1
                    padding: 0,dp(14)
                    on_text: app.search(self.text)
                Button:
                    text: '×'
                    size_hint_x: None
                    width: dp(30)
                    background_normal: ''
                    background_color: 1,1,1,0
                    color: .45,.51,.57,1
                    font_size: '24sp'
                    on_release: search.text = ''
            BoxLayout:
                size_hint_y: None
                height: dp(30)
                Label:
                    id: count
                    text: 'TESTS AVAILABLE'
                    bold: True
                    font_size: '12sp'
                    color: .34,.41,.48,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                Label:
                    text: 'TAP A TEST FOR DETAILS'
                    font_size: '10sp'
                    color: .49,.56,.62,1
                    halign: 'right'
                    valign: 'middle'
                    text_size: self.size
            ScrollView:
                do_scroll_x: False
                bar_width: dp(3)
                GridLayout:
                    id: results
                    cols: 1
                    spacing: dp(9)
                    padding: 0,dp(2),0,dp(12)
                    size_hint_y: None
                    height: self.minimum_height

                Label:
                    text: 'Powered by Mani 0322-7022841'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '11sp'
                    color: .40,.47,.54,1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

<DetailScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: .95,.97,.98,1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(62)
            padding: dp(12),dp(8)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: .055,.11,.20,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '‹  BACK'
                size_hint_x: None
                width: dp(82)
                background_normal: ''
                background_color: .14,.21,.30,1
                color: 1,1,1,1
                bold: True
                on_release: app.go_home()
            Label:
                text: 'TEST DETAILS'
                bold: True
                font_size: '18sp'
                color: 1,1,1,1
                halign: 'left'
                valign: 'middle'
                text_size: self.size
        ScrollView:
            do_scroll_x: False
            GridLayout:
                cols: 1
                spacing: dp(10)
                padding: dp(16),dp(16),dp(16),dp(20)
                size_hint_y: None
                height: self.minimum_height
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(116)
                    padding: dp(16),dp(12)
                    spacing: dp(5)
                    canvas.before:
                        Color:
                            rgba: .055,.11,.20,1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(14)]
                    Label:
                        text: 'TEST NAME'
                        font_size: '11sp'
                        bold: True
                        color: .52,.84,.83,1
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size
                        size_hint_y: None
                        height: dp(22)
                    Label:
                        text: root.test_name
                        font_size: '21sp'
                        bold: True
                        color: 1,1,1,1
                        halign: 'left'
                        valign: 'top'
                        text_size: self.width,None
                        size_hint_y: None
                        height: self.texture_size[1]+dp(4)
                GridLayout:
                    cols: 2
                    spacing: dp(9)
                    size_hint_y: None
                    height: dp(100)
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(4)
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        Label:
                            text: 'TEST CODE'
                            font_size: '11sp'
                            bold: True
                            color: .42,.49,.56,1
                            halign: 'left'
                            text_size: self.size
                        Label:
                            text: root.code
                            font_size: '21sp'
                            bold: True
                            color: .0,.58,.57,1
                            halign: 'left'
                            text_size: self.size
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(4)
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        Label:
                            text: 'REPORTING TIME'
                            font_size: '11sp'
                            bold: True
                            color: .42,.49,.56,1
                            halign: 'left'
                            text_size: self.size
                        Label:
                            text: root.reporting
                            font_size: '16sp'
                            bold: True
                            color: .10,.16,.23,1
                            halign: 'left'
                            valign: 'top'
                            text_size: self.width,None
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(112)
                        padding: dp(14)
                        spacing: dp(7)
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        Label:
                            text: 'SPECIMEN'
                            size_hint_y: None
                            height: dp(20)
                            font_size: '11sp'
                            bold: True
                            color: .42,.49,.56,1
                            halign: 'left'
                            text_size: self.size
                        Label:
                            text: root.specimen
                            font_size: '15sp'
                            color: .10,.16,.23,1
                            halign: 'left'
                            valign: 'top'
                            text_size: self.width,None
                            size_hint_y: None
                            height: max(dp(38),self.texture_size[1])
                    GridLayout:
                        cols: 2
                        size_hint_y: None
                        height: dp(104)
                        spacing: dp(9)
                        BoxLayout:
                            orientation: 'vertical'
                            padding: dp(14)
                            spacing: dp(6)
                            canvas.before:
                                Color:
                                    rgba: .88,.96,.95,1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [dp(12)]
                            Label:
                                text: 'LIST PRICE'
                                font_size: '11sp'
                                bold: True
                                color: .18,.43,.42,1
                                halign: 'left'
                                text_size: self.size
                            Label:
                                text: root.price
                                font_size: '24sp'
                                bold: True
                                color: .05,.30,.31,1
                                halign: 'left'
                                text_size: self.size
                        BoxLayout:
                            orientation: 'vertical'
                            padding: dp(14)
                            spacing: dp(6)
                            canvas.before:
                                Color:
                                    rgba: .90,.93,.98,1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [dp(12)]
                            Label:
                                text: 'B2B PRICE'
                                font_size: '11sp'
                                bold: True
                                color: .25,.36,.58,1
                                halign: 'left'
                                text_size: self.size
                            Label:
                                text: root.b2b
                                font_size: '24sp'
                                bold: True
                                color: .12,.22,.43,1
                                halign: 'left'
                                text_size: self.size
                Button:
                    text: '✎   EDIT TEST DETAILS'
                    size_hint_y: None
                    height: dp(52)
                    background_normal: ''
                    background_color: 0,.58,.57,1
                    color: 1,1,1,1
                    bold: True
                    on_release: app.open_editor(root.test_id)
                Button:
                    text: 'DELETE TEST'
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ''
                    background_color: .75,.22,.25,1
                    color: 1,1,1,1
                    on_release: app.confirm_delete(root.test_id)

<EditorScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: .95,.97,.98,1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(62)
            padding: dp(12),dp(8)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: .055,.11,.20,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: '‹  BACK'
                size_hint_x: None
                width: dp(82)
                background_normal: ''
                background_color: .14,.21,.30,1
                color: 1,1,1,1
                bold: True
                on_release: app.go_home()
            Label:
                text: root.heading
                bold: True
                font_size: '18sp'
                color: 1,1,1,1
                halign: 'left'
                text_size: self.size
        ScrollView:
            do_scroll_x: False
            GridLayout:
                cols: 1
                spacing: dp(7)
                padding: dp(16),dp(14),dp(16),dp(22)
                size_hint_y: None
                height: self.minimum_height
                Label:
                    text: 'TEST CODE  *'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '12sp'
                    bold: True
                    color: .25,.33,.41,1
                    halign: 'left'
                    text_size: self.size
                TextInput:
                    id: code
                    hint_text: 'Enter unique test code'
                    multiline: False
                    size_hint_y: None
                    height: dp(50)
                    padding: dp(12),dp(13)
                    font_size: '16sp'
                Label:
                    text: 'TEST NAME  *'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '12sp'
                    bold: True
                    color: .25,.33,.41,1
                    halign: 'left'
                    text_size: self.size
                TextInput:
                    id: name
                    hint_text: 'Enter full test name'
                    multiline: False
                    size_hint_y: None
                    height: dp(50)
                    padding: dp(12),dp(13)
                    font_size: '16sp'
                Label:
                    text: 'SPECIMEN'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '12sp'
                    bold: True
                    color: .25,.33,.41,1
                    halign: 'left'
                    text_size: self.size
                TextInput:
                    id: specimen
                    hint_text: 'Specimen / sample requirements'
                    size_hint_y: None
                    height: dp(86)
                    padding: dp(12),dp(12)
                    font_size: '15sp'
                Label:
                    text: 'REPORTING TIME'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '12sp'
                    bold: True
                    color: .25,.33,.41,1
                    halign: 'left'
                    text_size: self.size
                TextInput:
                    id: reporting
                    hint_text: 'e.g. SAME DAY / DAILY'
                    multiline: False
                    size_hint_y: None
                    height: dp(50)
                    padding: dp(12),dp(13)
                    font_size: '15sp'
                GridLayout:
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(98)
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(5)
                        Label:
                            text: 'PRICE'
                            size_hint_y: None
                            height: dp(24)
                            font_size: '12sp'
                            bold: True
                            color: .25,.33,.41,1
                            halign: 'left'
                            text_size: self.size
                        TextInput:
                            id: price
                            hint_text: 'List price'
                            multiline: False
                            padding: dp(12),dp(13)
                            font_size: '15sp'
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(5)
                        Label:
                            text: 'B2B PRICE'
                            size_hint_y: None
                            height: dp(24)
                            font_size: '12sp'
                            bold: True
                            color: .25,.33,.41,1
                            halign: 'left'
                            text_size: self.size
                        TextInput:
                            id: b2b
                            hint_text: 'B2B price'
                            multiline: False
                            padding: dp(12),dp(13)
                            font_size: '15sp'
                Button:
                    text: 'SAVE TEST DETAILS'
                    size_hint_y: None
                    height: dp(54)
                    background_normal: ''
                    background_color: 0,.58,.57,1
                    color: 1,1,1,1
                    bold: True
                    on_release: app.save_editor()
'''

DB_NAME = 'tests.db'

class MainScreen(Screen): pass
class DetailScreen(Screen):
    title = StringProperty('Test Details')
    test_id = NumericProperty(0)
    code = StringProperty('')
    test_name = StringProperty('')
    specimen = StringProperty('')
    reporting = StringProperty('')
    price = StringProperty('')
    b2b = StringProperty('')
class EditorScreen(Screen):
    heading = StringProperty('Add Test')
    edit_id = NumericProperty(0)

class TestApp(App):
    def build(self):
        self.title = 'Mani Labs Solution'
        Builder.load_string(KV)
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='home'))
        self.sm.add_widget(DetailScreen(name='detail'))
        self.sm.add_widget(EditorScreen(name='editor'))
        self.db_path = os.path.join(self.user_data_dir, DB_NAME)
        if not os.path.exists(self.db_path):
            src = os.path.join(os.path.dirname(__file__), DB_NAME)
            shutil.copy2(src, self.db_path)
        self.search('')
        return self.sm

    def conn(self):
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def search(self, q):
        if not hasattr(self, 'sm') or not self.sm.has_screen('home'):
            return
        q = (q or '').strip()
        c = self.conn()
        if q:
            like = '%' + q + '%'
            rows = c.execute('''SELECT * FROM tests WHERE code LIKE ? OR test_name LIKE ?
                                ORDER BY test_name COLLATE NOCASE LIMIT 150''', (like, like)).fetchall()
            self.sm.get_screen('home').ids.count.text = f'{len(rows)} MATCHING TEST(S)'
        else:
            rows = []
            total = c.execute('SELECT COUNT(*) FROM tests').fetchone()[0]
            self.sm.get_screen('home').ids.count.text = f'{total} TESTS AVAILABLE'
        c.close()
        box = self.sm.get_screen('home').ids.results
        box.clear_widgets()
        if q and not rows:
            msg = Label(text='No tests found. Try another code or spelling.', color=MUTED,
                        size_hint_y=None, height=dp(70), font_size='14sp')
            box.add_widget(msg)
        for r in rows:
            title = (r['test_name'] or '').replace('[', '\\[').replace(']', '\\]')
            code = (r['code'] or '').replace('[', '\\[').replace(']', '\\]')
            b = Button(text=f'[color=00a6a2][b]{code}[/b][/color]    [color=17283a]{title}[/color]\n[size=11sp][color=71808d]Tap to view full details[/color][/size]',
                       markup=True, size_hint_y=None, height=dp(76), halign='left', valign='middle',
                       text_size=(Window.width-dp(64), None), padding=(dp(16), dp(10)),
                       background_normal='', background_down='', background_color=(1,1,1,1),
                       color=TEXT, font_size='14sp')
            b.bind(on_release=lambda btn, rid=r['id']: self.show_detail(rid))
            box.add_widget(b)

    def show_detail(self, rid):
        c = self.conn()
        r = c.execute('SELECT * FROM tests WHERE id=?', (rid,)).fetchone()
        c.close()
        if not r:
            return
        s = self.sm.get_screen('detail')
        s.test_id = rid
        s.code = r['code'] or '-'
        s.test_name = (r['test_name'] or '-').replace('**', '')
        s.specimen = r['specimen'] or 'Not listed in source PDF'
        s.reporting = r['reporting_time'] or 'Not listed in source PDF'
        s.price = r['price'] or '-'
        s.b2b = r['b2b'] or '-'
        self.sm.current = 'detail'

    def open_editor(self, rid):
        s = self.sm.get_screen('editor')
        s.edit_id = rid or 0
        s.heading = 'Edit Test Details' if rid else 'Add New Test'
        for k in ['code', 'name', 'specimen', 'reporting', 'price', 'b2b']:
            s.ids[k].text = ''
        if rid:
            c = self.conn()
            r = c.execute('SELECT * FROM tests WHERE id=?', (rid,)).fetchone()
            c.close()
            if r:
                s.ids.code.text = r['code'] or ''
                s.ids.name.text = (r['test_name'] or '').replace('**', '')
                s.ids.specimen.text = r['specimen'] or ''
                s.ids.reporting.text = r['reporting_time'] or ''
                s.ids.price.text = r['price'] or ''
                s.ids.b2b.text = r['b2b'] or ''
        self.sm.current = 'editor'

    def save_editor(self):
        s = self.sm.get_screen('editor')
        vals = [s.ids.code.text.strip(), s.ids.name.text.strip(), s.ids.specimen.text.strip(),
                s.ids.reporting.text.strip(), s.ids.price.text.strip(), s.ids.b2b.text.strip()]
        if not vals[0] or not vals[1]:
            return self.notice('Test Code and Test Name are required.')
        c = self.conn()
        try:
            duplicate = c.execute('SELECT id FROM tests WHERE code=? AND id<>?', (vals[0], s.edit_id or -1)).fetchone()
            if duplicate:
                c.close()
                return self.notice('This test code is already in use. Please check the code.')
            if s.edit_id:
                c.execute('''UPDATE tests SET code=?,test_name=?,specimen=?,reporting_time=?,price=?,b2b=?,
                             updated_at=CURRENT_TIMESTAMP WHERE id=?''', (*vals, s.edit_id))
                rid = s.edit_id
            else:
                c.execute('INSERT INTO tests(code,test_name,specimen,reporting_time,price,b2b) VALUES(?,?,?,?,?,?)', vals)
                rid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
            c.commit()
        except sqlite3.Error as e:
            c.close()
            return self.notice('Could not save test: ' + str(e))
        c.close()
        self.show_detail(rid)

    def confirm_delete(self, rid):
        row = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(12))
        row.add_widget(Label(text='Delete this test from your mobile database?', color=TEXT))
        buttons = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        p = Popup(title='Confirm Delete', content=row, size_hint=(.88, .28), auto_dismiss=True)
        yes = Button(text='DELETE', background_normal='', background_color=(.75,.22,.25,1), color=WHITE)
        no = Button(text='CANCEL', background_normal='', background_color=(.20,.29,.38,1), color=WHITE)
        buttons.add_widget(yes); buttons.add_widget(no); row.add_widget(buttons)
        yes.bind(on_release=lambda *_: (self.delete_test(rid), p.dismiss()))
        no.bind(on_release=p.dismiss)
        p.open()

    def delete_test(self, rid):
        c = self.conn()
        c.execute('DELETE FROM tests WHERE id=?', (rid,))
        c.commit(); c.close()
        self.go_home()

    def notice(self, msg):
        Popup(title='Mani Labs Solution', content=Label(text=msg, color=TEXT),
              size_hint=(.86,.30)).open()

    def go_home(self):
        self.sm.current = 'home'
        self.search(self.sm.get_screen('home').ids.search.text)

if __name__ == '__main__':
    TestApp().run()
