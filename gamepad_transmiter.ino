#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "12345";

int tg1=5;
int tg2=6;
int p1=A6;
int p2=A5;
int s1=10;
int s2=9;
int s3=3;
int s4=2;
int j1x=A3;
int j1y=A4;
int j2x=A2;
int j2y=A1;
int j2s=A0;



struct package {
int vp1;
int vp2;
int vj1x;
int vj1y;
int vj2x;
int vj2y;
int vtg1;
int vtg2;
int vj2s;
int vs1;
int vs2;
int vs3;
int vs4;
};


package data; 

void setup() {
radio.begin();
radio.openWritingPipe(address);

radio.setPALevel(RF24_PA_MIN);
radio.stopListening();

pinMode(tg1,INPUT);
pinMode(tg2,INPUT);
pinMode(p1,INPUT);
pinMode(p2,INPUT);
pinMode(s1,INPUT);
pinMode(s2,INPUT);
pinMode(s3,INPUT);
pinMode(s4,INPUT);
pinMode(j1x,INPUT);
pinMode(j1y,INPUT);
pinMode(j2y,INPUT);
pinMode(j2s,INPUT);

data.vj2s = 1;
data.vtg1 = 1;
data.vtg2 = 1;
data.vs1 = 1;
data.vs2 = 1;
data.vs3 = 1;
data.vs4 = 1;
}

void loop() {
 // Read all analog inputs and map them to one Byte value
 data.vj1x = analogRead(j1x); // Convert the analog read value from 0 to 1023 into a BYTE
 data.vj1y = analogRead(j1y);
 data.vj2x = analogRead(j2x);
 data.vj2y = analogRead(j2y);
 data.vp1 = analogRead(p1);
 data.vp2 = analogRead(p2);
 // Read all digital inputs
 data.vj2s = digitalRead(j2s);
 data.vtg1 = digitalRead(tg1);
 data.vtg2 = digitalRead(tg2);
 data.vs1 = digitalRead(s1);
 data.vs2 = digitalRead(s2);
 data.vs3 = digitalRead(s3);
 data.vs4 = digitalRead(s4);
 radio.write(&data, sizeof(package));

 
 
 }

//For debugging


//  void printdata(){

// Serial.print("Tg1=");
// Serial.print(data.vtg1);
// Serial.print("\t");

// Serial.print("Tg2=");
// Serial.print(data.vtg2);
// Serial.print("\t");


// Serial.print("S1=");
// Serial.print(data.vs1);
// Serial.print("\t");


// Serial.print("S2=");
// Serial.print(data.vs2);
// Serial.print("\t");


// Serial.print("S3=");
// Serial.print(data.vs3);
// Serial.print("\t");


// Serial.print("S4=");
// Serial.print(data.vs4);
// Serial.print("\t");

// Serial.print("J2S=");
// Serial.print(data.vj2s);
// Serial.print("\t");


// Serial.print("P1=");
// Serial.print(data.vp1);
// Serial.print("\t\t");

// Serial.print("P2=");
// Serial.print(data.vp2);
// Serial.print("\t\t");

// Serial.print("J1X=");
// Serial.print(data.vj1x);
// Serial.print("\t\t");


// Serial.print("J1Y=");
// Serial.print(data.vj1y);
// Serial.print("\t\t");

// Serial.print("J2X=");
// Serial.print(data.vj2x);
// Serial.print("\t\t");


// Serial.print("J2Y=");
// Serial.print(data.vj2y);
// Serial.println("\t\t");
// }
