import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import pygame
import os
import time
import random


class MusicPlayer:
    def __init__(self, root):
        # INITIALIZING TKINTER
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x500")
        self.root.configure()
        self.root.resizable(0, 0)  # Disable Resizing Window

        self.INITIAL_DIR = "YOUR_DIR_THAT_CONTAINS_MUSIC_FILES_WITH_WAV_EXTENSION"

        # INITIALIZING PYGAME MIXER
        self.mixer = pygame.mixer
        self.mixer.init()

        self.track_list = []  # List of Tracks
        self.song_name = ""  # Current Song Name

        # Track Index, Track Pause, Current Index
        self.track_index, self.track_pause, self.current_index = 0, 0, 0

    def __loadImages(self):
        ''' IMAGES '''

        self.play_img = PhotoImage(file="images/play_btn.png")
        self.play_img = self.play_img.subsample(60, 60)

        self.pause_img = PhotoImage(file="images/pause_btn1.png")
        self.pause_img = self.pause_img.subsample(20, 20)

        self.next_img = PhotoImage(file="images/next_btn.png")
        self.next_img = self.next_img.subsample(20, 20)

        self.prev_img = PhotoImage(file="images/prev_btn.png")
        self.prev_img = self.prev_img.subsample(20, 20)

        self.shuffle_img = PhotoImage(file="images/shuffle_btn.png")
        self.shuffle_img = self.shuffle_img.subsample(20, 20)

        self.bg_img = PhotoImage(file="images/bg4.png")

    def __loadWidgets(self):
        '''BACKGROUND'''
        self.label = tk.Label(self.root, image=self.bg_img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        ''' BUTTONS '''

        # Open Button
        self.open_btn = tk.Button(
            self.root, text="Open", command=self.__openFile)
        self.open_btn.place(relx=0.01, rely=0.01, anchor='nw')

        # Previous Button
        self.prev_btn = tk.Button(self.root, command=self.__prevMusic,
                                  image=self.prev_img, borderwidth=0, compound=tk.CENTER)
        self.prev_btn.place(x=196, y=410)

        # Pause Button
        self.pause_btn = tk.Button(self.root, command=self.__pauseMusic,
                                   image=self.pause_img, borderwidth=0, compound=tk.CENTER)
        self.pause_btn.place(x=235, y=410)

        # Next Button
        self.next_btn = tk.Button(self.root, command=self.__nextMusic,
                                  image=self.next_img, borderwidth=0, compound=tk.CENTER)
        self.next_btn.place(x=275, y=410)

        # Shuffle Button
        self.shuffle_btn = tk.Button(self.root, command=self.__shuffleMusic,
                                     image=self.shuffle_img, borderwidth=0, compound=tk.CENTER)
        self.shuffle_btn.place(x=235, y=450)

        ''' LABELS '''

        # Current Song Label
        self.current_song = tk.Label(
            self.root, font=("Consolas", 10), fg="white", bg="black")
        self.current_song.place(x=0, y=480)

        ''' TRACKS '''

        # Music List
        self.music_list = tk.Listbox(self.root, width=50, height=10, font=(
            "Consolas", 10), fg="black", bg="white", selectmode='SINGLE')
        self.music_list.place(x=75, y=175)

        # Select Music
        self.music_list.bind('<<ListboxSelect>>', self.__selectMusic)

    # Get tracks from directory
    def __trackList(seFILES_WITH, track_path="YOUR_DIR_THAT_CONTAINS_MUSIC_AS_WAV_EXTENSION"):
        self.track_list = [music for music in os.listdir(
            track_path) if music.endswith(".wav")]
        self.__insertIntoList()
        return self.track_list

    # Insert tracks into listbox
    def __insertIntoList(self):
        for music in self.track_list:
            self.music_list.insert(tk.END, music[:-4])

    # Get selected music
    def __selectMusic(self, temp):
        self.selected = self.music_list.get(
            self.music_list.curselection()) + ".wav"
        file_name = self.INITIAL_DIR + "/" + self.selected
        song_name = self.selected
        self.track_index = self.track_list.index(song_name)
        self.current_index = self.track_index
        self.__playMusic(file_name, song_name)
        self.__queueMusic(song_name)

    # Play Music
    def __playMusic(self, file_name, song_name):
        self.mixer.music.load(file_name)
        self.mixer.music.play()
        self.current_song.configure(text=f"Current Song: {song_name[:-4]}")

    # Make Queue of Musics that are in track_list
    def __queueMusic(self, song_name):
        track_index = self.track_list.index(song_name)
        if (track_index) == len(self.track_list) - 1:
            track_index = 0
            self.queued_list = self.track_list[track_index:]
        else:
            self.queued_list = self.track_list[track_index +
                                               1:] + self.track_list[:track_index]

    # Refreshes list box
    def __delList(self):
        self.music_list.delete(0, tk.END)

    # Open .wav file
    def __openFile(self):
        file_name = filedialog.askopenfilename(
            initialdir=self.INITIAL_DIR, title="Select File", filetypes=(("Wav Files", "*.wav"), ("All Files", "*.*")))

        if file_name == "":
            pass
        else:
            file_name_split = file_name.split("/")
            song_name = file_name_split.pop()
            track_path = "/".join(file_name_split)
            self.track_list = self.__trackList(track_path)
            self.__delList()
            self.__insertIntoList()

    # Unpause Music
    def __unpauseMusic(self):
        self.mixer.music.unpause()
        self.pause_btn.configure(image=self.pause_img)

    # Pause Music
    def __pauseMusic(self):
        self.track_pause += 1
        if self.track_pause % 2 == 0:
            self.__unpauseMusic()
        else:
            self.mixer.music.pause()
            self.pause_btn.configure(image=self.play_img)

    # Next Music
    def __nextMusic(self):
        self.c_selected = self.music_list.get(
            self.music_list.curselection()) + ".wav"
        self.current_index = self.track_list.index(self.c_selected)
        self.music_list.selection_clear(self.current_index, tk.END)

        song_name = self.queued_list[0]
        file_name = "YOUR_DIR_THAT_CONTAINS_MUSIC_FILES_WITH_WAV_EXTENSION/" + song_name
        self.__queueMusic(song_name)
        self.__playMusic(file_name, song_name)
        idx = self.track_list.index(song_name)
        self.music_list.select_set(idx)
        if self.track_pause % 2 != 0:
            self.pause_btn.configure(image=self.pause_img)

    # Previous Music
    def __prevMusic(self):
        self.c_selected = self.music_list.get(
            self.music_list.curselection()) + ".wav"
        self.current_index = self.track_list.index(self.c_selected)
        self.music_list.selection_clear(self.current_index, tk.END)

        self.track_index = self.track_list.index(self.c_selected)
        self.track_index -= 1
        if self.track_index < 0:
            self.track_index = len(self.track_list) - 1

        song_name = self.track_list[self.track_index]
        file_name = "YOUR_DIR_THAT_CONTAINS_MUSIC_FILES_WITH_WAV_EXTENSION/" + song_name
        idx = self.track_list.index(song_name)

        self.__queueMusic(song_name)
        self.__playMusic(file_name, song_name)
        self.music_list.select_set(idx)
        if self.track_pause % 2 != 0:
            self.pause_btn.configure(image=self.pause_img)

    # Shuffle Music inside track_list
    def __shuffleMusic(self):
        self.c_selected = self.music_list.get(
            self.music_list.curselection()) + ".wav"
        self.current_index = self.track_list.index(self.c_selected)
        self.music_list.selection_clear(self.current_index, tk.END)

        random.shuffle(self.track_list)
        self.track_index = 0
        song_name = self.track_list[self.track_index]
        file_name = "YOUR_DIR_THAT_CONTAINS_MUSIC_FILES_WITH_WAV_EXTENSION/" + song_name
        idx = self.track_list.index(song_name)

        self.__playMusic(file_name, song_name)
        self.__delList()
        self.__queueMusic(song_name)
        self.__insertIntoList()
        self.music_list.select_set(idx)
        if self.track_pause % 2 != 0:
            self.pause_btn.configure(image=self.pause_img)

    def start(self):
        self.__loadImages()
        self.__loadWidgets()
        self.track_list = self.__trackList()
        self.root.mainloop()


window = tk.Tk()
music_player = MusicPlayer(root=window)
music_player.start()
