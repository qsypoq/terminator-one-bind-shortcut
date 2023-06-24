import terminatorlib.plugin as plugin
from terminatorlib.translation import _
from terminatorlib.terminator import Terminator
import gi
from gi.repository import Gtk, Gdk, GObject
from terminatorlib.util import err, dbg
from terminatorlib.version import APP_NAME


try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    # Every plugin you want Terminator to load *must* be listed in 'AVAILABLE'
    # This is inside this try so we only make the plugin available if pynotify
    #  is present on this computer.
    AVAILABLE = ['OneBindShortCut']
except (ImportError, ValueError):
    err('OneBindShortcut plugin unavailable as we cannot import Notify')



class OneBindShortCut(plugin.Plugin):
    capabilities = ['terminal_menu']

    def __init__(self):
        self.windows = Terminator().get_windows()
        for window in self.windows:
            window.connect('key-press-event', self.onKeyPress)
        Notify.init(APP_NAME.capitalize())

    def notify(self,msg):
        note = Notify.Notification.new(_(msg), '' ,'terminator')
        note.set_timeout(15)
        note.show()

    def broadcast_all(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['all']:
                t.key_broadcast_all()
                self.notify('Broadcast All Activated')
            else:
                t.key_broadcast_off()
                self.notify('Broadcast All Desactivated')
            break

    def broadcast_group(self, widget):
        for t in Terminator().terminals:
            if t.terminator.groupsend != t.terminator.groupsend_type['group']:
                t.key_broadcast_group()
                self.notify('Broadcast Group Activated')
            else:
                t.key_broadcast_off()
                self.notify('Broadcast Group Desactivated')
            break

    def onKeyPress(self, widget, event):
        if (event.state & Gdk.ModifierType.CONTROL_MASK == Gdk.ModifierType.CONTROL_MASK) and (event.keyval == 81 or event.keyval == 113): #CTRL+Q
                self.broadcast_all(widget)
