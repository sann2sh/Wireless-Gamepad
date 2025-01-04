#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00000";

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
  Serial.begin(115200);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening(); // Set the module as receiver
}

void loop() {
  if (radio.available()) {
    radio.read(&data, sizeof(package));

    // Send start marker, data, and end marker
    Serial.write('<'); // Start marker
    Serial.write((byte*)&data, sizeof(package)); // Data
    Serial.write('>'); // End marker
  }
}
