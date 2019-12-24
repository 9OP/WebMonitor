import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango, GdkPixbuf

from database import MONITOR_METRICS
from datetime import datetime
from queue import Queue


class Interface(Gtk.Window):
    def __init__(self, **kwargs):
        # Window
        Gtk.Window.__init__(self, **kwargs)
        self.set_default_size(1100, 450)
        self.set_icon_from_file('media/icon.png')

        # HeaderBar
        self.spinner = Gtk.Spinner()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename='media/header_icon.png',
                width=150,
                height=150,
                preserve_aspect_ratio=True)
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)

        self.monitor_button = Gtk.ToggleButton(label="Start monitoring...")
        self.monitor_button.connect("toggled", self.on_monitor_button_toggled)
        self.monitor_button.set_active(False)
        self.monitor_button.set_size_request(width=200, height=20)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = 'Web Monitor'
        self.headerbar.props.subtitle = 'DataDog take home project - Martin GUYARD'
        self.headerbar.pack_start(self.spinner)
        self.headerbar.pack_start(self.monitor_button)
        self.headerbar.pack_start(self.image)
        self.headerbar.pack_start(Gtk.Separator())
        self.set_titlebar(self.headerbar)

        # MainFrame
        self.main_frame = MainFrame()

        # Pack
        self.add(self.main_frame.get_top_level_widget())

    def on_monitor_button_toggled(self, button):
        date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if button.get_active():
            self.spinner.start()
            self.send_message('info', date+' Start monitoring...')
            self.start_monitoring()
            self.monitor_button.set_label("Stop monitoring...")
        else:
            self.spinner.stop()
            self.send_message('info', date+' Stop monitoring...')
            self.stop_monitoring()
            self.monitor_button.set_label("Start monitoring...")


    def update_monitoring(self, metrics, mon):
        if mon=='10min':
            self.main_frame.mon_10min.update_liststore(metrics)
        elif mon=='1hour':
            self.main_frame.mon_1h.update_liststore(metrics)

    def send_message(self, type, message):
        self.main_frame.alert.print_message(type, message)

    def connect_to_monitor(self, start, stop):
        self.start_monitoring = start
        self.stop_monitoring = stop

    @staticmethod
    def start_monitoring():
        # Override with MonitorMaster.start_monitoring, in connect_to_monitor
        pass

    @staticmethod
    def stop_monitoring():
        # Overrine with MonitorMaster.stop_monitoring, in connect_to_monitor
        pass


class MainFrame:
    def __init__(self):
        # Paned
        self.paned = Gtk.VPaned()

        # 10 minutes look back monitor
        self.mon_10min = Monitor(title='10 minutes look back')

        # 1h look back monitor
        self.mon_1h = Monitor(title='1 hour look back')

        # alert box
        self.alert = AlertBox()

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.paned.add1(self.mon_10min.get_top_level_widget())
        self.paned.add2(self.mon_1h.get_top_level_widget())
        self.vbox.pack_start(self.paned, True, True, 0)
        self.vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, True, 0)
        self.vbox.pack_start(self.alert.get_top_level_widget(), True, True, 0)

    def get_top_level_widget(self):
        return self.vbox


class Monitor:
    def __init__(self, title):
        # MonitorLabel
        self.mon_label = Gtk.Label()
        self.mon_label.set_markup('<b>'+title+'</b>')

        self.info = Gtk.InfoBar()
        self.info.add(self.mon_label)

        # MonitorTreeview
        self.columns = MONITOR_METRICS
        self.mon_liststore = Gtk.ListStore(int, str, str, str, str, str, str, str)
        self.mon_treeview =  Gtk.TreeView.new_with_model(self.mon_liststore)

        for i, column_title in enumerate(self.columns):
            if i==0:
                renderer = Gtk.CellRendererProgress()
                column = Gtk.TreeViewColumn(column_title, renderer, value=i)
            else:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.mon_treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(self.mon_treeview)
        self.scrollable_treelist.set_size_request(400, 100)

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.info, False, False, 0)
        self.vbox.pack_start(self.scrollable_treelist, True, True, 0)

    def get_top_level_widget(self):
        # self.update_liststore([99, 'https://google.com', '1s', '2s', '200', '1kb', '2kb', 'text'])
        # self.update_liststore([53, 'https://facebook.com', '1s', '2s', '200', '1kb', '2kb', 'text'])
        return self.vbox

    def update_liststore(self, metrics):
        index = self.columns.index('Website')
        website = metrics[index]
        if website:
            for i, row in enumerate(self.mon_liststore):
                if row[index] == website:
                    self.mon_liststore[i] = metrics
                    return #break flow... not super clean
            self.mon_liststore.append(metrics)


class AlertBox:
    def __init__(self):
        # Asynchronize data structure to manage concurent call
        # thread safe FIFO
        self.queue = Queue()

        # Alert text view
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.add(self.textview)

        self.textbuffer.create_tag("alert",
                        weight=Pango.Weight.BOLD,
                        foreground='red',
                        left_margin=10)
        self.textbuffer.create_tag("recover",
                        weight=Pango.Weight.BOLD,
                        foreground='green',
                        left_margin=10)
        self.textbuffer.create_tag("info",
                        weight=Pango.Weight.BOLD,
                        foreground='#127cc1',
                        left_margin=10)

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.scrolledwindow, True, True, 0)

    def get_top_level_widget(self):
        return self.vbox

    def print_message(self, type, message):
        self.queue.put((type, message+'\n'))
        while not self.queue.empty():
            type, message = self.queue.get()
            self._print(type, message)

    def _print(self, type, message):
        if type=='alert':
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message, 'alert')
        elif type=='recover':
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message, 'recover')
        else:
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message, 'info')


def start_interface(interface):
    interface.connect("destroy", Gtk.main_quit)
    interface.show_all()
    Gtk.main()


if __name__ == '__main__':
    client_interface = Interface()
    start_interface(client_interface)
