import json
from os import path


from defaults import CONFIGNAME, bundle_dir


class Config():
    def __init__(self, confname=CONFIGNAME):
        self.confname = confname
        try:
            with open(path.join(bundle_dir, self.confname), 'r', encoding="utf-8") as f:
                self.data = json.load(f)

        except:
            self.data = {
                "addr": "localhost",
                "port": 9000,
                "printer_patern": "Xprinter XP-360B",
                "selected_printer": "",
                "label_size": [40, 25],
                "printer_dpi": 203
            }

            # Запись в файл JSON
            self.save()

    def set(self, key, value):
        self.data[key]=value
        self.save()

    def save(self):
        print('save config')
        with open(path.join(bundle_dir, self.confname), 'w', encoding="utf-8") as f:
            json.dump(self.data, f)

if __name__ == "__main__":
    config = Config()
    print(config.data)
