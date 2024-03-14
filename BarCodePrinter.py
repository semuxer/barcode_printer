import wx
from os import path
from multiprocessing import freeze_support

from myconfig import Config
from printer import Printes
from serverv2 import BGServer
from defaults import bundle_dir


class MyWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MyWindow, self).__init__(parent, title=title, size=(640, 580))
        self.SetIcon(wx.Icon(path.join(bundle_dir, 'Icon19.ico'), wx.BITMAP_TYPE_ICO))

        self.myserv = BGServer()

        self.config = Config()
        self.printer_patern = ""
        self.selected_printer = ""
        self.finded_printer = []
        self.set_printers()

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        ######################################################################
        self.static_text00 = wx.StaticText(
            self.panel, label=f"Обрано принтер: {self.selected_printer}")
        vbox.Add(self.static_text00, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)

        self.static_text1 = wx.StaticText(
            self.panel, label="Патерн пошуку принтера:")
        vbox.Add(self.static_text1, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.text_ctrl = wx.TextCtrl(self.panel, size=(300, -1))
        self.text_ctrl.SetValue(self.printer_patern)
        vbox.Add(self.text_ctrl, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.text_ctrl.Bind(wx.EVT_TEXT, self.on_patern_change)
        self.static_text2 = wx.StaticText(
            self.panel, label="Принтери що відповідають патерну:")
        vbox.Add(self.static_text2, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.listbox = wx.ListBox(
            self.panel, choices=self.finded_printer, size=(300, 200))
        vbox.Add(self.listbox, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.static_line = wx.StaticLine(
            self.panel, wx.ID_ANY, size=(640, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(self.static_line, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)

        ######################################################################
        self.text_ctrl_server = wx.TextCtrl(self.panel, size=(640, 200), style=wx.TE_MULTILINE)
        vbox.Add(self.text_ctrl_server, 0, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.btn_server = wx.Button(self.panel, label='Перезапустити сервер')
        self.btn_server.Bind(wx.EVT_BUTTON, self.restart_server)
        vbox.Add(self.btn_server, 0, wx.ALL, 5)
        ######################################################################
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_timer, self.timer)
        # Запускаем таймер с интервалом в 1000 миллисекунд (1 секунда)
        self.timer.Start(200)
        ######################################################################
        self.Bind(wx.EVT_CLOSE, self.on_close)
        ######################################################################
        self.panel.SetSizer(vbox)
        self.Center()
        self.Show()

    def on_close(self, event):
        self.myserv.stop_server()
        event.Skip()  # Пропускаем событие закрытия окна для завершения процесса закрытия

    def restart_server(self, event):
        self.myserv.stop_server()
        self.myserv = BGServer()

    def update_timer(self, event):
        ret = self.myserv.get_queue()
        if ret:
            self.text_ctrl_server.AppendText(ret)

    def on_patern_change(self, event):
        self.set_printers(self.text_ctrl.GetValue())
        self.listbox.SetItems(self.finded_printer)
        if self.selected_printer:
            message = f"Обрано принтер: {self.selected_printer}"
        else:
            message = "Змініть патерн так, щоб в списку залишився один принтер."
        self.static_text00.SetLabel(message)
        self.config.set('printer_patern', self.printer_patern)

    def set_printers(self, printer_patern=None):
        if printer_patern is None:
            self.printer_patern = self.config.data.get('printer_patern')
        else:
            self.printer_patern = printer_patern

        myprn = Printes(self.printer_patern)
        self.selected_printer = myprn.selected_printer
        self.finded_printer = myprn.finded
        self.config.set('selected_printer', self.selected_printer)


freeze_support()
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyWindow(None, "BarCodePrinter")
    app.MainLoop()
