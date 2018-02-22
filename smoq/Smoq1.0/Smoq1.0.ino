/*
 Smoq Project by Theex.org
 Enviromental Project Section based on Internet of Things
 This code is in the private domain

 This project also in github.com/theex-project/SmartIotProjects
 Regards, Developer

 Copyright (c) 2016 Copyright Holder All Rights Reserved.
*/

//define libraries
#include "DHT.h"
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

//define pins
#define DHTPIN 4
#define LEDPIN 13

//define global variables
DHT dht(DHTPIN, DHT22);
const int MQ2PIN = A0;
const int MQ7PIN = A1;
const int MQ135PIN = A2;
const int CURRENTPIN = A3;
const char payload_length = 32;
byte data[payload_length];

void sendData(float sensorParam) {
  String sensorVal = String(sensorParam);
  char data[32];
  sensorVal.toCharArray(data, 32);
  Mirf.send((byte*) data);
  while (Mirf.isSending()) {
    /* code */
  }
  delay(1000);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(DHTPIN, INPUT);
  pinMode(MQ2PIN, INPUT);
  pinMode(MQ7PIN, INPUT);
  pinMode(MQ135PIN, INPUT);
  pinMode(CURRENTPIN, INPUT);
  pinMode(LEDPIN, OUTPUT);
  dht.begin();
  //NRF
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  Mirf.setTADDR((byte *)"serve");
  Mirf.payload = payload_length;
  Mirf.channel = 201;
  Mirf.config();
}

void loop() {
  // put your main code here, to run repeatedly:
  float mq2Value = sensorValue(MQ2PIN);
  Serial.print("mq2Value = ");
  Serial.println(mq2Value);

  float mq7Value = sensorValue(MQ7PIN);
  Serial.print("mq7Value = ");
  Serial.println(mq7Value);

  float mq135Value = sensorValue(MQ135PIN);
  Serial.print("mq135Value = ");
  Serial.println(mq135Value);

  float currentValue = sensorValue(CURRENTPIN);
  Serial.print("currentValue = ");
  Serial.println(currentValue);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  //decision maker
  if ((mq2Value>100) || (mq7Value>100) || (mq135Value>100)) {
    digitalWrite(LEDPIN, HIGH);
  } else {
    digitalWrite(LEDPIN, LOW);
  }

  if (currentValue>10) {
    digitalWrite(LEDPIN, HIGH);
  } else {
    digitalWrite(LEDPIN, LOW);
  }

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  } else {
    Serial.print("Humidity = ");
    Serial.println(h);
    Serial.print("Temperature = ");
    Serial.println(t);
  }

  sendData(mq2Value);
  sendData(mq7Value);
  sendData(mq135Value);
  sendData(h);
  sendData(t);
  sendData(currentValue);

  Serial.println();
  delay(1000);
}

float sensorValue(int pin) {
  //CURRENTPIN
  if (pin == CURRENTPIN) {
    float temp = (analogRead(pin)*(5.0/1023.0));
    float adcVolt = abs(temp-2.5);
    adcVolt /= 0.185;
    adcVolt *= 1000;
    return adcVolt;
  } else {
    return (analogRead(pin)*0.004882814);
  }
}
