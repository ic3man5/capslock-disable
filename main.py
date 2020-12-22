import sys
from PySide import QtGui, QtCore

import win32api
import win32con

from threading import Thread, Event
import time

def setup_menu():
    menu = QtGui.QMenu()
    enable_action = menu.addAction("&Enable")
    disable_action = menu.addAction("&Disable")
    exit_action = menu.addAction("E&xit")
    enable_action.triggered.connect(enable_thread)
    disable_action.triggered.connect(stop_thread)
    exit_action.triggered.connect(quit)
    return menu

def disable_capslock():
    state = win32api.GetKeyState(win32con.VK_CAPITAL)
    if ((state & 0x80) != 0x80 and (state & 0x01) == 0x01):
        win32api.keybd_event(win32con.VK_CAPITAL, 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0);
        win32api.keybd_event(win32con.VK_CAPITAL, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0);
    
def disable_capslock_loop(event):
    while not event.wait(0.1):
        disable_capslock()
        #print("running!")

t_event = Event()
t = Thread(target=disable_capslock_loop, args=(t_event,))
t.daemon = True
#t.start()

icon = None

def enable_thread():
    global t_event
    global t
    t_event = Event()
    t = Thread(target=disable_capslock_loop, args=(t_event,))
    t.daemon = True
    t.start()
    icon.setIcon(QtGui.QIcon("icon-enable.png"))
    #print("Starting thread...")
    
def stop_thread():
    global t_event
    t_event.set()
    t.join()
    icon.setIcon(QtGui.QIcon("icon-disable.png"))
    #print("Stopping thread...")
    
def quit():
    QtGui.QApplication.exit()



if __name__ == "__main__":
    disable_capslock()
    app = QtGui.QApplication(sys.argv)

    menu = setup_menu()
    
    icon = QtGui.QSystemTrayIcon()
    icon.setIcon(QtGui.QIcon("icon-disable.png"))
    icon.setContextMenu(menu)
    icon.show()
    #icon.showMessage("Hello!", "Hello World!")
    enable_thread()

    app.exec_()
    
    sys.exit()
