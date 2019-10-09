# chip40000-python

[Qt's 40000 Chip example](https://doc.qt.io/qt-5/qtwidgets-graphicsview-chip-example.html)
port to [Qt for Python](https://pyside.org) (Pyside2).

The goal of this port is to test performance between both implementations.

## Usage

1. Generate `images` resource: `pyside2-rcc images.qrc -o rc_images.py`

### Notes

* Be careful, the statement `import rc_images` might be removed after "Optimize" by an "IDE"
* If the chip background color is all same, please check if you properly generated
  the file `images.py`.

## How to run it

`python main.py`

