#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

std_msgs::Float32 msg1;
std_msgs::Float32 msg2;
ros::Publisher chatter("chatter", &msg1);
ros::Publisher vel("vel", &msg2);

int encoderPin1 = 2;
int encoderPin2 = 3;

volatile int lastEncoded = 0;
volatile float encoderValue = 0;
volatile float time1 = 0;
volatile float time2 = 0;
long lastencoderValue = 0;
volatile float dt = 0;
volatile float velocity;
int lastMSB = 0;
int lastLSB = 0;

void setup()
{
  nh.initNode();
  nh.advertise(chatter); //publishes chatter to ros
  nh.advertise(vel);     //publishes rpm to ros
  Serial.begin(2000000);

  pinMode(encoderPin1, INPUT);
  pinMode(encoderPin2, INPUT);

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3)
  attachInterrupt(0, updateEncoder, CHANGE);
  attachInterrupt(1, updateEncoder, CHANGE);
}

void loop()
{
  msg1.data = encoderValue;
  msg2.data = velocity;

  nh.spinOnce();
  //Serial.println(dt);
  //Serial.println(time2);
  //Serial.println(time1);
  //Serial.println(velocity);
}

void updateEncoder()
{
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) | LSB;         //converting the 2 pin value to single number
  int sum = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
    encoderValue++;
  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
    encoderValue--;

  time1 = millis();
  if (time2 != 0)
  {
    dt = time1 - time2;
  }
  else
  {
    dt = time1;
  }
  velocity = (5 * 0.000078914 * 1600 * 100 * 3600) / (1600 * dt); //in miles per hour
  time2 = time1;
  Serial.println(velocity);

  chatter.publish(&msg1);
  vel.publish(&msg2);

  lastEncoded = encoded; //store this value for next time
}
