from tkinter import *
import spotifyapi
import youtube2sound as y2s
import MakeImage
import base64
import codecs
import os

class spotifyRoot:
    songs = []
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg = '#2b3038')
        self.root.title("AutoMattic Music Spotify Download")
        self.root.minsize(width=225, height=215)
        self.p = os.getenv('APPDATA')
        self.p+='\\AutoMattic Music\\'
        if not os.path.exists(self.p):
            os.makedirs(self.p)
        self.makeWidgets()
        try:
            self.root.iconbitmap(self.p+'automatticmusicicon.ico')
        except:
            self.makeImg('automatticmusicicon.ico', 'icon')
            self.root.iconbitmap(self.p+'automatticmusicicon.ico')
        self.root.mainloop()

    def makeWidgets(self):
        self.playlists = Listbox(self.root, selectmode=EXTENDED, bg='#ffffff', height=8, background = '#2b3038', foreground='white')
        self.playlists.pack(pady=10)
        self.playlists.configure(justify=LEFT)
        download = Button(self.root, command=lambda: y2s.Youtube2Sound(self.songs, self.playlists.curselection()), text="Download", background = '#2b3038', foreground='white', relief=FLAT)
        download.bind('<Enter>', lambda event: download.configure(relief='raised'))
        download.bind('<Leave>', lambda event: download.configure(relief='flat'))
        login = Button(self.root, command=lambda: self.spotifyDL(), text="Login", background = '#2b3038', foreground='white', relief=FLAT)
        login.bind('<Enter>', lambda event: login.configure(relief='raised'))
        login.bind('<Leave>', lambda event: login.configure(relief='flat'))
        download.pack()
        login.pack(pady=5)

    def spotifyDL(self):
        self.songs = spotifyapi.main()
        currentPlaylists = self.playlists.get(0, END)
        for i in self.songs:
            if i[0] not in currentPlaylists:
                self.playlists.insert(END, i[0])

    def makeImg(self, strng, com):
        b = MakeImage.MakeImage(strng, com)
        icon = b.getImage()
        icondata = base64.b64decode(icon)
        tempFile = strng
        iconfile = codecs.open(self.p+tempFile, 'wb', errors='ignore')
        iconfile.write(icondata)
        iconfile.close()

if __name__=='__main__':
    x = spotifyRoot()
