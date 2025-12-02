from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import subprocess, webbrowser, os

#window setup
window = tk.Tk()
window.title("ffmpeg photosensitivity GUI")
window.iconbitmap("icon.ico")

global filename #kinda just used to transfer between file dialog/text box
global ffmpegPath
global ffPresent
ffmpegPath = 'No path'
ffPresent = 0

#
# target video button
#

#total label
targetVideoLbl = tk.Label(window, text="Target Video:")
targetVideoLbl.grid(column=0, row=0, sticky="w")

#browse text box
targetTxt = tk.Text(window, height=1, width=50, wrap="none")
targetTxt.grid(column=0, row=1)

#browse button
def loadVideoClick():
    filename = tk.filedialog.askopenfilename()
    #print(filename)
    targetTxt.delete("1.0",tk.END)
    targetTxt.insert("1.0",filename) #it doesnt update var filename when you type, so be sure to read from textbox not var
    
targetButton = tk.Button(window, text="Browse...", command = loadVideoClick)
targetButton.grid(column=1, row=1)

#
# desination video button
#

#total label
destVideoLbl = tk.Label(window, text="Destination Video:")
destVideoLbl.grid(column=0, row=2, sticky="w")

#browse text box
destTxt = tk.Text(window, height=1, width=50, wrap="none")
destTxt.grid(column=0, row=3)

#browser button
def saveVideoClick():
    filename = tk.filedialog.asksaveasfilename()
    #print(filename)
    destTxt.delete("1.0",tk.END)
    destTxt.insert("1.0",filename) #see load video

destButton = tk.Button(window, text = "Browse...", command = saveVideoClick)
destButton.grid(column=1, row=3)

#
# parameter set
#

#reachin my threshold
thresholdLbl = tk.Label(window, text="Threshold:")
thresholdLbl.grid(column=0, row=4, sticky="w")

thresholdIn = ttk.Spinbox(window, from_=0, to=float('inf'), increment=0.1, width=6)
thresholdIn.grid(column=1, row=4)
thresholdIn.insert(0,1.0)

#fps
fpsLbl = tk.Label(window, text="Framerate:")
fpsLbl.grid(column=0, row=5, sticky="w")

fpsIn = ttk.Spinbox(window, from_=0, to=float('inf'), width=6)
fpsIn.grid(column=1, row=5)
fpsIn.insert(0,30)

#skip
skipLbl = tk.Label(window, text="Skip pixels:")
skipLbl.grid(column=0, row=6, sticky="w")

skipIn = ttk.Spinbox(window, from_=1, to=1024, width=6)
skipIn.grid(column=1, row=6)
skipIn.insert(0,1)

#
# ok lets actually do the thing
#

def gatherInfo():
    global currentParams
    skipTemp = float(skipIn.get())
    skipIn.set(round(skipTemp))
    if (int(skipIn.get()) < 1):
        skipIn.set(1)
    if (int(skipIn.get()) > 1024) :
        skipIn.set(1024)
    currentParams = (
        thresholdIn.get(),
        fpsIn.get(),
        skipIn.get()
        )
    global currentLocations
    currentLocations = (
        targetTxt.get(1.0,str(tk.END)+"-1c"),
        destTxt.get(1.0,str(tk.END)+"-1c")
        )


def informOfCommand():
    global ffPresent #0: not found   1: found by default   2: found at specified location
    ffPresent = 0
    print("\n\nGUI: Trying to find ffmpeg... \n\n")
    try:
        subprocess.run("ffmpeg")
        ffPresent = 1
    except:
        try:
            subprocess.run(str(ffmpegPath))
            ffPresent = 2
        except:
            print("ffmpeg found at: " + str(ffmpegPath))
    if (ffPresent == 0):
        return (False,"I can't find ffmpeg. Locate it in the File menu for me, pretty please?")
        
        
    if (currentLocations[0] == ''):
        return (False,"Please set a Target Video path.\n(What video should I use?)")
    else:
        if not (os.path.isfile(currentLocations[0])):
            return (False,"I couldn't find the file you pointed me to. Did you mistype it? Does it still exist?")

    if (currentLocations[1] == ''):
        return (False,"Please set a Destination Video path.\n(Where do you want me to save the filtered video?)")
    else:
        if not (os.path.isfile(currentLocations[0])):
            return (False,"I couldn't find the file you pointed me to. Did you mistype it? Does it still exist?")

    
    return (True,"All systems go! Let's filter!")
    

def makeCommand():
    global ffPresent
    appearError = "\"This message should not appear. If it does, it's a bug.\"\nPlease make an issue on GitHub. (andrewkehoe/ffmpeg-photosensitivity-gui)\nI apologize for the inconvinience."
    print("ffPresent found: " + str(ffPresent))
    print("\n\nGUI: Trying to run... \n\n")
    if ffPresent == 1:
        try:
            com = "ffmpeg -i " + "\"" + currentLocations[0] + "\" -y" + " -filter:v photosensitivity=threshold=" + currentParams[0] + ":frames=" + currentParams[1] + ":skip=" + currentParams[2] + " \"" + currentLocations[1] + "\"" #could maybe append beginning instead of having two separate ones to maintain
            print(com)
            subprocess.run(com)
        except:
            print("makeCommand default ffmpeg branch")
            tk.messagebox.showerror("Oops...", message=appearError)
    elif ffPresent == 2:
        try:
            com = str((ffmpegPath) + " -i " + "\"" + currentLocations[0] + "\" -y" +  " -filter:v photosensitivity=threshold=" + currentParams[0] + ":frames=" + currentParams[1] + ":skip=" + currentParams[2] + " \"" + currentLocations[1] + "\"")
            print(com)
            subprocess.run(com)
        except:
            print("makeCommand ffmpegPath branch")
            tk.messagebox.showerror("Oops...", message=appearError)
    else:
        print("makeCommand else branch")
        tk.messagebox.showerror("Oops...", message=appearError)

#
# menu bar
#

#init
menubar = tk.Menu(window)
window.config(menu=menubar)

#file bar
fileMenu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=fileMenu)

def saveProfClick():
    filename = tk.filedialog.asksaveasfilename(defaultextension = ".fpgp")
    print(filename)

def loadProfClick():
    filename = tk.filedialog.askopenfilename(filetypes= (('FPG Profile', '*.fpgp'),))
    print(filename)

def locateFFmpegClick():
    global ffmpegPath
    path = tk.filedialog.askopenfilename()
    if path.endswith("ffmpeg.exe"): #find a way to make this work on non-windows systems. probably use if(os=win) do "ffmpeg.exe", then if(os=mac) change to .app, etc.
        ffmpegPath = path
    else:
        tk.messagebox.showerror("Oh no!", message="Locating ffmpeg failed.\nMake sure you've got the right executable and try again.")
    print("ffmpeg path set to " + ffmpegPath)

#fileMenu.add_command(label="Save Profile As...", command = saveProfClick)
#fileMenu.add_command(label="Open Profile", command = loadProfClick)
fileMenu.add_separator()
fileMenu.add_command(label="Locate FFmpeg...", command = locateFFmpegClick)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command = window.destroy)

#help bar
helpMenu = tk.Menu(menubar)
menubar.add_cascade(label="Help", menu=helpMenu)

def aboutPage():
    tk.messagebox.showinfo(title="About", message="ffmpeg photosensitivity GUI\n0.1.1 pre-release version")

def helpPage():
    webbrowser.open('help.html')

helpMenu.add_command(label="GUI Usage", command=helpPage)
helpMenu.add_command(label="About", command=aboutPage)

#
# run filter
#
def exportClick():
    gatherInfo()
    infoMsg = informOfCommand()
    tk.messagebox.showinfo(title="Run Filter", message=(infoMsg[1]))
    if infoMsg[0]:
        makeCommand()
        tk.messagebox.showinfo(title="Run Filter", message=("Should be done! Check log for details."))

exportButton = tk.Button(window, text = "Run Filter", command = exportClick)
exportButton.grid(column=3, row=7)

#loop it!
window.mainloop()
