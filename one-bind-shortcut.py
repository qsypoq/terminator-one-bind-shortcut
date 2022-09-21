import terminatorlib.plugin as plugin
import os
from terminatorlib.translation import _
from terminatorlib.terminator import Terminator
from terminatorlib.version import APP_VERSION

if float(APP_VERSION) <= 0.98:
    import gtk as Gtk
else:
    import gi
    from gi.repository import Gtk, Gdk

AVAILABLE = ['OneBindShortCut']

class OneBindShortCut(plugin.Plugin):
    capabilities = ['terminal_menu']

    def __init__(self):
        self.windows = Terminator().get_windows()
        for window in self.windows:
            window.connect('key-press-event', self.onKeyPress)

    def broadcast_all(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['all']:
                t.key_broadcast_all()
            else:
                t.key_broadcast_off()
            break

    def broadcast_group(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['group']:
                t.key_broadcast_group()
            else:
                t.key_broadcast_off()
            break

    def onKeyPress(self, widget, event):
        if float(APP_VERSION) <= 0.98:
            if (event.state & Gtk.gdk.CONTROL_MASK == Gtk.gdk.CONTROL_MASK) and (event.keyval == 81 or event.keyval == 113): #CTRL+Q
                self.broadcast_all(widget)
        else:
            if (event.state & Gdk.ModifierType.CONTROL_MASK == Gdk.ModifierType.CONTROL_MASK) and (event.keyval == 81 or event.keyval == 113): #CTRL+Q
                self.broadcast_all(widget)