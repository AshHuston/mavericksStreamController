import tkinter as tk
import time
import threading
import json
#from pillow import image
import requests

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

global pushedP1Life
global pushedP2Life
global pushedP1Name
global pushedP2Name
global pushedP1Deck
global pushedP2Deck
global pushedP1GameWins
global pushedP2GameWins
global pushedCardName

pushedP1Life = "20"
pushedP2Life = "20"
pushedP1Name = "Player 1"
pushedP2Name = "Player 2"
pushedP1Deck = "P1 Deck"
pushedP2Deck = "P2 Deck"
pushedP1GameWins = "0"
pushedP2GameWins = "0"
pushedCardName = "Chillarpillar"

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

    def enterValues(var, index, mode):
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

    guiP1Life.trace_add('write', enterValues)
    guiP2Life.trace_add('write', enterValues)
    guiP1Name.trace_add('write', enterValues)
    guiP2Name.trace_add('write', enterValues)
    guiP1Deck.trace_add('write', enterValues)
    guiP2Deck.trace_add('write', enterValues)
    guiP1GameWins.trace_add('write', enterValues)
    guiP2GameWins.trace_add('write', enterValues)
    guiCardName.trace_add('write', enterValues)

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
    
    master.mainloop()

def saveCardImage(cardName):
    if cardName != "":
        #get cardname scyfall uri
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + cardName.replace(" ", "+")
        request = requests.get(url=url)
        sucess = 200
        if request.status_code == sucess:
            cardJson = json.loads(request.content)
            imageUrl = cardJson["image_uris"]["large"]
            imageRequest = requests.get(imageUrl)
            image = imageRequest.content
            file = open("controller output files\\displayCardImage.jpg", 'wb')
            file.write(image)
            file.close()
           
        else:
            print("Failed to connect. Status code: " + str(request.status_code))

        #get list of printings
        #find printing that is not full art, is not a variation, non promoprioritizing standard legal printings
        #If it cant, itll find the default printing.


def checkForValueUpdates():
    global enteredP1Life
    global enteredP2Life
    global enteredP1Name
    global enteredP2Name
    global enteredP1Deck
    global enteredP2Deck
    global enteredP1GameWins
    global enteredP2GameWins
    global enteredCardName
    global pushedP1Life
    global pushedP2Life
    global pushedP1Name
    global pushedP2Name
    global pushedP1Deck
    global pushedP2Deck
    global pushedP1GameWins
    global pushedP2GameWins
    global pushedCardName

    def updateCombinedGameWins():
        p1wins = pushedP1GameWins
        p2wins = pushedP2GameWins
        if p1wins == "":
            p1wins = "0"
        if p2wins == "":
            p2wins = "0"
        combinedGamewins = p1wins + " - " + p2wins
        file = open('controller output files\\Combined GameWins.txt', 'w')
        file.write(combinedGamewins)
        file.close()
        combinedGamewins = p2wins + " - " + p1wins
        file = open('controller output files\\Combined GameWins Reveresed.txt', 'w')
        file.write(combinedGamewins)
        file.close()

    if enteredP1Life != pushedP1Life:
        pushedP1Life = enteredP1Life
        print(pushedP1Life)
        file = open('controller output files\\player 1 life.txt', 'w')
        file.write(pushedP1Life)
        file.close()
        
    if enteredP2Life != pushedP2Life:
        pushedP2Life = enteredP2Life
        print(pushedP2Life)
        file = open('controller output files\\player 2 life.txt', 'w')
        file.write(pushedP2Life)
        file.close()
             
    if enteredP1Name != pushedP1Name:
        pushedP1Name =enteredP1Name
        print(pushedP1Name)
        file = open('controller output files\\player 1 name.txt', 'w')
        file.write(pushedP1Name)
        file.close()
             
    if enteredP2Name != pushedP2Name:
        pushedP2Name = enteredP2Name 
        print(pushedP2Name)
        file = open('controller output files\\player 2 name.txt', 'w')
        file.write(pushedP2Name)
        file.close()
             
    if enteredP1Deck != pushedP1Deck:
        pushedP1Deck = enteredP1Deck
        print(pushedP1Deck)
        file = open('controller output files\\player 1 deck.txt', 'w')
        file.write(pushedP1Deck)
        file.close()

    if enteredP2Deck != pushedP2Deck:
        pushedP2Deck = enteredP2Deck
        print(pushedP2Deck)
        file = open('controller output files\\player 2 deck.txt', 'w')
        file.write(pushedP2Deck)
        file.close()
        
    if enteredP1GameWins != pushedP1GameWins:
        pushedP1GameWins = enteredP1GameWins
        print(pushedP1GameWins)
        file = open('controller output files\\player 1 game wins.txt', 'w')
        file.write(pushedP1GameWins)
        file.close()
        updateCombinedGameWins()

    if enteredP2GameWins != pushedP2GameWins:
        pushedP2GameWins = enteredP2GameWins
        print(pushedP2GameWins)
        file = open('controller output files\\player 2 game wins.txt', 'w')
        file.write(pushedP2GameWins)
        file.close()
        updateCombinedGameWins()

    if enteredCardName != pushedCardName:
        pushedCardName = enteredCardName
        print(pushedCardName)
        file = open('controller output files\\display Card Name.txt', 'w')
        file.write(pushedCardName)
        file.close()
        saveCardImage(pushedCardName)
    
windowThred = threading.Thread(group = None, target = keepWindowOpen)
windowThred.start()
delaySeconds = 0.5
while True:
    threadCount = threading.active_count()
    checkForValueUpdates()
    time.sleep(delaySeconds)
    if threadCount <= 1:
        exit(1)