#include <Servo.h>

Servo trigger;
Servo trigger2;
Servo container;

int post = 0;
int posc = 0;

const int buttonPin1 = 2;     // the number of the pushbutton pin
const int buttonPin2 = 4;
     // the number of the LED pin
// variables will change:
int buttonState1 = 0;     
int buttonState2 = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  trigger.attach(9);
  trigger2.attach(11);
 container.attach(13);
  container.write(90);
    trigger.write(163);
      trigger2.write(180);


}

void loop() {

   if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if(data.toInt() == 1)
    {
      trigger.write(45);
      delay(100); 
      //container.write(94);
      //delay(100); 
      //container.write(90);
      //delay(100); 
      //container.write(86);
      //delay(100); 
      //container.write(90);
      //delay(100); 
      trigger2.write(0);
      delay(200); 
      trigger.write(163);
      delay(100); 
      trigger2.write(180);
      delay(500); 
      goPos();
      delay(100); 
     
    }
     if(data.toInt() == 0)
    {
      trigger.write(164);
      trigger2.write(180);
    }
    if(data.toInt() == 2)
    {
      for(int i =0; i<10; i++)
      {
        goPos();
        delay(1000);
      }
    }
    if(data.toInt() == 3){
      goPos();
    }
  if(data.toInt() == 4)
    {
      trigger.write(45);
      delay(100); 
      //container.write(94);
      //delay(100); 
      //container.write(90);
      //delay(100); 
      //container.write(86);
      //delay(100); 
      //container.write(90);
      //delay(100); 
      trigger2.write(0);
      delay(200); 
      trigger.write(163);
      delay(100); 
      trigger2.write(180);
      delay(500); 
     
    }
    }
 

    

}

void goPos()
{
      delay(1000);
      buttonState1 = HIGH; 
      buttonState2 = HIGH;
      while(buttonState1 == HIGH && buttonState2 == HIGH)
      {
      Serial.println("trying");
      container.write(75);
      delay(5);
      buttonState1 = digitalRead(buttonPin1);
      buttonState2 = digitalRead(buttonPin2);
      }
      container.write(90);

}
