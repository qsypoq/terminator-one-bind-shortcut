import terminatorlib.plugin as plugin
import os
import time
from terminatorlib.translation import _
from terminatorlib.terminator import Terminator
from terminatorlib.version import APP_VERSION, APP_NAME

if float(APP_VERSION) <= 0.98:
    import gtk as Gtk
else:
    import gi
    from gi.repository import Gtk, Gdk, GObject, Notify
    

AVAILABLE = ['OneBindShortCut']

class OneBindShortCut(plugin.Plugin):
    capabilities = ['terminal_menu']

    def __init__(self):
        self.windows = Terminator().get_windows()
        for window in self.windows:
            window.connect('key-press-event', self.onKeyPress)
        Notify.init(APP_NAME.capitalize())

    def send_notify(self,msg):
        note = Notify.Notification.new(_(msg), '' ,'terminator')
        note.set_timeout(15)
        note.show()

    def broadcast_all(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['all']:
                t.key_broadcast_all()
                self.send_notify('Broadcast All Activated')
            else:
                t.key_broadcast_off()
                self.send_notify('Broadcast All Desactivated')
            break

    def broadcast_group(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['group']:
                t.key_broadcast_group()
                self.send_notify('Broadcast Group Activated')
            else:
                t.key_broadcast_off()
                self.send_notify('Broadcast Group Desactivated')
            break

    def onKeyPress(self, widget, event):
        if float(APP_VERSION) <= 0.98:
            if (event.state & Gtk.gdk.CONTROL_MASK == Gtk.gdk.CONTROL_MASK) and (event.keyval == 81 or event.keyval == 113): #CTRL+Q
                self.broadcast_all(widget)
        else:
            if (event.state & Gdk.ModifierType.CONTROL_MASK == Gdk.ModifierType.CONTROL_MASK) and (event.keyval == 81 or event.keyval == 113): #CTRL+Q
                self.broadcast_all(widget)