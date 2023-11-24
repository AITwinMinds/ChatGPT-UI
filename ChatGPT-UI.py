import os
import sys
import json
import re
import httpx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QRadioButton, QCheckBox,
    QTextEdit, QLabel, QComboBox
)
from PyQt5.QtGui import QPalette, QColor, QFont, QPixmap, QIcon
import openai
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ICON_DATA = b'\x00\x00\x01\x00\x01\x00  \x00\x00\x01\x00 \x00\xa8\x10\x00\x00\x16\x00\x00\x00(\x00\x00\x00 \x00\x00\x00@\x00\x00\x00\x01\x00 \x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n\x0c3\x00m\x105\x04p\t3*q\x072nr\x071\xafr\x061\xdcs\x050\xf5s\x040\xfes\x040\xfes\x051\xf5s\x061\xddr\x071\xb0q\x071np\t2+m\x105\x04o\x0c4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n\x0e5\x00m\x127\x03q\t28r\x060\x99s\x040\xe0t\x041\xfcv\x042\xffw\x042\xffx\x042\xffy\x043\xffy\x043\xffx\x042\xffw\x042\xffv\x042\xfft\x041\xfcs\x040\xe0q\x060\x9aq\t28n\x126\x04o\r4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00u\x1c>\x00o\x03.\x00p\n3\x1aq\x061\x8bs\x050\xebv\x041\xffx\x042\xff{\x044\xff|\x044\xff}\x045\xff\x7f\x045\xff\x7f\x045\xff\x7f\x045\xff\x7f\x045\xff}\x045\xff|\x044\xff{\x044\xffx\x042\xffv\x041\xffs\x050\xebq\x060\x8bp\x0b3\x1bo\x02-\x00u#C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00o\x116\x00w\x00+\x00p\x0826r\x050\xc3u\x041\xfex\x043\xff{\x044\xff~\x045\xff\x80\x046\xff\x82\x046\xff\x83\x047\xff\x84\x047\xff\x83\x037\xff\x82\x026\xff\x82\x025\xff\x82\x036\xff\x81\x036\xff\x80\x046\xff~\x045\xff{\x044\xffx\x043\xffu\x041\xfer\x050\xc4p\x0827x\x00)\x00o\x126\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n\x114\x00t\x00,\x00q\x081Ar\x050\xd9v\x041\xffz\x043\xff}\x044\xff\x80\x046\xff\x83\x047\xff\x85\x047\xff\x87\x048\xff\x86\x027\xff\x7f\x001\xffw\x01.\xfft\x062\xfft\x072\xffu\x02.\xffz\x00/\xff\x81\x015\xff\x83\x037\xff\x81\x046\xff}\x045\xffz\x043\xffv\x041\xffr\x050\xdap\x082Bs\x00*\x00o\x126\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00s\x1b=\x00p\x03.\x00p\x0816r\x050\xd9v\x042\xff{\x044\xff\x7f\x045\xff\x82\x036\xff\x84\x027\xff\x83\x015\xff\x83\x004\xff\x82\x003\xffy\x020\xff|,O\xff\x90p\x86\xff\x9c\x94\xa4\xff\x9d\x96\xa7\xff\x93|\x90\xff~>\\\xfft\x082\xff\x7f\x003\xff\x85\x027\xff\x82\x046\xff~\x045\xff{\x044\xffv\x042\xffr\x050\xd9p\x0817p\x04/\x00t\x19;\x00\x00\x00\x00\x00\x00\x00\x00\x00p\t2\x00p\n2\x1ar\x050\xc1v\x041\xff{\x044\xff\x7f\x045\xff\x82\x026\xff~\x002\xffv\x02/\xffv\x12:\xff{$I\xffy#G\xff\x8a\\v\xff\xab\xb6\xc3\xff\xa7\xab\xb9\xff\x99\x82\x97\xff\x97|\x91\xff\xa2\x9e\xae\xff\xac\xbc\xc7\xff\x92y\x8e\xffv\x108\xff\x82\x004\xff\x86\x038\xff\x83\x047\xff\x7f\x045\xff{\x044\xffv\x042\xffr\x051\xc2o\n3\x1bp\t2\x00\x00\x00\x00\x00p\x0f5\x00k\x1c;\x02q\x060\x89u\x041\xffz\x043\xff\x7f\x045\xff\x82\x026\xffz\x000\xffu\x17=\xff\x8dj\x81\xff\xa5\xa8\xb6\xff\xac\xb9\xc5\xff\xae\xbb\xc8\xff\xb7\xce\xd8\xff\xab\xb2\xc0\xff{0P\xfft\x00+\xff|\x00/\xff{\x0c8\xff\x8bUq\xff\xae\xbc\xc8\xff\x91r\x88\xffw\x040\xff\x86\x017\xff\x87\x048\xff\x83\x047\xff\x7f\x045\xffz\x043\xffu\x041\xffq\x060\x8aj\x1a;\x02o\x0e5\x00q\x071\x00p\t27s\x050\xe9x\x043\xff}\x045\xff\x82\x036\xff|\x001\xffv\x1eB\xff\x9d\x98\xa8\xff\xaa\xb5\xc2\xff\x94s\x8a\xff\x88Gg\xff\x8aKj\xff\x9c~\x95\xff\xb5\xc0\xcd\xff\xaf\xaf\xbf\xff\x8fRp\xff\x80\x0c9\xff\x85\x002\xff}\x01/\xff\x8fb|\xff\xae\xbd\xc9\xff~9X\xffw\x02/\xff\x80\x002\xff\x85\x027\xff\x82\x046\xff}\x045\xffx\x043\xffs\x050\xe9p\t28q\x061\x00h\x1a9\x02q\x060\x96v\x041\xff{\x044\xff\x81\x046\xff\x82\x015\xfft\x082\xff\x96\x84\x97\xff\xa8\xad\xbb\xff\x802T\xff~\x010\xff\x81\x00/\xff}\x00,\xff{\x02.\xff\x870U\xff\xa8\x94\xa8\xff\xbe\xcf\xdb\xff\xab\x9e\xb1\xff\x8b9]\xff\x82\x023\xff\x7f\x1bC\xff\xae\xb5\xc3\xff\xae\xbb\xc7\xff\x96\x7f\x93\xffz&I\xffy\x00/\xff\x83\x016\xff\x81\x046\xff|\x044\xffv\x041\xffq\x060\x97f\x18:\x03p\t2)s\x050\xdex\x043\xff~\x045\xff\x83\x047\xff}\x001\xff|2R\xff\xac\xba\xc6\xff\x88Ok\xff}\x00-\xff\x82\x012\xff\x86%M\xff\x9et\x8d\xff\x94Pq\xff\x7f\t5\xff\x7f\x074\xff\x92Jl\xff\xb4\xb0\xc1\xff\xbd\xca\xd7\xff\x8c9^\xff|\x084\xff\xaa\xa5\xb6\xff\xab\xb0\xbe\xff\xa7\xac\xba\xff\xa6\xab\xb9\xff{1Q\xffz\x00/\xff\x82\x036\xff~\x045\xffx\x043\xffs\x050\xdep\t2*q\x071jt\x041\xfbz\x044\xff\x80\x055\xff\x85\x048\xffz\x00/\xff\x8a\\v\xff\xaa\xb1\xbe\xffw\x19=\xff}\x12<\xff\x97f\x81\xff\xb9\xc2\xd0\xff\xbb\xc4\xd1\xff\xb3\xad\xbe\xff\xad\x97\xad\xff\x8f6]\xff\x81\x020\xff\x81\x14>\xff\xaf\xa5\xb7\xff\x95Rr\xff}\x063\xff\xae\xa7\xb8\xff\x9b~\x93\xffw\x1fC\xff\xa2\x9d\xad\xff\x9f\x9b\xab\xfft\x129\xff\x7f\x003\xff\x80\x046\xff{\x043\xffu\x041\xfbq\x071kr\x061\xaav\x041\xff|\x044\xff\x82\x046\xff\x86\x048\xff{\x00/\xff\x8fh\x80\xff\xa9\xaf\xbd\xff\x8aWr\xff\xae\xaa\xbb\xff\xbd\xcc\xd8\xff\xa4\x83\x9b\xff\x87"K\xff\x80\x10<\xff\xa6\x86\x9e\xff\xc6\xd6\xe4\xff\xaa\x85\x9f\xff\x86#K\xff\xa9\x91\xa6\xff\x97St\xff\x7f\x064\xff\xb0\xaa\xbb\xff\x9f\x80\x97\xffx\x00*\xff\x816W\xff\xab\xb9\xc5\xff\x81Ie\xffy\x00/\xff\x81\x046\xff|\x044\xffv\x041\xffr\x061\xabr\x061\xd7x\x042\xff}\x045\xff\x83\x047\xff\x88\x048\xff|\x00/\xff\x87Sm\xff\xb6\xcc\xd6\xff\xb8\xca\xd6\xff\xa9\x9a\xad\xff\x8b8\\\xff\x7f\x030\xff\x85\x10=\xff\x9fe\x84\xff\xb9\xb3\xc6\xff\xab\x87\xa0\xff\xab\x87\xa1\xff\xba\xb5\xc8\xff\xc1\xca\xd9\xff\x98Rs\xff\x81\x065\xff\xb2\xac\xbd\xff\xa1\x82\x99\xff\x80\x000\xff{\x0c7\xff\xa2\x9f\xaf\xff\x91t\x8a\xffv\x00.\xff\x82\x036\xff}\x045\xffw\x042\xffr\x050\xd9s\x050\xf0x\x042\xff~\x045\xff\x84\x047\xff\x86\x017\xffw\x052\xff\x95{\x90\xff\xb2\xc0\xcc\xff\x90Wt\xff}\n5\xff\x7f\x063\xff\x94Jl\xff\xb9\xb2\xc5\xff\xbe\xbd\xcf\xff\x95;b\xff\x91\x039\xff\x91\x039\xff\x95:b\xff\xbe\xbf\xd0\xff\x99Su\xff\x81\x054\xff\xb3\xad\xbe\xff\xa3\x83\x9a\xff\x83\x002\xff}\x064\xff\x9f\x96\xa7\xff\x95~\x92\xffv\x00.\xff\x83\x036\xff~\x045\xffx\x042\xffs\x050\xf2s\x051\xfcy\x043\xff\x7f\x045\xff\x84\x047\xff\x7f\x002\xff~3T\xff\xae\xbd\xc9\xff\x8f]x\xff|\x00-\xff\x87$L\xff\xa9\x90\xa5\xff\xb2\xa7\xba\xff\xae\x9b\xb0\xff\xb0\x95\xac\xff\x90\x017\xff\xab\x02F\xff\xab\x02F\xff\x90\x017\xff\xaf\x96\xac\xff\x97Ut\xff\x83\x1cE\xff\xb9\xbd\xcc\xff\xa1{\x94\xff\x81\x000\xff}\x17?\xff\xa8\xae\xbc\xff\x8dg\x7f\xffy\x00.\xff\x84\x037\xff\x7f\x045\xffy\x043\xffs\x050\xfds\x051\xfby\x043\xff\x7f\x045\xff\x84\x037\xffx\x00.\xff\x8dg\x7f\xff\xa9\xae\xbc\xff}\x17?\xff\x81\x000\xff\xa1}\x95\xff\xb9\xbc\xcb\xff\x82\x19C\xff\x97Ut\xff\xb0\x96\xac\xff\x8f\x017\xff\xab\x02F\xff\xab\x02F\xff\x90\x017\xff\xaf\x95\xac\xff\xb0\xa0\xb5\xff\xb3\xaa\xbc\xff\xa7\x8a\xa1\xff\x86!J\xff|\x00.\xff\x8f_z\xff\xae\xbc\xc8\xff}1R\xff\x7f\x002\xff\x84\x047\xff\x7f\x045\xffy\x043\xffs\x050\xfds\x050\xf0x\x042\xff\x7f\x055\xff\x83\x037\xffv\x00/\xff\x94~\x92\xff\xa0\x98\xa9\xff}\x075\xff\x82\x002\xff\xa2\x83\x9a\xff\xb4\xad\xbf\xff\x81\x065\xff\x99Su\xff\xbf\xc2\xd3\xff\x97Ah\xff\x90\x04:\xff\x90\x04:\xff\x97@g\xff\xbe\xbf\xd0\xff\xb7\xad\xc1\xff\x93Dh\xff\x7f\x051\xff~\x0c7\xff\x91\\x\xff\xb2\xc2\xce\xff\x94y\x8e\xffw\x041\xff\x86\x017\xff\x84\x047\xff~\x045\xffx\x042\xffs\x050\xf1r\x061\xd6x\x042\xff~\x045\xff\x82\x036\xffv\x00.\xff\x90r\x88\xff\xa3\xa2\xb1\xff{\x0e9\xff\x80\x000\xff\xa1\x82\x98\xff\xb3\xac\xbe\xff\x81\x065\xff\x98Rs\xff\xc0\xc7\xd6\xff\xb9\xb4\xc6\xff\xae\x8f\xa7\xff\xad\x8e\xa6\xff\xb9\xb2\xc5\xff\x9c_\x7f\xff\x84\x0e;\xff\x80\x041\xff\x8d=`\xff\xab\x9f\xb2\xff\xb8\xca\xd5\xff\xb6\xcb\xd6\xff\x88Uo\xff|\x00/\xff\x88\x048\xff\x83\x047\xff}\x045\xffw\x042\xffr\x061\xd8r\x071\xa9v\x041\xff|\x044\xff\x82\x046\xffz\x00/\xff\x80Eb\xff\xac\xba\xc6\xff\x82:Z\xffw\x00*\xff\x9f\x80\x97\xff\xb1\xaa\xbc\xff\x7f\x065\xff\x97Rt\xff\xaa\x91\xa6\xff\x85\x1eG\xff\xa7~\x99\xff\xc6\xd3\xe1\xff\xa7\x8a\xa1\xff\x81\x14?\xff\x88\'O\xff\xa6\x8a\xa0\xff\xbd\xcd\xd9\xff\xac\xa6\xb7\xff\x87Qm\xff\xa8\xae\xbc\xff\x8fj\x81\xff{\x00/\xff\x86\x048\xff\x82\x046\xff|\x044\xffv\x041\xffr\x071\xaar\x082hu\x041\xfaz\x044\xff\x80\x046\xff\x80\x004\xfft\x107\xff\x9d\x97\xa7\xff\xa4\xa2\xb2\xffy$G\xff\x9a~\x94\xff\xae\xa7\xb9\xff}\x064\xff\x95Qr\xff\xb1\xa8\xba\xff\x83\x18B\xff\x80\x01/\xff\x8d0W\xff\xab\x92\xa8\xff\xb4\xb0\xc1\xff\xbc\xc7\xd4\xff\xb8\xbf\xcd\xff\x95`|\xff|\x0f9\xffw\x19=\xff\xaa\xb1\xbf\xff\x89\\v\xffz\x00/\xff\x85\x037\xff\x80\x046\xff{\x044\xffu\x041\xfbr\x082iq\x0b3\'s\x050\xdcx\x043\xff~\x045\xff\x82\x036\xffz\x000\xffz,M\xff\xa5\xa7\xb6\xff\xa9\xb0\xbe\xff\xac\xb4\xc1\xff\xab\xa5\xb7\xff}\x085\xff\x8c6[\xff\xbc\xc8\xd4\xff\xb6\xb6\xc6\xff\x95Rr\xff\x80\t6\xff\x7f\x063\xff\x92Ij\xff\x9cl\x88\xff\x85!J\xff\x83\x001\xff}\x00-\xff\x89Qm\xff\xac\xba\xc6\xff{1Q\xff}\x001\xff\x83\x047\xff~\x045\xffx\x043\xffs\x051\xddq\x0b3(m+E\x02r\x061\x93v\x041\xff{\x044\xff\x80\x046\xff\x83\x026\xffz\x000\xffy!E\xff\x94x\x8d\xff\xac\xb7\xc4\xff\xaf\xb7\xc5\xff\x7f\x1eE\xff\x82\x013\xff\x893X\xff\xa9\x97\xab\xff\xbe\xcf\xdb\xff\xab\x9b\xaf\xff\x897Z\xff{\x03/\xff}\x00,\xff\x81\x00.\xff}\x021\xff\x827X\xff\xa9\xb0\xbd\xff\x95\x81\x94\xfft\x072\xff\x82\x015\xff\x80\x046\xff{\x044\xffv\x041\xffr\x061\x95m%B\x02q\x082\x00r\x0b44s\x051\xe7x\x043\xff}\x045\xff\x82\x046\xff\x85\x027\xff\x81\x003\xffw\x01.\xff}4T\xff\xae\xbb\xc7\xff\x91g\x80\xff}\x020\xff\x85\x002\xff\x80\t7\xff\x8dJj\xff\xad\xa9\xb9\xff\xb6\xc2\xcf\xff\x9f\x86\x9b\xff\x8dRp\xff\x8aNl\xff\x96z\x90\xff\xab\xb7\xc4\xff\x9c\x94\xa4\xffu\x1c@\xff|\x001\xff\x82\x036\xff}\x045\xffx\x043\xffs\x051\xe8r\x0b46q\x082\x00s\x13:\x00r/L\x01r\x071\x85u\x041\xffz\x043\xff\x7f\x045\xff\x83\x047\xff\x87\x048\xff\x87\x017\xffx\x030\xff\x90m\x84\xff\xaf\xbd\xc9\xff\x8d\\v\xff{\x10:\xff|\x010\xfft\x01,\xff{0P\xff\xab\xb1\xbf\xff\xb6\xcc\xd7\xff\xad\xb9\xc6\xff\xab\xb7\xc4\xff\xa3\xa4\xb2\xff\x8bd|\xfft\x15;\xff{\x000\xff\x82\x026\xff\x7f\x045\xffz\x043\xffu\x041\xffr\x071\x86r,I\x02s\x14:\x00\x00\x00\x00\x00q\x0b4\x00q\r5\x18s\x061\xbdv\x041\xff{\x044\xff\x7f\x045\xff\x83\x047\xff\x86\x048\xff\x82\x004\xffv\r6\xff\x90r\x88\xff\xac\xbb\xc6\xff\xa4\xa4\xb3\xff\x99\x83\x98\xff\x9b\x89\x9d\xff\xa9\xaf\xbd\xff\xaa\xb3\xc1\xff\x88Wq\xffx\x1fC\xffz E\xffv\x0f8\xffw\x01.\xff\x7f\x003\xff\x82\x026\xff\x7f\x045\xff{\x044\xffv\x041\xffr\x061\xbfr\r5\x19r\x0b4\x00\x00\x00\x00\x00\x00\x00\x00\x00~\'J\x00p\x04/\x00r\n32s\x051\xd5v\x042\xff{\x044\xff\x7f\x045\xff\x82\x046\xff\x85\x037\xff\x80\x003\xffu\x061\xff}7W\xff\x90t\x8a\xff\x9b\x91\xa2\xff\x9a\x8e\x9f\xff\x8di\x80\xff{\'K\xffy\x020\xff\x83\x003\xff\x84\x004\xff\x84\x016\xff\x84\x037\xff\x82\x046\xff\x7f\x045\xff{\x044\xffv\x041\xffs\x050\xd6q\n33p\x03.\x00~/L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00q\x19;\x00r\x00+\x00r\n4=s\x050\xd5v\x041\xffz\x043\xff}\x045\xff\x80\x046\xff\x83\x037\xff\x82\x015\xff{\x000\xffu\x01.\xfft\x051\xffu\x040\xffx\x00.\xff\x7f\x002\xff\x86\x028\xff\x87\x048\xff\x85\x048\xff\x83\x047\xff\x81\x046\xff}\x045\xffz\x043\xffv\x041\xffs\x050\xd6r\n3>q\x00*\x00r\x17;\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x1a;\x00t\x00*\x00r\x0b31s\x061\xbeu\x041\xfex\x042\xff{\x044\xff~\x045\xff\x80\x046\xff\x82\x036\xff\x82\x036\xff\x82\x036\xff\x83\x026\xff\x83\x037\xff\x84\x047\xff\x83\x047\xff\x82\x046\xff\x80\x045\xff~\x045\xff{\x044\xffx\x042\xffu\x041\xfer\x061\xbeq\n32s\x00+\x00q\x17;\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|-L\x00p\x05/\x00r\r5\x17r\x072\x84s\x051\xe7v\x041\xffx\x042\xff{\x044\xff|\x044\xff}\x045\xff\x7f\x045\xff\x7f\x045\xff\x7f\x045\xff\x7f\x045\xff}\x045\xff|\x044\xff{\x044\xffx\x042\xffv\x041\xffs\x051\xe8r\x072\x84q\r5\x17p\x04/\x00{+K\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00t\x14:\x00u\x1c?\x03r\x0b42r\x071\x91s\x051\xdbt\x041\xfav\x042\xffw\x042\xffx\x042\xffy\x043\xffy\x043\xffx\x042\xffw\x042\xffv\x041\xfft\x041\xfas\x051\xdcr\x071\x92r\x0b43t\x1b>\x03s\x149\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x116\x00o\x168\x03q\x0c4%r\t3fr\x071\xa6s\x061\xd4s\x051\xeds\x050\xf9s\x050\xf9s\x051\xees\x061\xd4r\x072\xa6r\t3fq\x0c4%p\x158\x03q\x117\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x80\x01\xff\xfe\x00\x00\x7f\xfc\x00\x00?\xf8\x00\x00\x1f\xf0\x00\x00\x0f\xe0\x00\x00\x07\xc0\x00\x00\x03\x80\x00\x00\x01\x80\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x01\x80\x00\x00\x01\xc0\x00\x00\x03\xe0\x00\x00\x07\xf0\x00\x00\x0f\xf8\x00\x00\x1f\xfc\x00\x00?\xfe\x00\x00\x7f\xff\x80\x01\xff'

class GPTUI(QWidget):
    CONFIG_FILE_PATH = "config.json"

    def __init__(self):
        super().__init__()

        self.client = None
        self.api_key_fixed = False
        self.stop_generation = False

        self.init_ui()

        self.load_config_from_file()

    def init_ui(self):
        self.setWindowTitle('ChatGPT')
        self.setGeometry(100, 100, 800, 600)

        icon_path = os.path.join(os.path.dirname(sys.executable), "icon.ico")
        if not os.path.exists(icon_path):
            with open(icon_path, "wb") as icon_file:
                icon_file.write(ICON_DATA)

        self.setWindowIcon(QIcon(icon_path))

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(26, 29, 33))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(8, 68, 49))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(26, 82, 118))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(dark_palette)

        layout = QVBoxLayout()

        scrollbar_stylesheet = """
        QScrollBar:vertical {
            border: 1px solid #041b20;
            background: #222529;
            width: 15px;
            margin: 5px 0 5px 0;
        }

        QScrollBar::handle:vertical {
            background: #0b4654;
            min-height: 30px;  /* Adjust min-height for the handle */
            max-height: 30px;  /* Adjust max-height for the handle */
        }

        QScrollBar::add-line:vertical {
            border: 1px solid #041b20;
            background: #073a43;  /* Change color for the add-line (down arrow) */
            height: 5px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            border: 1px solid #041b20;
            background: #073a43;  /* Change color for the sub-line (up arrow) */
            height: 5px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar:horizontal {
            border: 1px solid #041b20;
            background: #222529;
            height: 15px;
            margin: 0 5px 0 5px;
        }

        QScrollBar::handle:horizontal {
            background: #0b4654;
            min-width: 30px;  /* Adjust min-width for the handle */
            max-width: 30px;  /* Adjust max-width for the handle */
        }

        QScrollBar::add-line:horizontal {
            border: 1px solid #041b20;
            background: #073a43;  /* Change color for the add-line (right arrow) */
            width: 5px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:horizontal {
            border: 1px solid #041b20;
            background: #073a43;  /* Change color for the sub-line (left arrow) */
            width: 5px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        """

        input_layout = QHBoxLayout()

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText('Enter API key...')
        self.api_key_input.setFixedHeight(26)
        self.api_key_input.setStyleSheet("QLineEdit { background-color: #222529; color: white; font-size: 11pt; border: 1px solid #565856; border-radius: 2px;}")
        input_layout.addWidget(self.api_key_input)
        self.fix_api_key_button = QPushButton('Fix/Unfix API Key', self)
        self.fix_api_key_button.clicked.connect(self.toggle_api_key)

        input_layout.addWidget(self.fix_api_key_button)
        layout.addLayout(input_layout)

        self.toggle_always_on_top_button = QPushButton('Always On Top', self)
        self.toggle_always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.toggle_always_on_top_button.setStyleSheet(
            'background-color: #757777; border-color: #0f1c19; color: #000000; min-height: 19px; font: 10.5pt Arial;')
        input_layout.addWidget(self.toggle_always_on_top_button)

        prompt_layout = QHBoxLayout()

        self.radio_rephrase = QRadioButton('Rephrase', self)
        self.radio_rephrase.setChecked(True)
        prompt_layout.addWidget(self.radio_rephrase)

        self.radio_debug_code = QRadioButton('Debug code', self)
        prompt_layout.addWidget(self.radio_debug_code)

        self.radio_summarize = QRadioButton('Summarize', self)
        prompt_layout.addWidget(self.radio_summarize)

        self.radio_translate = QRadioButton('Translate', self)
        prompt_layout.addWidget(self.radio_translate)

        self.radio_email = QRadioButton('Reply to email', self)
        prompt_layout.addWidget(self.radio_email)

        self.radio_explain = QRadioButton('Explain', self)
        prompt_layout.addWidget(self.radio_explain)

        self.radio_manual_prompts = QRadioButton('Manual prompts', self)
        prompt_layout.addWidget(self.radio_manual_prompts)
        layout.addLayout(prompt_layout)

        language_layout = QHBoxLayout()

        language_layout.setAlignment(Qt.AlignLeft)

        self.from_language_dropdown = QComboBox(self)
        self.from_language_dropdown.setStyleSheet(
            'background-color: #073a43; border-color: #000000; color: #FFFFFF; min-height: 20px; font: 10.5pt Arial;')
        self.to_language_dropdown = QComboBox(self)
        self.to_language_dropdown.setStyleSheet(
            'background-color: #073a43; border-color: #000000; color: #FFFFFF; min-height: 20px; font: 10.5pt Arial;')
        self.from_language_dropdown.setHidden(True)
        self.to_language_dropdown.setHidden(True)

        self.from_language_dropdown.setMaximumWidth(100)
        self.to_language_dropdown.setMaximumWidth(100)

        self.from_language_label = QLabel('From Language:', self)
        self.to_language_label = QLabel('To Language:', self)
        self.from_language_label.setHidden(True)
        self.to_language_label.setHidden(True)

        self.from_language_label.setMaximumWidth(120)
        self.to_language_label.setMaximumWidth(100)

        language_layout.addWidget(self.from_language_label)
        language_layout.addWidget(self.from_language_dropdown)
        language_layout.addWidget(self.to_language_label)
        language_layout.addWidget(self.to_language_dropdown)

        layout.addLayout(language_layout)

        self.radio_translate.toggled.connect(self.toggle_language_dropdowns)

        available_languages = [
            "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali",
            "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)",
            "Corsican", "Croatian",
            "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", "French", "Frisian",
            "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew",
            "Hindi",
            "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese",
            "Kannada",
            "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", "Kyrgyz", "Lao", "Latin", "Latvian",
            "Lithuanian",
            "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian",
            "Myanmar (Burmese)",
            "Nepali", "Norwegian", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian",
            "Samoan",
            "Scots Gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali",
            "Spanish",
            "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu",
            "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
        ]
        self.from_language_dropdown.addItems(available_languages)
        self.to_language_dropdown.addItems(available_languages)

        self.checkbox_clipboard = QCheckBox('Use last clipboard text', self)
        self.checkbox_clipboard.setChecked(True)
        layout.addWidget(self.checkbox_clipboard)

        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText('Enter prompt manually...')
        self.input_text.setFixedHeight(70)
        self.input_text.setStyleSheet("QTextEdit { background-color: #222529; color: white; font-size: 11.5pt; border: 1px solid #565856; border-radius: 4px; padding: 5px;}")
        self.input_text.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.input_text.setHidden(True)
        layout.addWidget(self.input_text)

        self.text_editor = QTextEdit(self)
        self.text_editor.setPlaceholderText('Enter text manually...')
        self.text_editor.setStyleSheet("QTextEdit { background-color: #222529; color: white; font-size: 11.5pt; border: 1px solid #565856; border-radius: 4px; padding: 5px;}")
        self.text_editor.setFixedHeight(150)
        self.text_editor.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.text_editor.setHidden(True)
        layout.addWidget(self.text_editor)

        self.proxy_checkbox = QCheckBox('Enable HTTP proxy', self)
        self.proxy_checkbox.toggled.connect(self.configure_proxy)
        layout.addWidget(self.proxy_checkbox)

        self.proxy_input_layout = QVBoxLayout()
        self.proxy_server_input = QLineEdit(self)
        self.proxy_server_input.setPlaceholderText('Enter server address (e.g., 127.0.0.1)')
        self.proxy_server_input.setStyleSheet("QLineEdit { background-color: #222529; color: white; font-size: 11pt; border: 1px solid #565856; border-radius: 2px;}")
        self.proxy_server_input.setFixedHeight(26)
        self.proxy_server_input.setHidden(True)


        self.proxy_input_layout.addWidget(self.proxy_server_input)

        self.proxy_port_input = QLineEdit(self)
        self.proxy_port_input.setStyleSheet("QLineEdit { background-color: #222529; color: white; font-size: 11pt; border: 1px solid #565856; border-radius: 2px;}")
        self.proxy_port_input.setFixedHeight(26)
        self.proxy_port_input.setPlaceholderText('Enter port number (e.g., 10809)')
        self.proxy_port_input.setHidden(True)
        self.proxy_input_layout.addWidget(self.proxy_port_input)

        layout.addLayout(self.proxy_input_layout)

        self.save_proxy_button = QPushButton('Save proxy settings', self)
        self.save_proxy_button.clicked.connect(self.save_proxy_settings)
        self.save_proxy_button.setStyleSheet(
            'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 25px; font: 10.5pt Arial;')
        self.save_proxy_button.setFixedHeight(25)
        self.save_proxy_button.setHidden(True)
        layout.addWidget(self.save_proxy_button)

        self.checkbox_clipboard.stateChanged.connect(self.toggle_clipboard_text)

        self.radio_manual_prompts.toggled.connect(self.toggle_manual_prompt_input)

        self.proxy_checkbox.stateChanged.connect(self.configure_proxy)

        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText('Response will appear here...')
        self.output_text.setStyleSheet("QTextEdit { background-color: #222529; color: white; font-size: 11.5pt; border: 1px solid #565856; border-radius: 4px; padding: 5px;}")
        self.output_text.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.output_text.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)

        layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()

        self.run_regenerate_button = QPushButton('Generate', self)
        self.run_regenerate_button.clicked.connect(self.run_regenerate_text)
        self.run_regenerate_button.setStyleSheet(
                'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')
        self.run_regenerate_button.setFixedHeight(26)
        button_layout.addWidget(self.run_regenerate_button)

        self.copy_button = QPushButton('Copy response', self)
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setStyleSheet(
            'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')
        self.copy_button.setFixedHeight(26)
        button_layout.addWidget(self.copy_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_generation_process)
        self.stop_button.setStyleSheet(
            'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')
        self.stop_button.setFixedHeight(26)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSizeF(11.5)
        self.setFont(font)

        self.from_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)
        self.to_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)

        self.load_config_from_file()
        if self.api_key_input.text() == "":
            self.api_key_fixed = True
            self.api_key_input.setReadOnly(False)
            self.fix_api_key_button.setStyleSheet(
                'background-color: #757777; border-color: #0f1c19; color: #000000; min-height: 19px; font: 10.5pt Arial;')
        else:
            self.api_key_fixed = False
            self.api_key_input.setReadOnly(True)
            self.fix_api_key_button.setStyleSheet(
                'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 19px; font: 10.5pt Arial;')
        print("Key is:", self.api_key_input.text())

    def toggle_language_dropdowns(self, checked):
        self.from_language_dropdown.setHidden(not checked)
        self.to_language_dropdown.setHidden(not checked)
        self.from_language_label.setHidden(not checked)
        self.to_language_label.setHidden(not checked)

    def toggle_manual_prompt_input(self, checked):
        self.input_text.setHidden(not checked)
        if checked:
            self.input_text.setFocus()

    def toggle_api_key(self):
        if not self.api_key_input.text() == "":
            if self.api_key_fixed is False:
                self.api_key_fixed = True
                self.api_key_input.setReadOnly(False)
                self.fix_api_key_button.setStyleSheet(
                    'background-color: #757777; border-color: #0f1c19; color: #000000; min-height: 19px; font: 10.5pt Arial;')
            else:
                self.api_key_fixed = False
                self.api_key_input.setReadOnly(True)
                self.api_key = self.api_key_input.text()
                # self.set_api_key()
                self.fix_api_key_button.setStyleSheet(
                    'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 19px; font: 10.5pt Arial;')
        else:
            self.fix_api_key_button.setStyleSheet(
                'background-color: #757777; border-color: #0f1c19; color: #000000; min-height: 19px; font: 10.5pt Arial;')

        self.save_config_to_file()
    def toggle_proxy_settings(self, state):
        self.proxy_server_input.setHidden(not state)
        self.proxy_port_input.setHidden(not state)
        self.save_proxy_button.setHidden(not state)

    def load_config_from_file(self):
        if os.path.exists(self.CONFIG_FILE_PATH):
            with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                config_data = json.load(config_file)
                saved_api_key = config_data.get('api_key')
                saved_proxy_enabled = config_data.get('proxy_enabled', False)
                self.saved_proxy_server = config_data.get('proxy_server', '')
                self.saved_proxy_port = config_data.get('proxy_port', '')
                from_language = config_data.get('from_language', '')
                to_language = config_data.get('to_language', '')

                from_index = self.from_language_dropdown.findText(from_language)
                to_index = self.to_language_dropdown.findText(to_language)

                if from_index != -1:
                    self.from_language_dropdown.setCurrentIndex(from_index)

                if to_index != -1:
                    self.to_language_dropdown.setCurrentIndex(to_index)

                if saved_api_key:
                    self.api_key_input.setText(saved_api_key)
                    self.api_key = saved_api_key

                if saved_proxy_enabled:
                    self.proxy_checkbox.setChecked(True)
                    self.proxy_server_input.setText(self.saved_proxy_server)
                    self.proxy_port_input.setText(self.saved_proxy_port)
                    self.toggle_proxy_settings(False)
                print(self.saved_proxy_server)
                print(self.proxy_port_input)

    def save_config_to_file(self):
        api_key = self.api_key_input.text().strip()
        proxy_enabled = self.proxy_checkbox.isChecked()
        proxy_server = self.proxy_server_input.text().strip()
        proxy_port = self.proxy_port_input.text().strip()

        from_language = self.from_language_dropdown.currentText()
        to_language = self.to_language_dropdown.currentText()

        config_data = {
            'api_key': api_key,
            'proxy_enabled': proxy_enabled,
            'proxy_server': proxy_server,
            'proxy_port': proxy_port,
            'from_language': from_language,
            'to_language': to_language
        }

        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            json.dump(config_data, config_file)

    def save_proxy_settings(self):
        proxy_server = self.proxy_server_input.text().strip()
        proxy_port = self.proxy_port_input.text().strip()
        if not proxy_server or not proxy_port:
            self.show_error_message("Please enter both proxy server and port.")
            self.proxy_checkbox.setChecked(False)
            return

        self.save_config_to_file()
        self.toggle_proxy_settings(False)

    def configure_proxy(self):
        if self.proxy_checkbox.isChecked():
            self.toggle_proxy_settings(True)
            proxy_server = self.proxy_server_input.text().strip()
            proxy_port = self.proxy_port_input.text().strip()

            try:
                self.client = openai.OpenAI(api_key=self.api_key, http_client=httpx.Client(proxies=f"http://{proxy_server}:{proxy_port}"))
            except:
                pass
        else:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except:
                pass
            self.toggle_proxy_settings(False)

    def run_regenerate_text(self):

        from_language = self.from_language_dropdown.currentText()
        to_language = self.to_language_dropdown.currentText()

        if self.api_key_fixed:
            self.set_api_key()

        if self.radio_rephrase.isChecked():
            prompt = "Rephrase and improve the following text:"
        elif self.radio_debug_code.isChecked():
            prompt = "Debug the following code:"
        elif self.radio_explain.isChecked():
            prompt = "Explain the following text:"
        elif self.radio_summarize.isChecked():
            prompt = "Summarize the following text:"
        elif self.radio_translate.isChecked():
            prompt = f"Translate the following text from {from_language} to {to_language}:"
        elif self.radio_email.isChecked():
            prompt = "Write a reply to this email. Avoid wordy language:"
        elif self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText()
        else:
            prompt = "Rephrase and improve the following text:"

        if self.checkbox_clipboard.isChecked():
            clipboard = QApplication.clipboard()
            prompt += " " + clipboard.text()

        elif not self.checkbox_clipboard.isChecked():
            prompt += " " + self.text_editor.toPlainText()

        elif not self.checkbox_clipboard.isChecked() and self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText() + " " + self.text_editor.toPlainText()

        self.save_config_to_file()

        self.run_regenerate_button.setEnabled(False)
        self.run_regenerate_button.setStyleSheet(
            'background-color: #4b4b4b; border-color: #4b4b4b; color: #a5a5a5; min-height: 26px; font: 10.5pt Arial;'
        )
        self.run_regenerate_button.setText("Generating your response...")

        self.generate_response(prompt)

        self.run_regenerate_button.setEnabled(True)
        self.run_regenerate_button.setStyleSheet(
            'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')
        self.run_regenerate_button.setText("Generate")

    def toggle_clipboard_text(self, state):
        self.text_editor.setHidden(state == Qt.Checked)

    def toggle_always_on_top(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                'background-color: #757777; border-color: #0f1c19; color: #000000; min-height: 19px; font: 10.5pt Arial;')
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                'background-color: #073a43; border-color: #0f1c19; color: #FFFFFF; min-height: 19px; font: 10.5pt Arial;')
        self.show()

    def set_api_key(self):
        self.api_key = self.api_key_input.text()
        if self.api_key:
            e = openai.OpenAIError
            self.show_api_key_error_alert(str(e))
        else:
            self.show_api_key_error_alert("Please enter a valid API key.")
        self.save_config_to_file()

    def generate_response(self, prompt):
        try:
            self.stop_generation = False
            full_text = ""
            block_color_status = 0
            self.configure_proxy()
            self.toggle_proxy_settings(False)

            for part in self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-3.5-turbo",
                    stream=True,
            ):

                if self.stop_generation:
                    break
                new_content = part.choices[0].delta.content or ""

                if block_color_status == 0:
                    if new_content.startswith("```"):
                        block_color_status = 1
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="green">' + new_content + '</font>'
                    elif new_content.startswith("`"):
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="green">' + new_content + '</font>'
                    else:
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="white">' + new_content + '</font>'

                elif block_color_status == 1:
                    if new_content.startswith("``"):
                        block_color_status = 0
                    new_content = new_content.replace('\n', '<br>')
                    full_text += '<font color="green">' + new_content + '</font>'

                if new_content:
                    self.output_text.setHtml(full_text)

                self.output_text.verticalScrollBar().setValue(self.output_text.verticalScrollBar().maximum())

                QApplication.processEvents()

            code_blocks = re.findall(r"```([\s\S]+?)``", full_text)

            html_code = ''.join(code_blocks)

            soup = BeautifulSoup(html_code, 'html.parser')

            for br_tag in soup.find_all('br'):
                br_tag.replace_with('\n')

            plain_text = soup.get_text()

            language = ""
            for code_block in code_blocks:

                start_delimiter = '<font color="green">'
                end_delimiter = '</font>'

                start_index = code_block.find(start_delimiter)
                end_index = code_block.find(end_delimiter, start_index + len(start_delimiter))

                if start_index != -1 and end_index != -1:
                    language = code_block[start_index + len(start_delimiter):end_index]

                if language == "":
                    language = "python"

                lexer = get_lexer_by_name(language, stripall=True)

                formatter = HtmlFormatter(style="native", noclasses=True, nobackground=True)

                highlighted_code = highlight(plain_text, lexer, formatter)
                try:
                    updated_html = full_text.replace('``</font><font color="green">`', '```')
                except:
                    updated_html = full_text

                full_text = updated_html.replace(f"```{code_block}```", highlighted_code)

            full_text = full_text.replace('<br><br></font><font color="green">',
                                          '<br></font><font color="green">')
            full_text = full_text.replace('</font><font color="green"><br><br>',
                                          '</font><font color="green">')

            self.output_text.setHtml(full_text)
            QApplication.processEvents()

        except openai.OpenAIError as err:
            self.output_text.setPlainText(str(err))

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())

        self.copy_button.setEnabled(False)
        self.copy_button.setText("Copied!")
        self.copy_button.setStyleSheet(
            'background-color: #04262c; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clear_copied)
        self.timer.start(2000)

    def clear_copied(self):
        self.timer.stop()
        self.copy_button.setEnabled(True)
        self.copy_button.setText("Copy response")
        self.copy_button.setStyleSheet(
            'background-color: #073a43; border-color: #127287; color: #FFFFFF; min-height: 26px; font: 10.5pt Arial;')

    def stop_generation_process(self):
        self.stop_generation = True

    def show_api_key_error_alert(self, error_message):
        alert = QMessageBox()
        alert.setWindowTitle("API Key Error")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error setting API key!")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    def show_error_message(self, message):
        error_message = QMessageBox()
        error_message.setWindowTitle("Error")
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText(message)
        error_message.exec_()

    def set_widget_palette_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.WindowText, QColor(color))
        widget.setPalette(palette)

def main():
    app = QApplication(sys.argv)

    app_icon = QIcon(QPixmap.fromImage(QtGui.QImage.fromData(ICON_DATA)))
    app.setWindowIcon(app_icon)

    app.setStyle('Fusion')

    ui = GPTUI()

    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
