from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.clipboard import Clipboard
from Connection import Connection

'''
Builder.load_string("""
<Clippy>:
    cols: 1
    ScrollView:
        size: self.size
        TextInput:
            text: root.data_model.clip_text
            readonly: True
""")
'''


class DataModel(EventDispatcher):
    """
    Creates a DataModel for storing clipboard text as a Kivy StringProperty
    EventDispatcher is used to manage callbacks.
    """
    clip_text = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(DataModel, self).__init__(*args, **kwargs)
        self.clip_text = ''


class Clippy(GridLayout):
    """
    GridLayout Gui component.
    """
    data_model = ObjectProperty(DataModel())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Connection  # Initializes the Connection class.
        self.conn = self.db.init_DB()
        self.last_record = self.db.get_last_record(self.conn)
        self.times_updated = 1  # For handling the individual Clippy Entries.
        Clock.schedule_interval(self.on_update, 1 / 30.)  # Schedules on_update 30 times/second.

    def on_update(self, dt):
        """
        on_update callback gets clipboard and decides
        if the value is different than the value previously stored.
        """
        if 'text/plain' == ''.join(Clipboard.get_types()[0]):
            # Logger.info(Clippy.get_types())
            if Clipboard.paste():
                data = Clipboard.paste()  # Gets the data currently in the clipboard
            else:
                data = None
        else:
            Logger.info('on_update', Clipboard.get_types())
            data = 'Unsupported type'

        if data != self.last_record:
            self.db.insert_new_record(self.conn, data)
            self.last_record = data
            self.data_model.clip_text += ('\nClip {0}:\n{1}'.format(self.times_updated, data))
            self.times_updated += 1


class ClippyApp(App):
    def build(self):
        clippy = Clippy()
        return clippy


if __name__ == '__main__':
    ClippyApp().run()
