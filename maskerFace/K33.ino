#include <Servo.h>
#include <LiquidCrystal.h>
#define Trigpin 8
#define Echopin 9

long duration,distance;
Servo servo_ibnu;

const int pompa = 11;
const int ir = 13;

int bacaSensor;

void setup() { 
  pinMode(ir, INPUT);
  pinMode(pompa, OUTPUT);
  pinMode (Trigpin, OUTPUT);
  pinMode (Echopin, INPUT);
  servo_ibnu.attach(10);
  servo_ibnu.write(0);
}

void loop() {

  digitalWrite(Trigpin, LOW);
  delay(2);
  digitalWrite(Trigpin, HIGH);
  delay(10);
  digitalWrite(Trigpin, LOW);
  duration=pulseIn (Echopin, HIGH);
  distance=duration/58,2;

  if (distance <10 && distance >0) {
    servo_ibnu.write(0);    
  }

  bacaSensor = digitalRead(ir);
  
  if (bacaSensor == LOW) {
    digitalWrite(pompa, LOW);
    servo_ibnu.write(90);
  } else {
    digitalWrite(pompa, HIGH);
  } 
}