# barcode_printer


Main script - **BarCodePrinter.py**

Before use, edit the configuration file **config.json**
```python
{
  "addr": "localhost", # Host address
  "port": 9000, # Host port
  "printer_patern": "Xprinter", # Patern name (use filter and select one printer if you have many printers)
  "label_size": [40, 25], # Label size in mm
  "printer_dpi": 203, # Printer resolution
  "selected_printer": "Xprinter XP-420B" # Selected printer (generated automatically based on printer_patern)
}
```

Example request for generating a label:
```http://127.0.0.1:9000/?txt1=123456789&txt2=sample_text```


Author: **Sergey Movchan**, 2024
