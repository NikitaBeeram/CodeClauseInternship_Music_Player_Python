from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()
root.title("Music Player")
root.iconbitmap("images\\music_player.ico")
root.resizable(height=False, width=False)
root.geometry("420x360+100+100")
root.configure(bg="white")
#Initialize Pygame Mixer
pygame.mixer.init()

def add_a_Song():
    song = filedialog.askopenfilename(initialdir='C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs',title="Choose a Song",filetypes=(("mp3 Files", "*.mp3"), ))
    song = song.replace("C:/Users/HP/OneDrive/Desktop/niki/tkinter/songs/","")
    song = song.replace(".mp3", "")
    playlistBox.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs',title="Choose a Song",filetypes=(("mp3 Files", "*.mp3"), ))

    for song in songs:
        song = song.replace("C:/Users/HP/OneDrive/Desktop/niki/tkinter/songs/","")
        song = song.replace(".mp3", "")
        playlistBox.insert(END, song)

def delete_a_song():
    stop()
    playlistBox.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    playlistBox.delete(0,END)
    pygame.mixer.music.stop()

def play_time():
    if stopped:
        return
    currentTime = pygame.mixer.music.get_pos() / 1000
    convertedTime = time.strftime('%M:%S', time.gmtime(currentTime))

    #SliderLabel.config(text=f'Slider: {int(SongSlider.get())} and Song Pos: {int(currentTime)}')

    song = playlistBox.get(ACTIVE)
    song = f'C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs\\{song}.mp3'
    songMut = MP3(song)
    global songLength
    songLength = songMut.info.length
    convertedLength = time.strftime('%M:%S', time.gmtime(songLength))

    currentTime = int(currentTime)+1
    if int(SongSlider.get()) == int(songLength):
        statusBar.config(text=f'{convertedLength}')
    elif paused:
        pass
    elif int(SongSlider.get()) == int(currentTime):
        sliderPosition = int(songLength)
        SongSlider.config(to=sliderPosition, value=int(currentTime))
    else:
        sliderPosition = int(songLength)
        SongSlider.config(to=sliderPosition, value=int(SongSlider.get()))
        convertedTime = time.strftime('%M:%S', time.gmtime(int(SongSlider.get())))
        statusBar.config(text=f'{convertedTime}/{convertedLength}')
        nextTime = int(SongSlider.get()) + 1
        SongSlider.config(value=nextTime)


    #SongSlider.config(value=int(currentTime))

    statusBar.after(1000,play_time)

def play():
    global stopped
    stopped = False
    song = playlistBox.get(ACTIVE)
    song = f'C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs\\{song}.mp3'

    SongSlider.config(value=0)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    play_time()

global stopped
stopped = False
def stop():
    pygame.mixer.music.stop()
    playlistBox.selection_clear(ACTIVE)

    statusBar.config(text='')
    SongSlider.config(value=0)

    global stopped
    stopped = True

global paused
paused = False 
def pause(is_paused):
    global paused
    paused = is_paused
    if paused == False:
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

def next_song():
    statusBar.config(text='')
    SongSlider.config(value=0)

    nextSong = playlistBox.curselection()
    nextSong = nextSong[0] + 1
    song = playlistBox.get(nextSong)
    song = f'C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs\\{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlistBox.selection_clear(0,END)
    playlistBox.activate(nextSong)
    playlistBox.selection_set(nextSong,last=None)

def prev_song():
    statusBar.config(text='')
    SongSlider.config(value=0)

    prevSong = playlistBox.curselection()
    prevSong = prevSong[0] - 1
    song = playlistBox.get(prevSong)
    song = f'C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs\\{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlistBox.selection_clear(0,END)
    playlistBox.activate(prevSong)
    playlistBox.selection_set(prevSong,last=None)

def slide(a):
    song = playlistBox.get(ACTIVE)
    song = f'C:\\Users\\HP\\OneDrive\\Desktop\\niki\\tkinter\\songs\\{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(SongSlider.get()))

def volume(x):
    pygame.mixer.music.set_volume(VolumeSlider.get())

    currentVolume = pygame.mixer.music.get_volume()
    currentVolume = currentVolume * 100

    if currentVolume < 1:
        volumeMeter.config(image=Volume_no)
    elif currentVolume > 1 and currentVolume <= 25:
        volumeMeter.config(image=Volume_0)
    elif currentVolume > 25 and currentVolume <= 50:
        volumeMeter.config(image=Volume_1)
    elif currentVolume > 50 and currentVolume <= 75:
        volumeMeter.config(image=Volume_2)
    else:
        volumeMeter.config(image=Volume_3)

#Create Playlist Box
playlistBox = Listbox(root, bg="black", fg="pink", width=50, selectbackground="gray", selectforeground="blue3")
playlistBox.grid(row=0, column=0, columnspan=7, pady=10,padx=10)

back_button_img = PhotoImage(file="images\\backward_button.png")
play_button_img = PhotoImage(file="images\\play_button.png")
pause_button_img = PhotoImage(file="images\\pause_button.png")
stop_button_img = PhotoImage(file="images\\stop_button.png")
forward_button_img = PhotoImage(file="images\\forward_button.png")

global Volume_no
global Volume_0
global Volume_1
global Volume_2
global Volume_3

Volume_no = PhotoImage(file="images\\volumeno.png")
Volume_0 = PhotoImage(file="images\\volume0.png")
Volume_1 = PhotoImage(file="images\\volume1.png")
Volume_2 = PhotoImage(file="images\\volume2.png")
Volume_3 = PhotoImage(file="images\\volume3.png")


controls_frame = Frame(root)
controls_frame.grid(row=1, column=1, columnspan=7)  

volumeMeter = Label(root, image=Volume_3,bg="white")
volumeMeter.grid(row=1, column=7, sticky="ew")

back_button = Button(root, image=back_button_img, borderwidth=0,padx=0,pady=0,bg="white",  command=prev_song)
play_button = Button(root, image=play_button_img, borderwidth=0,padx=0,pady=0,bg="white", command=play)
pause_button = Button(root, image=pause_button_img, borderwidth=0,padx=0,pady=0,bg="white", command=lambda: pause(paused))
stop_button = Button(root, image=stop_button_img, borderwidth=0,padx=0,pady=0,bg="white", command=stop)
forward_button = Button(root, image=forward_button_img,padx=0,pady=0,bg="white", borderwidth=0, command=next_song)

back_button.grid(row=1, column=1)
play_button.grid(row=1, column=3)
pause_button.grid(row=1, column=4)
stop_button.grid(row=1, column=5)
forward_button.grid(row=1, column=2)

myMenu = Menu(root)
root.config(menu=myMenu)

addSong = Menu(myMenu)
myMenu.add_cascade(label="Add Songs", menu=addSong)
addSong.add_command(label="Add a Song to playlist", command=add_a_Song)
addSong.add_command(label="Add many Songs to playlist", command=add_many_songs)

deleteSong = Menu(myMenu)
myMenu.add_cascade(label="Delete Songs", menu=deleteSong)
deleteSong.add_command(label="Delete Song from playlist", command=delete_a_song)
deleteSong.add_command(label="Delete all Songs from playlist", command=delete_all_songs)

statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E,width=59)
statusBar.grid(row=4, column=0, columnspan=8, sticky="ew")

SongSlider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide,length=250)
SongSlider.grid(row=2, column=1, columnspan=7,padx=10, sticky="ew",pady=20)

volume_frame = LabelFrame(root,text="    Volume", padx=5, pady=5, bd=1, relief=RAISED)
volume_frame.grid(row=0, column=7, sticky="ew", padx=10)

VolumeSlider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=130)
VolumeSlider.pack(fill=BOTH, expand=True)

root.mainloop()