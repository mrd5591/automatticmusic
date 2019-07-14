import keyboard
from tkinter import *
import codecs
import os
import MakeImage
import base64
import AutoMatticMusic

class Settings:
    def __init__(self):
        self.p = os.getenv('APPDATA')
        self.p+='\\AutoMattic Music\\'
        self.exitFlag = False

        try:
            file = codecs.open(self.p+'binds.txt', 'r', encoding='utf-8', errors='ignore')
        except:
            file = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            file.write('pause:\n')
            file.write('rewind:\n')
            file.write('skip:\n')
            file.write('volumeup:\n')
            file.write('volumedown:\n')
        file.close()
        self.main()

    def main(self):
        self.root = Tk()

        self.root.configure(bg = '#2b3038')
        self.root.title("Settings")
        self.root.minsize(width=225, height=150)
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap(self.p+'automatticmusicicon.ico')
        except:
            self.makeImg('automatticmusicicon.ico', 'icon')
            self.root.iconbitmap(self.p+'automatticmusicicon.ico')

        self.pauseButton = Button(self.root, command=lambda: self.pauseBind(), text="Set Pause Bind", background = '#2b3038', foreground='white', relief=FLAT)
        self.pauseButton.bind('<Enter>', lambda event: self.pauseButton.configure(relief='raised'))
        self.pauseButton.bind('<Leave>', lambda event: self.pauseButton.configure(relief='flat'))
        self.rewindButton = Button(self.root, command=lambda: self.rewindBind(), text="Set Rewind Bind", background = '#2b3038', foreground='white', relief=FLAT)
        self.rewindButton.bind('<Enter>', lambda event: self.rewindButton.configure(relief='raised'))
        self.rewindButton.bind('<Leave>', lambda event: self.rewindButton.configure(relief='flat'))
        self.skipButton = Button(self.root, command=lambda: self.skipBind(), text="Set Skip Bind", background = '#2b3038', foreground='white', relief=FLAT)
        self.skipButton.bind('<Enter>', lambda event: self.skipButton.configure(relief='raised'))
        self.skipButton.bind('<Leave>', lambda event: self.skipButton.configure(relief='flat'))
        self.vUpButton = Button(self.root, command=lambda: self.vUpBind(), text="Set Increase Volume Bind", background = '#2b3038', foreground='white', relief=FLAT)
        self.vUpButton.bind('<Enter>', lambda event: self.vUpButton.configure(relief='raised'))
        self.vUpButton.bind('<Leave>', lambda event: self.vUpButton.configure(relief='flat'))
        self.vDownButton = Button(self.root, command=lambda: self.vDownBind(), text="Set Decrease Volume Bind", background = '#2b3038', foreground='white', relief=FLAT)
        self.vDownButton.bind('<Enter>', lambda event: self.vDownButton.configure(relief='raised'))
        self.vDownButton.bind('<Leave>', lambda event: self.vDownButton.configure(relief='flat'))

        self.pauseButton.pack(pady=5)
        self.rewindButton.pack(pady=5)
        self.skipButton.pack(pady=5)
        self.vUpButton.pack(pady=5)
        self.vDownButton.pack(pady=5)

        self.fixBindings()

        self.hook = None

        self.root.protocol('WM_DELETE_WINDOW', self.die)
        self.root.mainloop()

    def on_press(self, key):
        keyboard.unhook_all()
        if self.exitFlag:
            return
        f = codecs.open(self.p+'binds.txt', 'r', encoding='utf-8', errors='ignore')
        binds = f.readlines()
        f.close()
        if self.currentBind == 'pause':
            f = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            for i in binds:
                if i.split(':')[0].strip() == 'pause':
                    f.write('pause:{}\n'.format(key.name))
                    self.pauseButton.config(text='Set Pause Bind: {}'.format(key.name))
                else:
                    f.write(i)
            f.close()
        elif self.currentBind == 'rewind':
            f = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            for i in binds:
                if i.split(':')[0].strip() == 'rewind':
                    f.write('rewind:{}\n'.format(key.name))
                    self.rewindButton.config(text='Set Rewind Bind: {}'.format(key.name))
                else:
                    f.write(i)
            f.close()
        elif self.currentBind == 'skip':
            f = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            for i in binds:
                if i.split(':')[0].strip() == 'skip':
                    f.write('skip:{}\n'.format(key.name))
                    self.skipButton.config(text='Set Skip Bind: {}'.format(key.name))
                else:
                    f.write(i)
            f.close()
        elif self.currentBind == 'volumeup':
            f = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            for i in binds:
                if i.split(':')[0].strip() == 'volumeup':
                    f.write('volumeup:{}\n'.format(key.name))
                    self.vUpButton.config(text='Set Increase Volume Bind: {}'.format(key.name))
                else:
                    f.write(i)
            f.close()
        elif self.currentBind == 'volumedown':
            f = codecs.open(self.p+'binds.txt', 'w', encoding='utf-8', errors='ignore')
            for i in binds:
                if i.split(':')[0].strip() == 'volumedown':
                    f.write('volumedown:{}\n'.format(key.name))
                    self.vDownButton.config(text='Set Decrease Volume Bind: {}'.format(key.name))
                else:
                    f.write(i)
            f.close()


    def vDownBind(self):
        self.fixBindings()
        self.currentBind = 'volumedown'
        keyboard.unhook_all()
        self.hook = keyboard.hook(self.on_press)
        self.vDownButton.config(text='Set Decrease Volume Bind: ...')

    def vUpBind(self):
        self.fixBindings()
        self.currentBind = 'volumeup'
        keyboard.unhook_all()
        self.hook = keyboard.hook(self.on_press)
        self.vUpButton.config(text='Set Increase Volume Bind: ...')

    def skipBind(self):
        self.fixBindings()
        self.currentBind = 'skip'
        keyboard.unhook_all()
        self.hook = keyboard.hook(self.on_press)
        self.skipButton.config(text='Set Skip Bind: ...')

    def rewindBind(self):
        self.fixBindings()
        self.currentBind = 'rewind'
        keyboard.unhook_all()
        self.hook = keyboard.hook(self.on_press)
        self.rewindButton.config(text='Set Rewind Bind: ...')

    def pauseBind(self):
        self.fixBindings()
        self.currentBind = 'pause'
        keyboard.unhook_all()
        self.hook = keyboard.hook(self.on_press)
        self.pauseButton.config(text='Set Pause Bind: ...')

    def makeImg(self, strng, com):
        b = MakeImage.MakeImage(strng, com)
        icon = b.getImage()
        icondata = base64.b64decode(icon)
        tempFile = strng
        iconfile = codecs.open(self.p+tempFile, 'wb', errors='ignore')
        iconfile.write(icondata)
        iconfile.close()

    def fixBindings(self):
        f = codecs.open(self.p+'binds.txt', 'r', encoding='utf-8', errors='ignore')
        binds = f.readlines()
        f.close()

        for i in binds:
            if i.split(':')[0].strip() == 'pause':
                if i.split(':')[1].strip() == "":
                    self.pauseButton.config(text='Set Pause Bind: Unbound')
                else:
                    self.pauseButton.config(text='Set Pause Bind: {}'.format(i.split(':')[1].strip()))
            elif i.split(':')[0].strip() == 'rewind':
                if i.split(':')[1].strip() == "":
                    self.rewindButton.config(text='Set Rewind Bind: Unbound')
                else:
                    self.rewindButton.config(text='Set Rewind Bind: {}'.format(i.split(':')[1].strip()))
            elif i.split(':')[0].strip() == 'skip':
                if i.split(':')[1].strip() == "":
                    self.skipButton.config(text='Set Skip Bind: Unbound')
                else:
                    self.skipButton.config(text='Set Skip Bind: {}'.format(i.split(':')[1].strip()))
            elif i.split(':')[0].strip() == 'volumeup':
                if i.split(':')[1].strip() == "":
                    self.vUpButton.config(text='Set Increase Volume Bind: Unbound')
                else:
                    self.vUpButton.config(text='Set Increase Volume Bind: {}'.format(i.split(':')[1].strip()))
            elif i.split(':')[0].strip() == 'volumedown':
                if i.split(':')[1].strip() == "":
                    self.vDownButton.config(text='Set Decrease Volume Bind: Unbound')
                else:
                    self.vDownButton.config(text='Set Decrease Volume Bind: {}'.format(i.split(':')[1].strip()))

    def die(self):
        self.exitFlag = True
        self.root.destroy()
        
if __name__=='__main__':
    Settings()
