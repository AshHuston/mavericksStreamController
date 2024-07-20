import tkinter as tk
import time
import threading
import json
import requests
from sys import exit
from PIL import Image
from PIL import ImageTk
from io import BytesIO
import serial
from serial import tools
from serial.tools import list_ports
import os

global lifeControllerIsOn
lifeControllerIsOn = False

global guiCardImageName
guiCardImageName = ""

global controllerIsConnected
controllerIsConnected = False

global connectedControllerPort

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

pushedP1Life = "20"
pushedP2Life = "20"
pushedP1Name = "Player 1 Name"
pushedP2Name = "Player 2 Name"
pushedP1Deck = "Player 1 Deck"
pushedP2Deck = "Player 2 Deck"
pushedP1GameWins = "0"
pushedP2GameWins = "0"
pushedCardName = "Chillarpillar"
enteredCardName = "Chub Toad"

def getCardImage(cardName):
    if cardName != "":
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + cardName.strip().replace(" ", "+")
        request = requests.get(url=url)
        sucess = 200
        if request.status_code == sucess:
            try:
                cardJson = json.loads(request.content)
                imageUrl = cardJson["image_uris"]["large"]
                imageRequest = requests.get(imageUrl)
                image = imageRequest.content
                return image
            except:
                print("Scryfall search failed. Status code: " + str(request.status_code))
                return False
        else:
            print("Failed to connect. Status code: " + str(request.status_code))
            return False

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
    global lifeControllerIsOn
    global pushedP1Life
    global pushedP2Life
    global pushedP1Name
    global pushedP2Name
    global pushedP1Deck
    global pushedP2Deck
    global pushedP1GameWins
    global pushedP2GameWins
    global pushedCardName
    global controllerIsConnected

    master = tk.Tk()
    master.geometry("725x360")
    master.configure(bg="#2A2A2A")
    master.title("Stream Overlay Controller")

    try:
        photo = tk.PhotoImage(file='Mlogo.png')
        master.wm_iconphoto(False, photo)
    except:
        pass

    guiP1Life = tk.StringVar()
    guiP2Life = tk.StringVar()
    guiP1Name = tk.StringVar()
    guiP2Name = tk.StringVar()
    guiP1Deck = tk.StringVar()
    guiP2Deck = tk.StringVar()
    guiP1GameWins = tk.StringVar()
    guiP2GameWins = tk.StringVar()
    guiCardName = tk.StringVar()
    guiControllerToggle = tk.BooleanVar()

    guiP1Life.set(pushedP1Life)
    guiP2Life.set(pushedP2Life)
    guiP1Name.set(pushedP1Name)
    guiP2Name.set(pushedP2Name)
    guiP1Deck.set(pushedP1Deck)
    guiP2Deck.set(pushedP2Deck)
    guiP1GameWins.set(pushedP1GameWins)
    guiP2GameWins.set(pushedP2GameWins)
    guiCardName.set(pushedCardName)

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
        global lifeControllerIsOn

        if lifeControllerIsOn == False:
            enteredP1Life = guiP1Life.get()
            enteredP2Life = guiP2Life.get()
            enteredP1GameWins = guiP1GameWins.get()
            enteredP2GameWins = guiP2GameWins.get()

        enteredP1Name = guiP1Name.get()
        enteredP2Name = guiP2Name.get()
        enteredP1Deck = guiP1Deck.get()
        enteredP2Deck = guiP2Deck.get()
        enteredCardName = guiCardName.get()


    def updateControllerState(var, index, mode):
        global lifeControllerIsOn
        lifeControllerIsOn = guiControllerToggle.get()

    def updateGuiCardDisplay():
        global guiCardImageName
        if (pushedCardName != guiCardImageName):
            height = 350
            width = 250
            guiCardImage = getCardImage(pushedCardName)
            try:
                cardImage = Image.open(BytesIO(guiCardImage))
                cardImage = cardImage.resize((width, height))
                cardPhotoImage = ImageTk.PhotoImage(cardImage)
                displayCard = tk.Label(master, image=cardPhotoImage)
                displayCard.photo = cardPhotoImage
                displayCard.place(in_=master, relx=0.995, rely=0.005, x=-(width+2), y=2)
            except:
                pass
            guiCardImageName = pushedCardName
        master.after(guiDisplayUpdateDelayMiliseconds, updateGuiCardDisplay)

    guiDisplayUpdateDelayMiliseconds = 500
    master.after(guiDisplayUpdateDelayMiliseconds, updateGuiCardDisplay)

    guiP1Life.trace_add('write', enterValues)
    guiP2Life.trace_add('write', enterValues)
    guiP1Name.trace_add('write', enterValues)
    guiP2Name.trace_add('write', enterValues)
    guiP1Deck.trace_add('write', enterValues)
    guiP2Deck.trace_add('write', enterValues)
    guiP1GameWins.trace_add('write', enterValues)
    guiP2GameWins.trace_add('write', enterValues)
    guiCardName.trace_add('write', enterValues)
    guiControllerToggle.trace_add('write', updateControllerState)

    p1Label = tk.Label(master, text="          Player 1:          ", bg="#AE3FB9")
    p1LifeLabel = tk.Label(master, text="Life Total", bg="#AE3FB9")
    p1NameLabel = tk.Label(master, text="Name", bg="#AE3FB9")
    p1DeckLabel = tk.Label(master, text="Deck", bg="#AE3FB9")

    p1LifeEntry = tk.Entry(master, textvariable=guiP1Life, justify='center', width=5, bg="#E968F5", )
    p1NameEntry = tk.Entry(master, textvariable=guiP1Name, justify='center', bg="#E968F5")
    p1DeckEntry = tk.Entry(master, textvariable=guiP1Deck, justify='center', bg="#E968F5")
    p1GameWins = tk.Entry(master, textvariable=guiP1GameWins, justify='center', width=5, bg="#E968F5")

    gameWinsLabel2 = tk.Label(master, text="          -          ", bg="#757575")
    gameWinsLabel1 = tk.Label(master, text="Game Wins", bg="#656565")
    displayCardNameLabel = tk.Label(master, text="Enter card name:", bg="#C1C27C")
    cardNameEntry = tk.Entry(master, textvariable=guiCardName, justify='center', bg="#E4E594")
    physicalControllerToggleLabel = tk.Label(master, text="Physical Controller?", bg="#695EB5")
    physicalControllerToggle = tk.Checkbutton(master, variable=guiControllerToggle, justify='center', bg="#695EB5")
    global physicalControllerIsConnectedLabel
    physicalControllerIsConnectedLabel = tk.Label(master)
    
    p2Label = tk.Label(master, text="          Player 2:          ", bg="#46B6B8")
    p2LifeLabel = tk.Label(master, text="Life Total", bg="#46B6B8")
    p2NameLabel = tk.Label(master, text="Name", bg="#46B6B8")
    p2DeckLabel = tk.Label(master, text="Deck", bg="#46B6B8")

    p2LifeEntry = tk.Entry(master, textvariable=guiP2Life, justify='center', width=5, bg="#5CDFE1")
    p2NameEntry = tk.Entry(master, textvariable=guiP2Name, justify='center', bg="#5CDFE1")
    p2DeckEntry = tk.Entry(master, textvariable=guiP2Deck, justify='center', bg="#5CDFE1")
    p2GameWins = tk.Entry(master, textvariable=guiP2GameWins, justify='center', width=5, bg="#5CDFE1")

    def updateControllerIsConnectedDisplay():
        global controllerIsConnected
        global physicalControllerIsConnectedLabel
        if controllerIsConnected:
            physicalControllerIsConnectedLabel.config(text="Connected", bg="#04D700")
        else:
            physicalControllerIsConnectedLabel.config(text="NOT connected", bg="#D74500")

        master.after(guiControllerConnectedDelayMiliseconds, updateControllerIsConnectedDisplay)

    guiControllerConnectedDelayMiliseconds = 10
    master.after(guiControllerConnectedDelayMiliseconds, updateControllerIsConnectedDisplay)

    def checkForToggleDisables():
        while(windowThread.is_alive() == True):
            time.sleep(0.15)
            global pushedP1Life
            global pushedP2Life
            global enteredP1Life
            global enteredP2Life
            global pushedP1GameWins
            global pushedP2GameWins
            if lifeControllerIsOn:
                guiP1Life.set(enteredP1Life)
                guiP2Life.set(enteredP2Life)
                guiP1GameWins.set(pushedP1GameWins)
                guiP2GameWins.set(pushedP2GameWins)     
                p1LifeEntry.configure(state='disabled', disabledbackground="#E1B4E5")
                p2LifeEntry.configure(state='disabled', disabledbackground="#A8CBCB")
                p1GameWins.configure(state='disabled', disabledbackground="#E1B4E5")
                p2GameWins.configure(state='disabled', disabledbackground="#A8CBCB")
            else:
                p1LifeEntry.configure(state='normal')
                p2LifeEntry.configure(state='normal')
                p1GameWins.configure(state='normal')
                p2GameWins.configure(state='normal')

    toggleCheckThread = threading.Thread(group = None, target = checkForToggleDisables)
    toggleCheckThread.daemon = True
    toggleCheckThread.start()

    # Place on grid
    p1Label.grid(row=0, column=0)
    p1LifeLabel.grid(row=1, column=1)
    p1LifeEntry.grid(row=2, column=1)
    p1NameLabel.grid(row=1, column=0)
    p1NameEntry.grid(row=2, column=0)
    p1DeckLabel.grid(row=3, column=0)
    p1DeckEntry.grid(row=4, column=0)
    p1GameWins.grid(row=5, column=1, sticky="e")

    p2Label.grid(row=0, column=5)
    p2LifeLabel.grid(row=1, column=4)
    p2LifeEntry.grid(row=2, column=4)
    p2NameLabel.grid(row=1, column=5)
    p2NameEntry.grid(row=2, column=5)
    p2DeckLabel.grid(row=3, column=5)
    p2DeckEntry.grid(row=4, column=5)
    p2GameWins.grid(row=5, column=4, sticky="w")

    physicalControllerIsConnectedLabel.grid(row=1, column=3)
    gameWinsLabel1.grid(row=4, column=3)
    gameWinsLabel2.grid(row=5, column=3)
    displayCardNameLabel.grid(row=8, column=5)
    cardNameEntry.grid(row=9, column=5)
    physicalControllerToggleLabel.grid(row=2, column=3)
    physicalControllerToggle.grid(row=3, column=3)    

    master.mainloop()

def saveCardImage(cardName):
    if cardName != "":
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + cardName.strip().replace(" ", "+")
        request = requests.get(url=url)
        sucess = 200
        if request.status_code == sucess:
            try:
                cardJson = json.loads(request.content)
                imageUrl = cardJson["image_uris"]["large"]
                imageRequest = requests.get(imageUrl)
                image = imageRequest.content
                file = open("controller output files\\displayCardImage.png", 'wb')
                file.write(image)
                file.close()
            except:
                print("Scryfall search failed. Status code: " + str(request.status_code))
        else:
            print("Failed to connect. Status code: " + str(request.status_code))

def isRealCardName(cardName):
    if cardName != "":
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + cardName.strip().replace(" ", "+")
        request = requests.get(url=url)
        sucess = 200
        if request.status_code == sucess:
            return True
        else:
            return False

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
        if isRealCardName(enteredCardName):
            pushedCardName = enteredCardName
            saveCardImage(pushedCardName)
            print(f'Pushed: {pushedCardName}')
            file = open('controller output files\\display Card Name.txt', 'w')
            file.write(pushedCardName)
            file.close()

def setPreviousValues():
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
   
    try:
        file = open('controller output files\\player 1 life.txt', 'r')
        enteredP1Life = file.read()
        pushedP1Life = enteredP1Life
        file.close()
    except:
        enteredP1Life = ""  

    try:     
        file = open('controller output files\\player 2 life.txt', 'r')
        enteredP2Life = file.read()
        pushedP2Life = enteredP2Life
        file.close()
    except:
        enteredP2Life = ""  
        
    try:
        file = open('controller output files\\player 1 name.txt', 'r')
        enteredP1Name = file.read()
        pushedP1Name = enteredP1Name
        file.close()
    except:
        enteredP1Name = ""  
        
    try:
        file = open('controller output files\\player 2 name.txt', 'r')
        enteredP2Name = file.read()
        pushedP2Name = enteredP2Name 
        file.close()
    except:
        enteredP2Name = ""  
        
    try:
        file = open('controller output files\\player 1 deck.txt', 'r')
        enteredP1Deck = file.read()
        pushedP1Deck = enteredP1Deck
        file.close()
    except:
        enteredP1Deck = ""  
        
    try:
        file = open('controller output files\\player 2 deck.txt', 'r')
        enteredP2Deck = file.read()
        pushedP2Deck = enteredP2Deck
        file.close()
    except:
        enteredP2Deck = ""  
        
    try:
        file = open('controller output files\\player 1 game wins.txt', 'r')
        enteredP1GameWins = file.read()
        pushedP1GameWins = enteredP1GameWins
        file.close()
    except:
        enteredP1GameWins = ""  
        
    try:
        file = open('controller output files\\player 2 game wins.txt', 'r')
        enteredP2GameWins = file.read()
        pushedP2GameWins = enteredP2GameWins
        file.close()
    except:
        enteredP2GameWins = ""

    try:
        file = open('controller output files\\display Card Name.txt', 'r')
        enteredCardName = file.read()
        pushedCardName = enteredCardName
        file.close()
    except:
        enteredCardName = ""  

def updateLifeTotalsAndGameWins(serialData):
    global enteredP1Life
    global enteredP2Life
    global enteredP1GameWins
    global enteredP2GameWins
    player1WinSignal = 301
    player2WinSignal = 302
    player1NoWinSignal = 311
    player2NoWinSignal = 312
    try:
        if 100 <= serialData <= 200:
            enteredP1Life =  str(serialData-100)
        if 200 < serialData <= 300:
            enteredP2Life =  str(serialData-200)
        if serialData == player1WinSignal:
            enteredP1GameWins = str(int(enteredP1GameWins) + 1)
        if serialData == player2WinSignal:
            enteredP2GameWins = str(int(enteredP2GameWins) + 1)
        if serialData == player1NoWinSignal:
            enteredP1GameWins = "0"
        if serialData == player2NoWinSignal:
            enteredP2GameWins = "0" 
    except:
        pass

def runSerialReader():
    global lifeControllerIsOn
    global controllerIsConnected
    global connectedControllerPort
    controllerUpdateSeconds = 0.15
    while lifeControllerIsOn:
        time.sleep(controllerUpdateSeconds)
        try:
            if controllerIsConnected:
                if connectedControllerPort.readable():
                    serialData = connectedControllerPort.readline().decode()
                    if serialData != "":
                        serialData = int(serialData)
                    else:
                        serialData = 0
                else:
                    #serialData = "ERROR"
                    serialData = 0
                if serialData != 0:
                    print(serialData)
                    updateLifeTotalsAndGameWins(serialData)
        except:
            #ser.close()
            print("err")
            pass

def checkIfcontrollerIsConnected():
    global controllerIsConnected
    global connectedControllerPort
    ports = list_ports.comports(include_links=True)
    #controllerIsConnected = False
    connectionFound = False
    for any in ports:
        if any.manufacturer.count("wch.cn") >= 1:
            controllerIsConnected = True
            connectionFound = True
            if connectedControllerPort.is_open == False:
                connectedControllerPort.timeout = 0.005
                connectedControllerPort.baudrate = 9600
                connectedControllerPort.port = any.device
                try:
                    connectedControllerPort.open()
                except:
                    pass
    if connectionFound == False:
        controllerIsConnected = False

connectedControllerPort = serial.Serial() # Blank start port so when we check it later we don't crash

path = 'controller output files'
folderExists = os.path.exists(path)
if folderExists == False:
    os.makedirs(path)

setPreviousValues()
saveCardImage("Chillarpillar")    
windowThread = threading.Thread(group = None, target = keepWindowOpen)
windowThread.start()
controllerThread = threading.Thread(group = None, target = runSerialReader)
time.sleep(0.1)
delaySeconds = 0.05

#while threading.active_count() >= 2:
while windowThread.is_alive():
    checkIfcontrollerIsConnected()
    checkForValueUpdates()
    if lifeControllerIsOn:
        if controllerThread.is_alive() == False:
            print("---------------------Start serial reader")
            controllerThread.start()
    else:
        controllerThread = threading.Thread(group = None, target = runSerialReader)
    time.sleep(delaySeconds)

try:
    connectedControllerPort.close()
except:
    pass

raise SystemExit()
