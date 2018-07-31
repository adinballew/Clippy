from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import *
from kivy.core.clipboard import Clipboard
from Connection import Connection


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

        def get_clip_data():
            """Gets the data currently in the clipboard"""
            if 'text/plain' == ''.join(Clipboard.get_types()[0]):
                # Logger.info(Clippy.get_types())
                d = Clipboard.paste()
            else:
                Logger.info('on_update', Clipboard.get_types())
                d = 'Unsupported type'
            return d

        data = get_clip_data()
        if data != self.last_record:
            self.db.insert_new_record(self.conn, data)
            self.last_record = data
            self.data_model.clip_text += ('\nClip {0}:\n{1}'.format(self.times_updated, data))
            self.times_updated += 1
            Logger.info(data)


class ClippyApp(App):
    def build(self):
        clippy = Clippy()
        return clippy


if __name__ == '__main__':
    ClippyApp().run()
