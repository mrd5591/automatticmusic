import os
import base64
import MakeImage
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import psutil
from random import shuffle, Random
import threading
import vlc
import subprocess
import time
import codecs
import keyboard
import Settings
from belfrywidgets import ToolTip

class AutoMatticMusic:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.music = []
        self.ptop = False
        self.path = ""
        self.processName = ""
        self.stopped = True
        self.currentProcess = ""
        self.currentlyPlaying = ''
        self.playlist = False
        self.notPlaying = True
        self.alreadyPlayed = []
        self.currentPlaylist = []
        self.currentBind = ""
        self.bindCommand = ""
        self.listOfMusicTypes = ['mp3', 'wav', 'ogg', 'xm', 'mod', 'aac', 'flac', 'ac3', 'wma', 'm4a', 'ra', 'midi', 'alac', 'webm']
        self.main()

    def main(self):
        master = Tk()

        master.configure(bg = '#2b3038')
        master.title("AutoMattic Music")
        master.resizable(width=False, height=False)
        master.minsize(width=470, height=430)

        self.p = os.getenv('APPDATA')
        self.p += '\\AutoMattic Music\\'

        keyboard.on_press(self.mainListener)

        if not os.path.exists(self.p):
            os.makedirs(self.p)

        try:
            master.iconbitmap(self.p+'automatticmusicicon.ico')
        except:
            self.makeImg('automatticmusicicon.ico', 'icon')
            master.iconbitmap(self.p+'automatticmusicicon.ico')

        try:
            self.playimg=PhotoImage(file=self.p+"play.png")
        except:
            self.makeImg('play.png', 'play')
            self.playimg=PhotoImage(file=self.p+"play.png")

        try:
            self.pauseimg=PhotoImage(file=self.p+'pause.png')
        except:
            self.makeImg('pause.png', 'pause')
            self.pauseimg=PhotoImage(file=self.p+'pause.png')

        try:
            self.stopimg=PhotoImage(file=self.p+'stop.png')
        except:
            self.makeImg('stop.png', 'stop')
            self.stopimg=PhotoImage(file=self.p+'stop.png')

        try:
            self.ammimg=PhotoImage(file=self.p+'amm.png')
        except:
            self.makeImg('amm.png', 'amm')
            self.ammimg=PhotoImage(file=self.p+'amm.png')

        try:
            self.spotifyimg=PhotoImage(file=self.p+'spotify.png')
        except:
            self.makeImg('spotify.png', 'spotify')
            self.spotifyimg=PhotoImage(file=self.p+'spotify.png')

        try:
            self.settingsimg=PhotoImage(file=self.p+'settings.png')
        except:
            self.makeImg('settings.png', 'settings')
            self.settingsimg=PhotoImage(file=self.p+'settings.png')

        self.L1 = ttk.Label(master, text="", background = '#2b3038', foreground='white')
        #self.L1.bind('<Enter>', lambda event: self.L1.configure(text=self.path+'/'))
        #self.L1.bind('<Leave>', lambda event: self.sendPath(self.path))
        self.L2 = ttk.Label(master, text="", background = '#2b3038', foreground='white')
        self.plList = Listbox(master, height=11, width=20, background = '#2b3038', foreground='white')
        self.LB1 = Listbox(master, selectmode=EXTENDED, bg='#ffffff', height=13, background = '#2b3038', foreground='white')
        self.B1 = Button(master, command=lambda: self.filePath(filedialog.askdirectory()), text="Choose Path:", background = '#2b3038', foreground='white', relief=FLAT)
        self.B1.bind('<Enter>', lambda event: self.B1.configure(relief='raised'))
        self.B1.bind('<Leave>', lambda event: self.B1.configure(relief='flat'))
        self.playButton = Button(master, command=lambda: self.checkPause(), background = '#2b3038', foreground='white', relief=FLAT)
        self.playButton.bind('<Enter>', lambda event: self.playButton.configure(relief='raised'))
        self.playButton.bind('<Leave>', lambda event: self.playButton.configure(relief='flat'))
        self.playButton.config(image=self.playimg)
        self.selectProcess = Button(master, command=lambda: self.setProcess(filedialog.askopenfilename()), text="Select Process:", background = '#2b3038', foreground='white', relief=FLAT)
        self.selectProcess.bind('<Enter>', lambda event: self.selectProcess.configure(relief='raised'))
        self.selectProcess.bind('<Leave>', lambda event: self.selectProcess.configure(relief='flat'))
        self.createPlButton = Button(master, command=lambda: self.createPlaylist(), text="Create Playlist", background = '#2b3038', foreground='white', relief=FLAT)
        self.createPlButton.bind('<Enter>', lambda event: self.createPlButton.configure(relief='raised'))
        self.createPlButton.bind('<Leave>', lambda event: self.createPlButton.configure(relief='flat'))
        self.delPL = Button(master, command=lambda: self.findPlaylist('del'), text="Delete Playlist", background = '#2b3038', foreground='white', relief=FLAT)
        self.delPL.bind('<Enter>', lambda event: self.delPL.configure(relief='raised'))
        self.delPL.bind('<Leave>', lambda event: self.delPL.configure(relief='flat'))
        self.automattic = Button(master, command=lambda: self.checkPtoP(), background = '#2b3038', foreground='white', relief=FLAT)
        self.automattic.bind('<Enter>', lambda event: self.automattic.configure(relief='raised'))
        self.automattic.bind('<Leave>', lambda event: self.automattic.configure(relief='flat'))
        self.automattic.config(image=self.ammimg)
        self.plRank = Entry(master, background = '#2b3038', foreground='white')
        self.rankSet = Button(master, command=lambda: self.findPlaylist('rank'), text="Change Playlist Priority", background = '#2b3038', foreground='white', relief=FLAT)
        self.rankSet.bind('<Enter>', lambda event: self.rankSet.configure(relief='raised'))
        self.rankSet.bind('<Leave>', lambda event: self.rankSet.configure(relief='flat'))
        self.clearSongs = Button(master, command=lambda: self.clear(), text='Clear List', background = '#2b3038', foreground='white', relief=FLAT)
        self.clearSongs.bind('<Enter>', lambda event: self.clearSongs.configure(relief='raised'))
        self.clearSongs.bind('<Leave>', lambda event: self.clearSongs.configure(relief='flat'))
        self.addSong = Button(master, command=lambda: self.addSongs(), text="Add Songs", background = '#2b3038', foreground='white', relief=FLAT)
        self.addSong.bind('<Enter>', lambda event: self.addSong.configure(relief='raised'))
        self.addSong.bind('<Leave>', lambda event: self.addSong.configure(relief='flat'))
        self.checkSongs = Button(master, command=lambda: self.checkSongsInPL(), text="Check Songs", background = '#2b3038', foreground='white', relief=FLAT)
        self.checkSongs.bind('<Enter>', lambda event: self.checkSongs.configure(relief='raised'))
        self.checkSongs.bind('<Leave>', lambda event: self.checkSongs.configure(relief='flat'))
        self.spotifyBttn = Button(master, command=lambda: self.startRoot(), background = '#2b3038', foreground='white', relief=FLAT)
        self.spotifyBttn.bind('<Enter>', lambda event: self.spotifyBttn.configure(relief='raised'))
        self.spotifyBttn.bind('<Leave>', lambda event: self.spotifyBttn.configure(relief='flat'))
        self.spotifyBttn.config(image=self.spotifyimg)
        #self.donate = Button(master, text='Donate! I\'m a broke college kid.', command=lambda: webbrowser.open('http://www.google.com'), background = '#2b3038', foreground='white', relief=FLAT)
        self.loadM3UPlaylistsButton = Button(master, command=lambda: self.loadM3UPlaylists(), text="Load M3U Playlists", background = '#2b3038', foreground='white', relief=FLAT)
        self.loadM3UPlaylistsButton.bind('<Enter>', lambda event: self.loadM3UPlaylistsButton.configure(relief='raised'))
        self.loadM3UPlaylistsButton.bind('<Leave>', lambda event: self.loadM3UPlaylistsButton.configure(relief='flat'))
        self.settings = Button(master, command=Settings.Settings, background = '#2b3038', foreground='white', relief=FLAT)
        self.settings.bind('<Enter>', lambda event: self.settings.configure(relief='raised'))
        self.settings.bind('<Leave>', lambda event: self.settings.configure(relief='flat'))
        self.settings.config(image=self.settingsimg)
        self.volume = Scale(master, length = 140, label='              Volume', orient = 'horizontal', fg = 'white', bg='#2b3038', command=self.VolAdj)

        ToolTip(self.LB1, 'Songs')
        ToolTip(self.plList, 'Playlists')

        self.B1.place(x=10, y=5)
        self.L1.place(x=90, y=8)
        self.selectProcess.place(x=10, y=35)
        self.L2.place(x=97, y=38)
        self.playButton.place(x = 72, y = 315)
        self.LB1.place(x=10, y=65)
        self.createPlButton.place(x=175, y=65)
        self.plList.place(x= 155, y=95)
        self.automattic.place(x=303, y=315)
        self.delPL.place(x=295, y=95)
        self.plRank.place(x=430, y=133, width=30)
        self.rankSet.place(x=295, y=130)
        self.clearSongs.place(x=10, y=282)
        self.addSong.place(x=295, y=200)
        self.checkSongs.place(x=295, y=165)
        self.spotifyBttn.place(x = 295, y = 235)
        #self.donate.pack(side=BOTTOM)
        self.loadM3UPlaylistsButton.place(x=162, y=282)
        self.settings.place(x=432, y=392)
        self.volume.place(x=320, y=5)

        try:
            file = codecs.open(self.p+'playlists.csv', 'r', encoding='utf-8', errors='ignore')
        except:
            file = codecs.open(self.p+'playlists.csv', 'w', encoding='utf-8', errors='ignore')
        file.close()

        try:
            file = codecs.open(self.p+'volume.txt', 'r', encoding='utf-8', errors='ignore')
            vol = file.readline()
            self.player.audio_set_volume(int(vol))
            self.volume.set(int(vol))
        except:
            file = codecs.open(self.p+'volume.txt', 'w', encoding='utf-8', errors='ignore')
            file.write('50')
            self.player.audio_set_volume(50)
            self.volume.set(50)
        file.close()

        self.loadPlaylists()

        master.mainloop()

    def bindActions(self, com):
        if com == 'pause':
                self.checkPause()
        elif com == 'rewind':
            if not self.playlist or self.stopped:
                return
            if len(self.alreadyPlayed) == 0:
                return
            elif len(self.alreadyPlayed) == 1:
                self.player.set_position(0.0)
            else:
                if self.player.get_time() > 5000:
                    self.player.set_position(0.0)
                else:
                    self.bindCommand = 'rewind'
        elif com == 'skip':
            if not self.playlist or self.stopped:
                return
            self.bindCommand = 'skip'
        elif com == 'volumeup':
            f = open(self.p+'volume.txt', 'r', encoding='utf-8', errors='ignore')
            volume = f.readline()
            f.close()
            f = open(self.p+'volume.txt', 'w', encoding='utf-8', errors='ignore')
            f.write(str(int(volume)+2))
            f.close()
            self.volume.set(self.volume.get()+2)
            self.VolAdj()
        elif com == 'volumedown':
            f = open(self.p+'volume.txt', 'r', encoding='utf-8', errors='ignore')
            volume = f.readline()
            f.close()
            f = open(self.p+'volume.txt', 'w', encoding='utf-8', errors='ignore')
            f.write(str(int(volume)-2))
            f.close()
            self.volume.set(self.volume.get()-2)
            self.VolAdj()

    def VolAdj(self, _=None):
        f = codecs.open(self.p+'volume.txt', 'w', errors='ignore')
        f.write(str(self.volume.get()))
        f.close()
        self.player.audio_set_volume(self.volume.get())

    def mainListener(self, key):
        f = codecs.open(self.p+'binds.txt', 'r', encoding='utf-8', errors='ignore')
        binds = f.readlines()
        f.close()
        for i in range(len(binds)):
            x = binds[i].split(':')
            if key.name == x[1].strip():
                self.bindActions(x[0].strip())
                break

    def loadM3UPlaylists(self):
        playlists = list(filedialog.askopenfilenames())
        if len(playlists) == 0:
            return
        temp = playlists[:]
        for i in temp:
            x = i.split('/')
            if x[-1].split('.')[-1] != 'm3u':
                playlists.remove(i)
        if len(playlists) == 0:
            messagebox.showinfo("Error!", "None of these files are .m3u!")
        listOfSongs = []
        for i in playlists:
            f = codecs.open(i, 'r', errors='ignore')
            songs = f.readlines()
            f.close()
            for song in songs:
                if os.path.exists(song.strip()):
                    listOfSongs.append(song.strip())
            self.music = self.getMusic(listOfSongs)
            self.insertMusic()

    def startRoot(self):
        subprocess.Popen('dist\\spotifyRoot\\spotifyRoot.exe')

    def makeImg(self, strng, com):
        b = MakeImage.MakeImage(strng, com)
        icon = b.getImage()
        icondata = base64.b64decode(icon)
        tempFile = strng
        iconfile = codecs.open(self.p+tempFile, 'wb', errors='ignore')
        iconfile.write(icondata)
        iconfile.close()

    def checkPtoP(self):
        if self.plList.size() == 0:
            return
        if self.notPlaying:
            self.automattic.config(image=self.stopimg)
            self.playButton.image = self.stopimg
            self.ptop = True
            self.change()
        elif not self.ptop:
            self.stop()
            self.ptop = True
            self.change()
            self.automattic.config(image=self.stopimg)
            self.playButton.image = self.stopimg
        else:
            self.stop()
            self.ptop = False
            self.automattic.config(image=self.ammimg)
            self.playButton.image = self.ammimg

    def checkPause(self):
        if self.notPlaying:
            if len(self.LB1.curselection()) != 1 and len(self.plList.curselection()) != 1:
                messagebox.showinfo("Error!", "Please select a song or playlist!")
                return
            if self.getSong():
                self.playButton.config(image=self.pauseimg)
                self.playButton.image = self.pauseimg
            return
        elif not self.stopped:
            self.player.pause()
            self.stopped = True
            self.playButton.config(image=self.playimg)
            self.playButton.image = self.playimg
        else:
            if self.ptop:
                self.player.play()
                self.stopped = False
                self.playButton.config(image=self.pauseimg)
                self.playButton.image = self.pauseimg
            else:
                tple1 = self.LB1.curselection()
                tple2 = self.plList.curselection()
                if len(self.LB1.curselection()) != 1 and len(self.plList.curselection()) != 1:
                    messagebox.showinfo("Error!", "Please select a song or playlist!")
                    return
                if len(tple1) == 0:
                    temp = self.plList.get(tple2[0])
                    playlist = temp.split(':')[1].strip()
                    if playlist == self.currentlyPlaying and not self.stopped:
                        self.player.pause()
                        self.stopped = True
                        self.playButton.config(image=self.playimg)
                        self.playButton.image = self.playimg
                    elif playlist == self.currentlyPlaying and self.stopped:
                        self.player.pause()
                        self.stopped = False
                        self.playButton.config(image=self.pauseimg)
                        self.playButton.image = self.pauseimg
                    else:
                        self.stop()
                        if self.getSong():
                            self.stopped = False
                            self.playButton.config(image=self.pauseimg)
                            self.playButton.image = self.pauseimg
                else:
                    if self.getSong():
                        self.stopped = False
                        self.playButton.config(image=self.pauseimg)
                        self.playButton.image = self.pauseimg

    def checkSongsInPL(self):
        tple = self.plList.curselection()
        if len(tple) != 1:
            messagebox.showinfo("Error!", "Please select one playlist!")
            return
        name = self.plList.get(tple[0]).split()[1]
        f = codecs.open(self.p+'playlists.csv', 'r', encoding='utf-8', errors='ignore')
        lines = f.readlines()
        f.close()
        self.music = []
        for line in lines:
            if name == line.split('|')[0]:
                self.LB1.delete(0, END)
                temp = line.split("|")[2:]
                for i in temp:
                    if i.strip() == "":
                        continue
                    self.music.append(i.strip())
                    i = i.split("\\")
                    self.LB1.insert(END, i[len(i)-1])
                return
        messagebox.showinfo("Error!", "No songs were found in this playlist!")

    def clear(self):
        self.LB1.delete(0, END)
        self.music = []
        self.currentlyPlaying = ""

    def addSongs(self):
        tple = self.plList.curselection()
        if len(tple) != 1:
            messagebox.showinfo("Error!", "Please select one playlist!")
            return
        files = list(filedialog.askopenfilenames())
        name = self.plList.get(tple[0]).split()[1]
        f = codecs.open(self.p+'playlists.csv', 'r', encoding='utf-8', errors='ignore')
        c = f.readlines()
        f.close()
        f = codecs.open(self.p+'playlists.csv', 'w', encoding='utf-8', errors='ignore')
        for i in c:
            if name == i.split('|')[0]:
                lst = i.split('|')
                newLst = lst[:2]
                for j in files:
                    for k in lst[2:]:
                        if j == k.strip():
                            files.remove(j)
                newLst.extend(files)
                newLst.extend(lst[2:])
                str = "|".join(newLst)
                f.write(str.replace('/', '\\'))
            else:
                f.write(i)
        f.close()
        self.loadPlaylists()

    def change(self):
        self.currentProcess = ""
        self.notPlaying = False
        self.stopped = False
        self.processToPlaylist()

    def fixRank(self):
        f = codecs.open(self.p+'playlists.csv', 'r', encoding='utf-8', errors='ignore')
        lines = f.readlines()
        f.close()
        f = codecs.open(self.p+'playlists.csv', 'w', encoding='utf-8', errors='ignore')
        index = 1
        for line in lines:
            temp = line.split("|")
            f.write(temp[0]+"|"+str(index)+"|"+"|".join(temp[2:]))
            index += 1
        f.close()


    def setRank(self, name):
        newRank = self.plRank.get()
        if newRank == "":
            messagebox.showinfo("Error!", "Please enter the intended playlist rank!")
            return
        try:
            newRank = int(newRank)
        except ValueError:
            messagebox.showinfo("Error!", "Please enter a number!")
            return
        f = codecs.open(self.p+"playlists.csv", "r", encoding='utf-8', errors='ignore')
        lst = f.readlines()
        f.close()
        if newRank < 1:
            newRank = 1
        elif newRank > len(lst):
            newRank = len(lst)
        oldRank = -1
        for line in lst:
            tempLst = line.split('|')
            if tempLst[0].strip() == name.strip():
                oldRank = int(tempLst[1].strip())
                break
        splitList = []
        for line in lst:
            splitList.append(line.split('|'))
        if oldRank == newRank:
            return
        elif oldRank < newRank:
            for i in range(newRank-oldRank+1):
                if i == 0:
                    splitList[oldRank-1][1] = str(newRank)
                else:
                    splitList[i+oldRank-1][1] = str(int(splitList[i+oldRank-1][1])-1)
        else:
            for i in range(oldRank-newRank+1):
                if i == 0:
                    splitList[oldRank-1][1] = str(newRank)
                else:
                    splitList[oldRank-1-i][1] = str(int(splitList[oldRank-1-i][1])+1)
        newList = []
        for line in splitList:
            newList.append('|'.join(line))
        tempLst = []
        i = 1
        b = 0
        while len(newList) != 0:
            t = newList[b].split('|')
            if int(t[1]) == i:
                tempLst.append(newList[b])
                del newList[b]
                i+=1
                b=0
            else:
                b+=1
        f = codecs.open(self.p+"playlists.csv", 'w', encoding='utf-8', errors='ignore')
        for i in tempLst:
            f.write(i)
        f.close()
        self.loadPlaylists()

    def deletePlaylist(self, name):
        f = codecs.open(self.p+"playlists.csv", "r", encoding='utf-8', errors='ignore')
        lines = f.readlines()
        f.close()
        f = codecs.open(self.p+"playlists.csv", "w", encoding='utf-8', errors='ignore')
        for line in lines:
            if name != line.split("|")[0]:
                f.write(line)
        f.close()
        self.loadPlaylists()

    def startTimer(self, str, arg):
        ti = threading.Timer(0.5, str, arg)
        ti.daemon = True
        ti.start()

    def processToPlaylist(self):
        f = codecs.open(self.p+'playlists.csv', encoding='utf-8', errors='ignore')
        tempList = []
        line = f.readline()
        while line != "":
            tempList.append(line.split("|")[0])
            line = f.readline()
        f.close()
        processes = self.getProcesses()
        for process in tempList:
            if self.notPlaying:
                return
            if process in processes:
                if process == self.currentProcess:
                    self.startTimer(self.processToPlaylist, ())
                    return
                else:
                    self.currentProcess = process
                    self.playPlaylist(process)
                    self.startTimer(self.processToPlaylist, ())
                    self.playButton.config(image=self.pauseimg)
                    self.playButton.image = self.pauseimg
                    return
            elif process == self.currentProcess:
                self.currentProcess = ""
                self.startTimer(self.processToPlaylist, ())
                return
        self.startTimer(self.processToPlaylist, ())

    def stop(self):
        if self.stopped:
            self.player.stop()
            return
        self.stopped = True
        self.notPlaying = True
        self.playButton.config(image=self.playimg)
        self.playButton.image = self.playimg
        self.player.stop()

    def checkStatus(self):
        if not self.playlist:
            if abs(self.player.get_time() - self.player.get_length()) >= 500:
                self.startTimer(self.checkStatus, ())
                return
            else:
                self.stop()
                self.currentlyPlaying = ""
                return
        if (not self.player.is_playing()==1 and not self.stopped):
            self.play()
        elif self.bindCommand=='skip':
            self.bindCommand = ''
            self.play()
        elif self.bindCommand=='rewind':
            self.bindCommand = ''
            self.currentPlaylist +=[self.alreadyPlayed.pop(), self.alreadyPlayed.pop()]
            self.play()
        elif not self.stopped:
            self.startTimer(self.checkStatus, ())

    def play(self):
        if len(self.currentPlaylist)==0:
            f = codecs.open(self.p+"playlists.csv", 'r', encoding='utf-8', errors='ignore')
            lines = f.readlines()
            f.close()
            for line in lines:
                if self.currentlyPlaying == line.split("|")[0]:
                    lst = line.split('|')
                    self.currentPlaylist = lst[2:]
        self.player.stop()
        tempSong = self.currentPlaylist.pop().strip()
        self.alreadyPlayed.append(tempSong)
        self.playlist = True
        if os.path.isfile(tempSong):
            media = self.instance.media_new_path(tempSong)
            self.player.set_media(media)
            self.player.play()
        self.stopped = False
        self.notPlaying = False
        self.startTimer(self.checkStatus, ())

    def playPlaylist(self, name):
        lst = []
        self.alreadyPlayed = []
        f = codecs.open(self.p+"playlists.csv", 'r', encoding='utf-8', errors='ignore')
        lines = f.readlines()
        f.close()
        for line in lines:
            if name == line.split("|")[0]:
                lst = line.split('|')
        self.currentlyPlaying = lst[0]
        self.currentPlaylist = lst
        del lst[1], lst[0]
        millis = int(round(time.time() * 1000))
        Random(millis).shuffle(lst)
        self.play()

    def findPlaylist(self, command):
        tple = self.plList.curselection()
        if len(tple) != 1:
            messagebox.showinfo("Error!", "Please select one playlist!")
            return
        name = self.plList.get(tple[0]).split(":")
        if command == 'play':
            self.playPlaylist(name[1].strip())
        elif command == 'del':
            self.deletePlaylist(name[1].strip())
        elif command == 'rank':
            self.setRank(name[1].strip())

    def processInList(self, pil):
        lst = []
        f = codecs.open(self.p+'playlists.csv', encoding='utf-8', errors='ignore')
        line = f.readline()
        while line != "":
            lst.append(line.split("|")[0])
            line = f.readline()
        f.close()
        if pil not in lst:
            return False
        return True

    def loadPlaylists(self):
        self.plList.delete(0, END)
        self.fixRank()
        f = codecs.open(self.p+'playlists.csv', "r", encoding='utf-8', errors='ignore')
        x = f.readlines()
        for line in x:
            self.plList.insert(END, line.split("|")[1]+": "+line.split('|')[0])
        f.close()


    def createPlaylist(self):
        songs = self.LB1.curselection()
        if len(songs) == 0:
            messagebox.showinfo("Error!", "Please select at least one song!")
            return
        if self.processName == "":
            messagebox.showinfo("Error!", "Please select a process!")
            return
        if self.processInList(self.processName):
            messagebox.showinfo("Error!", "There is already a playlist associated with this process!")
            self.processName = ""
            return
        lst = []
        for song in songs:
            lst.append("|"+self.music[song])
        if len(lst) != 0:
            f = codecs.open(self.p+"playlists.csv", "r", encoding='utf-8', errors='ignore')
            numLines = len(f.readlines())+1
            f.close()
            f = codecs.open(self.p+"playlists.csv", "a", encoding='utf-8', errors='ignore')
            f.write(self.processName+'|'+str(numLines))
            for i in lst:
                f.write(i)
            f.write("\n")
            f.close()
        self.loadPlaylists()

    def setProcess(self, processpath):
        pathlist = processpath.split('/')
        self.processName = pathlist[len(pathlist)-1]
        if not self.processName.endswith(".exe") and self.processName != "":
            messagebox.showinfo("Error!", "Please select a '.exe' file!")
            self.processName=""
        if self.processInList(self.processName):
            messagebox.showinfo("Error!", "There is already a playlist associated with this process!")
            self.processName=""
        self.L2.configure(text=""+self.processName)

    def playSong(self, str):
        if os.path.isfile(str):
            self.stopped = False
            self.notPlaying = False
            media = self.instance.media_new_path(str)
            self.player.set_media(media)
            self.currentlyPlaying = str
            self.player.play()
            self.startTimer(self.checkStatus, ())
            return True
        else:
            self.currentlyPlaying = ""
            messagebox.showinfo("Error!", str+" does not exist!")
            return False

    def getSong(self):
        songTuple = self.LB1.curselection()
        playlistTuple = self.plList.curselection()
        if len(songTuple) != 1 and len(playlistTuple) != 1:
            messagebox.showinfo("Error!", "Please select one song or playlist!")
            return ""
        if len(playlistTuple) == 0:
            if self.currentlyPlaying == self.music[songTuple[0]]:
                self.player.pause()
                return True
            self.playlist = False
            return self.playSong(self.music[songTuple[0]])
        else:
            self.findPlaylist('play')
            return True

    def filePath(self, tempPath):
        try:
            self.path = tempPath
            self.sendPath(tempPath)
        except FileNotFoundError:
            pass

    def getProcesses(self):
        processes = []
        for process in psutil.process_iter(attrs=['pid', 'name']):
            processes.append(process.info['name'])
        return processes

    def getMusic(self, listOfFiles):
        temp = listOfFiles[:]
        for i in listOfFiles:
            if i in self.music:
                temp.remove(i)
                continue
            tempList = i.split(".")
            if len(tempList) == 1:
                temp.remove(i)
            elif tempList[len(tempList)-1] not in self.listOfMusicTypes:
                temp.remove(i)
        return self.music+temp

    def insertMusic(self):
        self.LB1.delete(0, END)
        for line in self.music:
            temp = line.split('\\')
            self.LB1.insert(END, temp[len(temp)-1])

    def sendPath(self, string):
        if string == "":
            return
        folders = string.split('\\')
        length = len(folders[-1])+1
        while length > 36:
            x = folders[-1].split('/')
            length = len(''.join(x[:len(x)-1]))
            folders[-1] = '/'.join(x[:len(x)-1])
        if folders[-1] == string:
            self.L1.configure(text=""+folders[-1]+'/')
            ToolTip(self.L1, self.path)
        else:
            self.L1.configure(text=""+folders[-1]+'/...')
            ToolTip(self.L1, self.path)
        listOfFiles = []
        for i in [x[0] for x in os.walk(string)]:
            for j in os.listdir(i):
                j = str(bytes(j, 'utf-8').decode('utf-8', 'ignore'))
                listOfFiles.append(i.replace('/', '\\')+'\\'+j)
        self.music = self.getMusic(listOfFiles)
        self.insertMusic()

if __name__=='__main__':
    AutoMatticMusic()
