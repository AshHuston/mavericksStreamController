import tkinter as tk
#from tkinter import * 
#from tkinter.ttk import *
import os
import time
import threading

global enteredP1Life
global enteredP2Life
global enteredP1Name
global enteredP2Name
global enteredP1Deck
global enteredP2Deck
global enteredP1GameWins
global enteredP2GameWins
global enteredCardName

enteredP1Life = ""
enteredP2Life = ""
enteredP1Name = ""
enteredP2Name = ""
enteredP1Deck = ""
enteredP2Deck = ""
enteredP1GameWins = ""
enteredP2GameWins = ""
enteredCardName = ""

pushedP1Life = ""
pushedP2Life = ""
pushedP1Name = ""
pushedP2Name = ""
pushedP1Deck = ""
pushedP2Deck = ""
pushedP1GameWins = ""
pushedP2GameWins = ""
pushedCardName = ""

def keepWindowOpen():

    global enteredP1Life
    global enteredP2Life
    global enteredP1Name
    global enteredP2Name
    global enteredP1Deck
    global enteredP2Deck
    global enteredP1GameWins
    global enteredP2GameWins
    global enteredCardName

    master = tk.Tk()
    master.geometry("600x350")

    guiP1Life = tk.StringVar()
    guiP2Life = tk.StringVar()
    guiP1Name = tk.StringVar()
    guiP2Name = tk.StringVar()
    guiP1Deck = tk.StringVar()
    guiP2Deck = tk.StringVar()
    guiP1GameWins = tk.StringVar()
    guiP2GameWins = tk.StringVar()
    guiCardName = tk.StringVar()


    p1Label = tk.Label(master, text="Player 1:")
    p1LifeLabel = tk.Label(master, text="Life Total")
    p1NameLabel = tk.Label(master, text="Name")
    p1DeckLabel = tk.Label(master, text="Deck")

    p1LifeEntry = tk.Entry(master, textvariable=guiP1Life)
    p1NameEntry = tk.Entry(master, textvariable=guiP1Name)
    p1DeckEntry = tk.Entry(master, textvariable=guiP1Deck)
    p1GameWins = tk.Entry(master, textvariable=guiP1GameWins)

    gameWinsLabel2 = tk.Label(master, text=" - ")
    gameWinsLabel1 = tk.Label(master, text="Game Wins")
    displayCardNameLabel = tk.Label(master, text="Enter card name:")
    cardNameEntry = tk.Entry(master, textvariable=guiCardName)

    p2Label = tk.Label(master, text="Player 2:")
    p2LifeLabel = tk.Label(master, text="Life Total")
    p2NameLabel = tk.Label(master, text="Name")
    p2DeckLabel = tk.Label(master, text="Deck")

    p2LifeEntry = tk.Entry(master, textvariable=guiP2Life)
    p2NameEntry = tk.Entry(master, textvariable=guiP2Name)
    p2DeckEntry = tk.Entry(master, textvariable=guiP2Deck)
    p2GameWins = tk.Entry(master, textvariable=guiP2GameWins)

    # Place on grid
    p1Label.grid(row=0, column=0)
    p1LifeLabel.grid(row=1, column=1)
    p1LifeEntry.grid(row=2, column=1)
    p1NameLabel.grid(row=1, column=0)
    p1NameEntry.grid(row=2, column=0)
    p1DeckLabel.grid(row=3, column=0)
    p1DeckEntry.grid(row=4, column=0)
    p1GameWins.grid(row=5, column=1)

    p2Label.grid(row=0, column=5)
    p2LifeLabel.grid(row=1, column=4)
    p2LifeEntry.grid(row=2, column=4)
    p2NameLabel.grid(row=1, column=5)
    p2NameEntry.grid(row=2, column=5)
    p2DeckLabel.grid(row=3, column=5)
    p2DeckEntry.grid(row=4, column=5)
    p2GameWins.grid(row=5, column=4)

    gameWinsLabel1.grid(row=4, column=3)
    gameWinsLabel2.grid(row=5, column=3)
    displayCardNameLabel.grid(row=8, column=0)
    cardNameEntry.grid(row=9, column=0)
    
    def enterValues():
        global enteredP1Life
        global enteredP2Life
        global enteredP1Name
        global enteredP2Name
        global enteredP1Deck
        global enteredP2Deck
        global enteredP1GameWins
        global enteredP2GameWins
        global enteredCardName
        enteredP1Life = guiP1Life.get()
        enteredP2Life = guiP2Life.get()
        enteredP1Name = guiP1Name.get()
        enteredP2Name = guiP2Name.get()
        enteredP1Deck = guiP1Deck.get()
        enteredP2Deck = guiP2Deck.get()
        enteredP1GameWins = guiP1GameWins.get()
        enteredP2GameWins = guiP2GameWins.get()
        enteredCardName = guiCardName.get()
    enterValues()
    master.mainloop()

def checkForValueUpdates():
        #guiP1Life, guiP2Life, guiP1Name, guiP2Name, guiP1Deck, guiP2Deck, guiP1GameWins, guiP2GameWins, guiCardName):
    global enteredP1Life
    global enteredP2Life
    global enteredP1Name
    global enteredP2Name
    global enteredP1Deck
    global enteredP2Deck
    global enteredP1GameWins
    global enteredP2GameWins
    global enteredCardName

    print(enteredP1Life)
    print(pushedP1Life)
    if enteredP1Life != pushedP1Life:
        #print('p1 life changed!')
        print(enteredP1Life)
        
    if enteredP2Life != pushedP2Life:
        pass
        
    if enteredP1Name != pushedP1Name:
        pass
        
    if enteredP2Name != pushedP2Name:
        pass

    if enteredP1Deck != pushedP1Deck:
        pass

    if enteredP2Deck != pushedP2Deck:
        pass
        
    if enteredP1GameWins != pushedP1GameWins:
        pass

    if enteredP2GameWins != pushedP2GameWins:
        pass

    if enteredCardName != pushedCardName:
        pass
    
windowThred = threading.Thread(group = None, target = keepWindowOpen)
windowThred.start()
delaySeconds = 0.5
while True:
    threadCount = threading.active_count()
    checkForValueUpdates()
    time.sleep(delaySeconds)

#updateThread = threading.Thread(group = None, target = checkForValueUpdates)


#threadCount = threading.active_count()
#updateThread = threading.Thread(group = None, target = checkForValueUpdates, args=[guiP1Life.get(), guiP2Life.get(), guiP1Name.get(), guiP2Name.get(), guiP1Deck.get(), guiP2Deck.get(), guiP1GameWins.get(), guiP2GameWins.get(), guiCardName.get()])
#if threadCount < 1 :
#    updateThread.start()

 
 
while True:
    print(guiP1Life.get())

# open, read, and close the files
    # Above variables 
    # Combined gamewins string

# Write values to the gui ('saving' from previous launch)

#while (True):
    # read the gui 

    # if gui and files are missmatched:
        # Open appropriate file(s), write new gui values to files, reassign  file variables, then close file(s).
    

   # pass


