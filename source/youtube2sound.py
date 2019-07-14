from __future__ import unicode_literals
import urllib.parse, urllib.request
import re
import youtube_dl
import subprocess
import os

class Youtube2Sound:
    def __init__(self, songs, tple):
        self.songs = songs
        self.tple = tple
        self.songs = self.remove()
        self.p = os.getenv('APPDATA')
        self.p+='\\AutoMattic Music\\'
        self.dlsongs()

    def dlsongs(self):
        if len(self.tple) == 0:
            return
        for i in self.songs:
            name = i[0]
            del i[0]
            for j in i:
                self.opts = {
                'format' : 'bestaudio[ext=m4a]',
                'extractaudio' : True,
                'outtmpl' : self.p+'Music\\{}\\{}.m4a'.format(name, j),
                'noplaylist' : True
                }
                self.video = self.searchyt(j)
                try:
                    self.download(self.video, self.opts)
                except youtube_dl.utils.SameFileError:
                    print('Passing...', j)
        subprocess.Popen('echo Music saved in {}Music\\{}'.format(self.p, name), shell=True)

    def searchyt(self, j):
        self.query_string = urllib.parse.urlencode({ 'search_query' : j})
        self.url = "http://www.youtube.com/results?" + self.query_string + '+lyrics+'
        self.req = urllib.request.Request(self.url)
        self.html_content = urllib.request.urlopen(self.url)
        self.search_results = re.findall(r'href=\"\/watch\?v=(.{11})', self.html_content.read().decode())
        return "http://www.youtube.com/watch?v="+self.search_results[0]

    def download(self, video, opts):
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([video])

    def remove(self):
        self.temp = []
        for i in range(len(self.songs)):
            if i in self.tple:
                self.temp.append(self.songs[i])
        return self.temp
