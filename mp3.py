from tkinter import *
import pygame
import os
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('MP3 Player')
root.iconbitmap('./images/mp3Icon.png')
root.geometry("500x400")

# Initialize PyGame Mixer
pygame.mixer.init() # Initializes the mixer module for Sound loading and playback

# Grab Song Length Time Info
def play_time():
    # Check for double timing
    if stopped:
        return

    # Grab Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos()//1000 # Get current position of the song in milliseconds

    # Throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')

    # Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time)) 

    # Grab song title from playlist
    song = song_box.get(ACTIVE)
    # Add directory structure and mp3 to song title
    if song in songNames: # This if statement was created in order to fix dictionary error when deleting songs
        song = f'{songNames[song]}'
    
        # Load song with mutagen
        song_mut = MP3(song)
        # Get song length
        global song_length
        song_length = song_mut.info.length 
        # Convert to Time Format
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length)) 

        # Increase current time by 1 second
        current_time += 1

        if int(my_slider.get()) == int(song_length):
            # If end of song reached, dont do anything
            status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}    ')
        elif paused:
            pass
        elif int(my_slider.get()) == int(current_time):
            # slider hasn't moved
            # Update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=int(current_time)) # Start value at zero for slider whenever play button is pressed
        else:
            # slider has been moved 
            # Update slider to position
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=int(my_slider.get())) # Start value at zero for slider whenever play button is pressed      

            # Convert to time format
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

            # Output time to status bar
            status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}    ') # Output onto the status bar

            # Move this thing along by one second
            next_time = int(my_slider.get()) + 1
            my_slider.config(value=next_time)

    # Output time to status bar
    # status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}    ') # Output onto the status bar
    
    # Update slider position value to current song position...
    # my_slider.config(value = int(current_time))
    
    # update time
    status_bar.after(1000, play_time)


# Initialize dictionary that will hold song name file directories
global songNames
songNames = {}

# Add Song Function
def add_song():
    global songNames
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),)) 
    # opens file dialog window to find song user wants to play

    temp = song # temporary variable that will hold full file directory path
    # Strip out the directory info and .mp3 extension from the song name
    song = os.path.basename(song) # removes file path info and keeps base file name
    song = song.replace(".mp3", "") # removes extension
    songNames[song] = temp # place full file directory path inside dictionary
    song_box.insert(END, song) #inserts to the end of the list box
    """ -------------------------------------------------------------------------------""" 

# Add many songs to playlist
def add_many_songs():
    global songNames
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),)) 
    # askopenfilenames will return a list so we need to loop through the list

    # Loop thru song list and replace directory info and mp3
    for song in songs:
            temp = song # temporary variable that will hold full file directory path
            # Strip out the directory info and .mp3 extension from the song name
            song = os.path.basename(song) # removes file path info and keeps base file name
            song = song.replace(".mp3", "") # removes extension
            songNames[song] = temp # place full file directory path inside dictionary
            song_box.insert(END, song) #inserts to the end of the list box

# Play selected song 
def play():
    # Set stopped variable to false so song can play
    global stopped
    stopped = False
    song = song_box.get(ACTIVE) # This will retrieve the song that is selected/highlighted => ACTIVE
    # ACTIVE = thing that was clicked
    song = f'{songNames[song]}' # string literal
    
    pygame.mixer.music.load(song) # Will load the song
    pygame.mixer.music.play(loops=0) # Will play the song

    # Call the play_time function to get song length
    play_time()

    # Update slider to position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0) # Start value at zero for slider whenever play button is pressed


# Stop playing current song
global stopped 
stopped = False
def stop():
    # Reset slider and status bar 
    status_bar.config(text='')
    my_slider.config(value=0)

    # Stop song form playing 
    pygame.mixer.music.stop() # Stop the music that is currently playing
    song_box.selection_clear(ACTIVE) # Unselects the current selection in the Listbox

    # Clear the status bar
    status_bar.config(text='')

    # Set stop variable to true
    global stopped
    stopped = True

# Play the next song in the playlist
def next_song():
    # Reset slider and status bar 
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number 
    next_one = song_box.curselection() # Will give us current song playing in playlist as a tuple number
    """ MIGHT WANT TO print(next_one) TO SHOW WHAT IT LOOKS LIKE and use next_one[0] to get value"""
    """ e.g. print(next_one) and print(next_one[0]) """
    # Add one to the current song number
    next_one = next_one[0] + 1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'{songNames[song]}'
    # Load and play song
    pygame.mixer.music.load(song) # Will load the song
    pygame.mixer.music.play(loops=0) # Will play the song

    """ At this point show how the next button play the next song but wont play the song after that """
    """ The following code will fix this ... """

    # Move active bar in playlist listbox by clearing the current one and selecting the next one
    song_box.selection_clear(0, END) # Clear all of the song titles
    
    # Activate new song bar
    song_box.activate(next_one) 

    # Set Active Bar to Next Song
    song_box.selection_set(next_one, last=None)

# Play previous song in playlist
def previous_song():
    # Reset slider and status bar 
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number 
    next_one = song_box.curselection() # Will give us current song playing in playlist as a tuple number

    # Subtract one to the current song number
    next_one = next_one[0] - 1
    # Grab song title from playlist
    song = song_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'{songNames[song]}'
    # Load and play song
    pygame.mixer.music.load(song) # Will load the song
    pygame.mixer.music.play(loops=0) # Will play the song

    # Move active bar in playlist listbox by clearing the current one and selecting the next one
    song_box.selection_clear(0, END) # Clear all of the song titles
    
    # Activate new song bar
    song_box.activate(next_one) 

    # Set Active Bar to Next Song
    song_box.selection_set(next_one, last=None)

# Delete A Song
def delete_song():
    stop()
    # Get currently playing song
    song = song_box.get(ANCHOR)
    songNames.pop(song) # Remove from dictionary

    song_box.delete(ANCHOR) # A song that is highlighted is the ANCHORED song
    pygame.mixer.music.stop()

  
# Delete All Songs from Playlist
def delete_all_songs():
    stop()
    songNames.clear() # removes all items from dictionary 
    # Delete All Songs
    song_box.delete(0, END) # delete() uses a range, so we are deleting all the elements in the listbox
    # Stop Music if its playing
    pygame.mixer.music.stop()


# Create Global Pause Variable
global paused
paused = False

# Pause and unpause the current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE) # This will retrieve the song that is selected/highlighted => ACTIVE
    # ACTIVE = thing that was clicked
    song = f'{songNames[song]}' # string literal
    
    pygame.mixer.music.load(song) # Will load the song
    pygame.mixer.music.play(loops=0, start=int(my_slider.get())) # Will play the song

# Create Volume Function
def volume(x): 
    pygame.mixer.music.set_volume(volume_slider.get())

# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Create Playlist Box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0) 
# This "puts it on the screen"  ... pady is external padding on y axis.
# When you .pack() a widget into a window, Tkinter sizes the windows as
# small as it can while fully encompassing the widget



"""
The Listbox widget is used to display a list of items from 
which a user can select a number of items.

The first argument gets passed the root.

The second argument bg stands for "background color".

Third argument fg stands for "foreground color", i.e. the text color.

The width of the widget in characters. The default is 20

The fifth argument selectbackground is the background color when the item is selected 

The sixth argument selectforeground is the foreground color (color of the text when the item is selected)

*** What is a widget ***

Tkinter provides various controls, such as buttons, labels and text boxes 
used in a GUI application. These controls are commonly called widgets.

"""

""" ---------------------------------------------------------------------- """

# Define Player Control Button Images
back_btn_img = PhotoImage(file='./images/back50.png') # Displays images in the widget
forward_btn_img = PhotoImage(file='./images/forward50.png') # Displays images in the widget
play_btn_img = PhotoImage(file='./images/play50.png') # Displays images in the widget
pause_btn_img = PhotoImage(file='./images/pause50.png') # Displays images in the widget
stop_btn_img = PhotoImage(file='./images/stop50.png') # Displays images in the widget

# Create Player Control Frame
controls_frame = Frame(master_frame) # Frame works as a container for grouping widgets
controls_frame.grid(row=1, column=0, pady=20)

# Create Volume Label Frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

 #.grid() organizes widgets into a table-like structure in the parent widget
back_button.grid(row=0, column=0, padx=10) 
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10) 
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root) # This widget allows us to create all kinds of menus
root.config(menu=my_menu) # Sets menu to my_menu
# .config() is used to access an object's attributes after its initialisation

# Add Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
# .add_cascade() creates new hierarchical menu by associating a given menu to a parent menu
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song) # once pressed, run add_song()
# Add many songs to the playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs) # once pressed, run add_song()
""" ----------------------------------------------------------------- """
""" At this point add_song hasn't been created, so go create add_song """

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2) 
# packs the widget into the app and fills the entire space assigned to it

# Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360) # Creates the slider
my_slider.grid(row=2, column=0, pady=10)

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125) # Creates the slider
volume_slider.pack(pady=10)

# Create Temporary Slider Label
# slider_label = Label(root,text="0")
# slider_label.pack(pady=10)

"""
    Text argument will be what the label of the text will be
    bd stands for border width
    relief will give the outline a GROOVE outline
    anchor of East will anchor the text to the right side of the app
"""

root.mainloop() 
# This Tkinter method runs an infinite loop which listens for events
# i.e. button clicks or keypresses

