import win32print
import win32ui
from PIL import Image


class Printes():
    def __init__(self, printer_patern=""):
        self.selected_printer = None
        self.printer_patern = printer_patern
        self.printers = []
        self.get_printers()
        self.find_printer()

    def get_printers(self):
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
            self.printers.append(printer[2])

    def find_printer(self):
        self.finded = []
        for printer in self.printers:
            if self.printer_patern.lower() in printer.lower():
                print('==', printer)
                self.finded.append(printer)
        if len(self.finded) == 1:
            self.selected_printer = str(self.finded[0])


if __name__ == "__main__":
    myprn = Printes('Xprinter XP-420B')
    print(myprn.selected_printer)
    print(myprn.finded)
