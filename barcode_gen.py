import os
import barcode
from barcode import Code128
from PIL import Image, ImageDraw, ImageFont


class Barcode128():
    def __init__(self, data, text="", bcsize=(320, 200), font_num="NotoSansMono_ExtraCondensed-Regular.ttf", font_num_size=1.0, font_txt="Roboto-Medium.ttf", font_txt_size=1.0, borders=20, saved=False):
        self.saved = saved
        self.filename = f'temp\\{data}.tiff'
        code128 = Code128(data)
        barcode_data = code128.build()

        print(barcode_data[0], len(barcode_data[0]))

        width = bcsize[0]-borders*2
        height = bcsize[1]//2-borders

        # генерируэм штрихкод
        # '1' означает 1-битное изображение, аргумент (width, height) - размер изображения, 1 - начальное значение всех пикселей
        self.img = Image.new('1', (width, height), color=1)
        draw = ImageDraw.Draw(self.img)
        bar_width = width / len(barcode_data[0])
        x = 0
        for ln in barcode_data[0]:
            # print(ln)
            upper_left = (bar_width*x, 0)
            lower_right = (bar_width*(x+1), height)
            if ln == "1":
                draw.rectangle([upper_left, lower_right], fill=0)
            elif ln == "0":
                draw.rectangle([upper_left, lower_right], fill=1)
            x += 1

        # генерируем подписи #######################################################
        self.barcodeimg = Image.new('1', bcsize, color=1)
        draw = ImageDraw.Draw(self.barcodeimg)
        # НОМЕР
        font = ImageFont.truetype(font_num, bcsize[0]//8*font_num_size)
        textbbox = draw.textbbox((0, 0), data, font=font)
        text_position = ((bcsize[0] - textbbox[2]) //
                         2, bcsize[1] // 2)
        text_color = 0  # Черный цвет текста (0)
        draw.text(text_position, data, fill=text_color, font=font)
        # НАЗВА
        font = ImageFont.truetype(font_txt, bcsize[0]//16*font_txt_size)
        textbbox = draw.textbbox((0, 0), text, font=font)
        text_position = (
            (bcsize[0] - textbbox[2]) // 2, bcsize[1] - textbbox[3] - borders)
        text_color = 0  # Черный цвет текста (0)
        draw.text(text_position, text, fill=text_color, font=font)
        # ШТРИХКОД
        self.barcodeimg.paste(self.img, (borders, borders))

        # Сохраняем
    def save(self, filename=None):
        if filename:
            self.filename = filename
        self.barcodeimg.save(self.filename)

        # Удаляем деструктором класса
    def __del__(self):
        if self.saved:
            return
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            print('Файл відсутній')
            pass


if __name__ == "__main__":
    data = '123456789'
    bc = Barcode128(data, text="sdfsdafasdf asdf ", saved=True)
    bc.save()
