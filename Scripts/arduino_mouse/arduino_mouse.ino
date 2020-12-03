#include <Mouse.h>
int vary = 0;
int varx = 0;
void setup() {
  Serial.begin(9600);
  Mouse.begin();
}

void loop() {
  while (!Serial.available()){}
  if (Serial.available() > 0) {
    varx = Serial.read();
    delay(50);
    vary = Serial.read();
    Mouse.move(varx,vary,0);
    //delay(1000);
  }
}
