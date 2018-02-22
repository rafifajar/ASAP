#include <LiquidCrystal.h>

const int SmokeInPin = A2;
const int SmokeOutPin = A3;
const int COInPin = A1;
const int COOutPin = A4;
const int tempPin = A0;
const int fanPin = 13;

float temp, strTemp;
int SmokeInValue, SmokeOutValue, COInValue, COOutValue, sensorFan = 0;
int strSmokeIn, strSmokeOut, strCOIn, strCOOut, strFan = 0;
int maxSense = 300;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(SmokeInPin, INPUT);
  pinMode(SmokeOutPin, INPUT);
  pinMode(COInPin, INPUT);
  pinMode(COOutPin, INPUT);
  pinMode(tempPin, INPUT);
  pinMode(fanPin, OUTPUT);

 }

void loop() {
  //  char d = ' ';
  //  while (Serial.available() > 0) {
  //    d = Serial.read();
  //  }
  //
  temp = analogRead(tempPin);
  temp = temp * 0.48828125;
  //Serial.print("TEMPRATURE = ");
  //Serial.print(temp-15);
  //Serial.print("*C");
  //Serial.println(temp-15);

  //  if(SmokeOutValue > SmokeInValue){
  //    Serial.println("Overlap!");
  //    Serial.println(" ");
  //  } else {
  //    Serial.println(" ");
  //  }

  //Serial.println("***MQ2 HERE***");
  SmokeInValue = analogRead(SmokeInPin);
  SmokeOutValue = analogRead(SmokeOutPin);
  //Serial.print("In : ");
  //Serial.println(SmokeInValue);
  //Serial.print("Out : ");
  //Serial.println(SmokeOutValue);
  //Serial.println(" ");

  //Serial.println("***MQ7 HERE***");
  COInValue = analogRead(COInPin);
  COOutValue = analogRead(COOutPin);
  //Serial.print("In : ");
  //Serial.println(COInValue);
  //Serial.print("Out : ");
  //Serial.println(COOutValue);

  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.print("data udara: ");
  lcd.print(SmokeInValue);
  lcd.print("  %\t"); 

  if (COInValue >= maxSense || SmokeInValue >= maxSense) {
    digitalWrite(fanPin, HIGH);
    lcd.setCursor(0, 1);
    lcd.print("BAHAYA");
  } else {
    digitalWrite(fanPin, LOW);
    lcd.setCursor(0, 1);
    lcd.print("AMAN");
  }
  sensorFan = digitalRead(fanPin);
  //Serial.println(sensorFan);
  //
  //  if (COOutValue >= maxSense || SmokeOutValue >= maxSense) {
  //    digitalWrite(ledPin, HIGH);
  //  } else {
  //    digitalWrite(ledPin, LOW);
  //  }

  //  if (d == '1'){
  //    strTemp = temp;
  //    strSmokeIn = SmokeInValue;
  //    strSmokeOut = SmokeOutValue;
  //    strCOIn = COInValue;
  //    strCOOut = COOutValue;
  //    strFan = sensorFan;
  //  } else {
  //    strTemp = 0;
  //    strSmokeIn = 0;
  //    strSmokeOut = 0;
  //    strCOIn = 0;
  //    strCOOut = 0;
  //    strFan = 0;
  //  }

  Serial.println(temp);
  Serial.println(SmokeInValue);
  Serial.println(SmokeOutValue);
  Serial.println(COInValue);
  Serial.println(COOutValue);
  Serial.println(sensorFan);

  delay(1000);
}
