#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_7segment matrix = Adafruit_7segment();
int player1Life = 120;
int player2Life = 120;
boolean player1Win = false;
boolean player2Win = false;

const int b1Pin = 2; 
const int b2Pin = 3;
const int b3Pin = 4;
const int b4Pin = 5; 
const int b5Pin = 6; 

int lastState1 = HIGH;
int lastState2 = HIGH;
int lastState3 = HIGH;
int lastState4 = HIGH;
int lastState5 = HIGH;
int currentState1; 
int currentState2;
int currentState3;
int currentState4;
int currentState5;

int counter1 = 0;
int counter2 = 0;
int counter3 = 0;
int counter4 = 0;

boolean incriment1 = true;
boolean incriment2 = true;
boolean incriment3 = true;
boolean incriment4 = true;

boolean sendPlayer1GameWinSignal = true;
boolean sendPlayer2GameWinSignal = true;

String bothLifes = "1111";
boolean countUp;
int lastLife1 = 120;
int lastLife2 = 120;
#define player1LED 12
#define player2LED 11

void setup() {
#ifndef __AVR_ATtiny85__
  Serial.begin(9600);
  //Serial.println("7 Segment Backpack Test");
#endif
  matrix.begin(0x70);
 // initialize the pushbutton pin as an input:
  pinMode(b1Pin, INPUT_PULLUP);
  pinMode(b2Pin, INPUT_PULLUP);
  pinMode(b3Pin, INPUT_PULLUP);
  pinMode(b4Pin, INPUT_PULLUP);
  pinMode(b5Pin, INPUT_PULLUP);
  pinMode(player1LED, OUTPUT);
  pinMode(player2LED, OUTPUT);
}

void loop() {
  //currentState1 = pinMode(player1LED, OUTPUT);
  currentState1 = digitalRead(b1Pin);
  currentState2 = digitalRead(b2Pin);
  currentState3 = digitalRead(b3Pin);
  currentState4 = digitalRead(b4Pin);
  currentState5 = digitalRead(b5Pin);
    
    if(lastState1 == LOW && currentState1 == LOW){
      counter1++;
     if (counter1 == 250){
      player1Life = player1Life + 5;
      incriment1 = false; 
      counter1 = 0;
     }
     } else if (lastState1 == LOW && currentState1 == HIGH && incriment1 == false){
      counter1 = 0;
     } else if (lastState1 == LOW && currentState1 == HIGH && incriment1 == true){
      player1Life++;
      counter1 = 0;
    }

    if(lastState2 == LOW && currentState2 == LOW){
      counter2++;
     if (counter2 == 250){
      player2Life = player2Life - 5;
      incriment2 = false;
      counter2 = 0;
     }
     } else if (lastState2 == LOW && currentState2 == HIGH  && incriment2 == false){
      counter2 = 0;
     } else if (lastState2 == LOW && currentState2 == HIGH && incriment2 == true){
      player2Life--;
      counter2 = 0;
    }
    
  if(lastState3 == LOW && currentState3 == LOW){
        counter3++;
       if (counter3 == 250){
        player1Life = player1Life - 5;
        incriment3 = false;
        counter3 = 0;
       }
       } else if (lastState3 == LOW && currentState3 == HIGH && incriment3 == false){
        counter3 = 0; 
       } else if (lastState3 == LOW && currentState3 == HIGH && incriment3 == true){
        player1Life--;
        counter3 = 0;
      }
    
    if(lastState4 == LOW && currentState4 == LOW){
      counter4++; 
     if (counter4 == 250){
      player2Life = player2Life + 5;
      incriment4 = false;
      counter4 = 0;
     }
     } else if (lastState4 == LOW && currentState4 == HIGH && incriment4 == false){
      counter4 = 0;
     } else if (lastState4 == LOW && currentState4 == HIGH && incriment4 == true){
      player2Life++;
      counter4 = 0;
    }

  if(lastState1 == HIGH && currentState1 == HIGH){
    incriment1 = true;
  }
  if(lastState2 == HIGH && currentState2 == HIGH){
    incriment2 = true;
  }   
  if(lastState3 == HIGH && currentState3 == HIGH){
     incriment3 = true;
  }
  if(lastState4 == HIGH && currentState4 == HIGH){
     incriment4 = true;
  }
    
    if(lastState5 == HIGH && currentState5 == LOW){   //Reset button
     player1Life = 120;
     player2Life = 120;
     player1Win = false;
     player2Win = false;
    sendPlayer1GameWinSignal = true;
    sendPlayer2GameWinSignal = true;
    }
    
    
    if(player2Life <= 100){           //Check for a player at 0
     player1Win = true;
     countUp = true;
    }
    if(player1Life <= 100){
     player2Win = true;
     countUp = true;
    }
    
    if (countUp == true){             //Auto reset the life totals
     if (player1Life < 120){
       player1Life++;
       player1Life = 120;
  }else if(player1Life > 120){
     player1Life--;
     player1Life = 120;
  }
     if (player2Life < 120){
        player2Life++;
        player2Life = 120;
  }else if(player2Life > 120){
     player2Life--;
     player2Life = 120;
  }
     if (player1Life == 120 && player2Life == 120){
        countUp = false;
  }
  delay(125);
    }
    
    if(player1Win == true){             //Game win indicators
      digitalWrite(player1LED, HIGH);
      if (sendPlayer1GameWinSignal){
        Serial.println("301");
        sendPlayer1GameWinSignal = false;
      }
    }else{
      digitalWrite(player1LED, LOW);
    }
    if(player2Win == true){
      digitalWrite(player2LED, HIGH);
      if (sendPlayer2GameWinSignal){
        Serial.println("302");
        sendPlayer2GameWinSignal = false;
      }
    }else{
      digitalWrite(player2LED, LOW);
    }
    
    printOut(); //Print to display
 
  matrix.writeDisplay();
  lastState1 = currentState1;
  lastState2 = currentState2;
  lastState3 = currentState3;
  lastState4 = currentState4;

if ((lastLife1 != player1Life) || (lastLife2 != player2Life)){    //print changes to serial
  if (lastLife1 != player1Life){
    Serial.println(player1Life);
    //Serial.print("/n");
    lastLife1 = player1Life;
  }
  delay(30);
  if (lastLife2 != player2Life){
    Serial.println(player2Life + 100);
   // Serial.print("\n");
    lastLife2 = player2Life;
  }
}

}
 void printOut(){
    String POL = String(player1Life);
    String PTL = String(player2Life);
    String char1 = "2";
    char1.setCharAt(0, POL.charAt(1));
    String char2 = "2";
    char2.setCharAt(0, POL.charAt(2));
    String char3 = "2";
    char3.setCharAt(0, PTL.charAt(1));
    String char4 = "2"; 
    char4.setCharAt(0, PTL.charAt(2));
    matrix.writeDigitNum(0, char1.toInt());
    matrix.writeDigitNum(1, char2.toInt());
    matrix.writeDigitNum(3, char3.toInt());
    matrix.writeDigitNum(4, char4.toInt());
 }
