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
    Serial.write(varx);
    delay(50);
    vary = Serial.read();
    Serial.write(vary);
    Mouse.move(varx,vary,0);
    //delay(1000);
  }
}
