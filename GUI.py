import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango, Gdk


class Interface(Gtk.Window):
    def __init__(self, **kwargs):
        # Window
        Gtk.Window.__init__(self, **kwargs)
        self.set_default_size(1100, 350)
        self.set_border_width(10)

        # HeaderBar
        self.spinner = Gtk.Spinner()

        self.monitor_button = Gtk.ToggleButton(label="Start monitoring...")
        self.monitor_button.connect("toggled", self.on_monitor_button_toggled)
        self.monitor_button.set_active(False)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = 'Web Monitor'
        self.headerbar.props.subtitle = 'DataDog take home project - Martin GUYARD'
        self.headerbar.pack_start(self.spinner)
        self.headerbar.pack_start(Gtk.Separator())
        self.headerbar.pack_start(self.monitor_button)
        self.set_titlebar(self.headerbar)

        # MainFrame
        self.main_frame = MainFrame()

        # Pack
        self.add(self.main_frame.get_top_level_widget())
        # self.show_all()

    def on_monitor_button_toggled(self, button):
        if button.get_active():
            self.spinner.start()
            self.send_message('info', 'Start monitoring...')
            self.start_monitoring()
            self.monitor_button.set_label("Stop monitoring.")
        else:
            self.spinner.stop()
            self.send_message('info', 'Stop monitoring...')
            self.stop_monitoring()
            self.monitor_button.set_label("Start monitoring...")


    def update_monitoring(self, metrics, mon):
        if mon=='10min':
            self.main_frame.mon_10min.update_liststore(metrics)
        elif mon=='1hour':
            self.main_frame.mon_1h.update_liststore(metrics)

    def send_message(self, type, message):
        self.main_frame.alert.print_message(type, message)

    @staticmethod
    def start_monitoring():
        # override with MonitorMaster.start_monitoring
        pass

    @staticmethod
    def stop_monitoring():
        # override with MonitorMaster.stop_monitoring
        pass


class MainFrame:
    def __init__(self):
        # 10 minutes look back monitor
        self.mon_10min = Monitor(title='10 minutes look back')

        # 1h look back monitor
        self.mon_1h = Monitor(title='1 hour look back')

        # alert box
        self.alert = AlertBox()

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.mon_10min.get_top_level_widget(), True, True, 0)
        self.vbox.pack_start(self.mon_1h.get_top_level_widget(), True, True, 0)
        self.vbox.pack_start(self.alert.get_top_level_widget(), True, True, 0)

    def get_top_level_widget(self):
        return self.vbox


class Monitor:
    def __init__(self, title):
        # MonitorLabel
        self.mon_label = Gtk.Label()
        self.mon_label.set_markup('<b>'+title+'</b>')

        # MonitorTreeview
        columns = ['Website', 'Avg response time', 'Max response time',
                   'Most occurent status code', 'Average size (byte)',
                   'Max size (byte)', 'Content type']
        self.mon_liststore = Gtk.ListStore(str, str, str, str, str, str, str, str)
        self.mon_treeview =  Gtk.TreeView.new_with_model(self.mon_liststore)

        # self.renderer_availability = Gtk.CellRendererProgress()
        # column_availability = Gtk.TreeViewColumn('Availability', self.renderer_availability)
        # self.mon_treeview.append_column(column_availability)

        for i, column_title in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.mon_treeview.append_column(column)


        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(self.mon_treeview)

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.mon_label, False, True, 0)
        self.vbox.pack_start(self.scrollable_treelist, True, True, 0)

    def get_top_level_widget(self):
        self.update_liststore([('100', 'https://google.com', '1s', '2s', '200', '1kb', '2kb', 'text')])
        self.update_liststore([('75', 'https://facebook.com', '1s', '2s', '200', '1kb', '2kb', 'text')])
        return self.vbox

    def update_liststore(self, metrics):
        self.mon_liststore.clear()
        for metric in metrics:
            self.mon_liststore.append(list(metric))


class AlertBox:
    def __init__(self):
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
                        foreground='yellow',
                        left_margin=10)

        # Pack
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.scrolledwindow, True, True, 0)

    def get_top_level_widget(self):
        return self.vbox

    def print_message(self, type, message):
        if type=='alert':
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message+'\n', 'alert')
        elif type=='recover':
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message+'\n', 'recover')
        else:
            self.textbuffer.insert_with_tags_by_name(
                self.textbuffer.get_end_iter(), message+'\n', 'info')


def start_interface(interface):
    interface.connect("destroy", Gtk.main_quit)
    interface.show_all()
    Gtk.main()


if __name__ == '__main__':
    client_interface = Interface()
    start_interface(client_interface)
