#include <WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

Servo servo1;

#define pinEcho 22
#define pinTrig 23
float durasi, jarak;

const int led1=LED_BUILTIN;
const int led2merah=18;
const int led3hijau=21;
static const int servoPin=12;

//buzzer
const int buzzer=19;
int freq = 2000;
int channel = 0;
int resolution = 10;

// Replace the next variables with your SSID/Password combination
const char *ssid ="asesor2";
const char *password ="coomputerstore4.0";

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.11";

const char* mqtt_server ="192.168.43.201";
const char* topic ="jarak1";

long lastMsg =0;
char msg[50];
int value =0;
char data[5];

WiFiClient espClient;
PubSubClient client(espClient);

void alarmbuka(){
  digitalWrite(led3hijau, HIGH); 
  ledcAttachPin(buzzer, channel);
  
  ledcWrite(channel, 1024);
  ledcWriteTone(channel, 4000);
  
  servo1.attach(servoPin);
  servo1.write(90);
  delay(3000);
  servo1.write(0);
  delay(500);
  
  ledcWriteTone(channel, 0);
  digitalWrite(led3hijau, LOW);
    
}


void alarmtutup(){
  for (int i=0; i<=10; i++){
  digitalWrite(led2merah, HIGH); 
  ledcAttachPin(buzzer, channel);
  ledcWrite(channel, 1024);
  ledcWriteTone(channel, 4000);
  delay(50);
  ledcWriteTone(channel, 0);
  digitalWrite(led2merah, LOW);
  delay(50);
  }
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while(WiFi.status() !=WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.begin(115200);
    pinMode(36, INPUT);
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  for(int i =0; i <length; i++) {
    Serial.print((char)message[i]);
    messageTemp +=(char)message[i];}
    Serial.println();
      if(messageTemp=="1"){
      alarmbuka();
    }else{
      alarmtutup();
    }
}

void reconnect() {
  // Loop until we're reconnected
  while(!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if(client.connect("ESP8266Client")) {
      Serial.println("connected");
      //Subscribe
      client.subscribe("servo");
      }
      else
      {
        Serial.print("failed, rc=");
        Serial.print(client.state());
        Serial.println(" try again in 5 seconds");
        // Wait 5 seconds before retrying
        delay(5000);
      }
    }
  }

void setup() {
  Serial.begin(115200);
 
  pinMode(pinTrig, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2merah, OUTPUT);
  pinMode(led3hijau, OUTPUT);
  pinMode(pinEcho, INPUT);
  
  ledcSetup(channel, freq, resolution);
  
  ledcAttachPin(19, channel);
  
  servo1.attach(servoPin);
  
  setup_wifi();
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}


void loop() {
  if(!client.connected()) {
    reconnect();
    }
    client.loop();
    digitalWrite(pinTrig, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinTrig, LOW);
    delayMicroseconds(8);
    
    durasi = pulseIn(pinEcho, HIGH);
    jarak = durasi / 1000000 / 2 * 340 * 100;
    Serial.print("Jarak : ");
    Serial.print(jarak);
    Serial.println(" cm");
    delay(1000);
    
    if(jarak<=10){
      snprintf(data, 5, "%f", jarak);
      Serial.println(data);
      client.publish(topic,data);
      delay(3000);
      //alarmbuka();
    }

    

}
