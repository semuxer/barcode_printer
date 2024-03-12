from PIL import Image, ImageWin
import win32print
import win32ui

def print_tiff_file(file_path, printer_name):
    # Открываем файл TIFF
    image = Image.open(file_path)
    if image.mode != "1":
        image = image.convert("1")

    # Получаем хэндл принтера
    printer_handle = win32print.OpenPrinter(printer_name)
    # Создаем объект DC для принтера
    printer_dc = win32ui.CreateDC()
    printer_dc.CreatePrinterDC(printer_name)

    # Устанавливаем параметры печати
    printer_dc.StartDoc('Print TIFF File')
    printer_dc.StartPage()

    # Отображаем изображение на контексте устройства принтера
    dib = ImageWin.Dib(image)
    dib.draw(printer_dc.GetHandleOutput(), (0, 0, image.width, image.height))

    # Завершаем печать
    printer_dc.EndPage()
    printer_dc.EndDoc()

    # Закрываем принтер
    win32print.ClosePrinter(printer_handle)

if __name__ == "__main__":
    # Путь к файлу TIFF
    tiff_file_path = "temp\\123456789.tiff"
    # Имя принтера
    printer_name = "Xprinter XP-420B"

    print_tiff_file(tiff_file_path, printer_name)
