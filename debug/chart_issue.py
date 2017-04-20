#!/usr/bin/python
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

# Import modules from /batterym/ folder.
import sys
sys.path.append(os.path.abspath('../batterym'))
import log
import plotter


CHART = 'tmp_chart.svg'
LOG = 'capacity'


def main():
    plotter.caluclate_chart(CHART, LOG)

    window = gtk.Window()
    window.set_title('Battery Monitor')
    window.set_border_width(10)
    window.set_size_request(700, 500)
    window.set_resizable(False)
    window.set_position(gtk.WindowPosition.CENTER)
    window.vbox = gtk.Box()
    window.vbox.set_spacing(5)
    window.vbox.set_orientation(gtk.Orientation.VERTICAL)
    window.add(window.vbox)
    image = gtk.Image()
    image.set_from_file(CHART)
    window.vbox.pack_start(image, False, False, 0)
    window.show_all()
    gtk.main()


if __name__ == '__main__':
    main()
