/*  
 *  *** NeoCortex 2023 ***
 *  IMU NO-BUTTONS FIRMWARE
 *
 *  This program controls the non-button IMU module
 */
#include <Wire.h>
#include <esp_now.h>
#include <Adafruit_NeoPixel.h>
#include "WiFi.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// Neopixel LED pin
#define PIN        23
// How many NeoPixels are attached to the Arduino
#define NUMPIXELS 3
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

// Interrupt data received flag
volatile uint8_t flag_receive = 0;

// IMU module features data structure
int id = 2;
int Xacc1 = 0;
int Yacc1 = 0;
int Zacc1 = 0;
int Xori1 = 0;
int Yori1 = 0;
int Zori1 = 0;
int Xmag1 = 0;
int Ymag1 = 0;
int Zmag1 = 0 ;
int Xgyro1 = 0;
int Ygyro1 = 0;
int Zgyro1 = 0;
int Xrot1 = 0;
int Yrot1 = 0 ;
int Zrot1 = 0;
int Xlin1 = 0;
int Ylin1 = 0;
int Zlin1 = 0;
int Xgrav1 = 0;
int Ygrav1 = 0;
int Zgrav1 = 0;
int Sample = 100;


/* Set the delay between fresh samples */
uint16_t BNO055_SAMPLERATE_DELAY_MS = 80;

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);

uint8_t broadcastAddress[] = {0x4C, 0x75, 0x25, 0x31, 0xA9, 0x47};
uint8_t IMUnoButtonAddress[] = {0x24, 0x4C, 0xAB, 0x82, 0xFC, 0x2C};
uint8_t IMUwithButtonAddress[] = {0x24, 0x4C, 0xAB, 0x82, 0xF6, 0x40};

#define BOARD_ID 1

typedef struct struct_message {
    int id;
    int Xacc ;
    int Yacc ;
    int Zacc ;
    int Xori ;
    int Yori ;
    int Zori ;
    int Xmag ;
    int Ymag ;
    int Zmag ;
    int Xgyro ;
    int Ygyro ;
    int Zgyro ;
    int Xrot ;
    int Yrot ;
    int Zrot ;
    int Xlin ;
    int Ylin ;
    int Zlin ;
    int Xgrav ;
    int Ygrav ;
    int Zgrav ;
} struct_message;

struct_message myData;
unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

esp_now_peer_info_t peerInfo;


void setup() {
  // Setup Neopixel LEDs
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear(); // Set all pixel colors to 'off'

  // Open USART at 115200 baud rate
  Serial.begin(115200);

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  } 

  // Callback function executed when ESP data is sent
  esp_now_register_send_cb(OnDataSent);
  // Callback function executed when ANY ESP data is received
  esp_now_register_recv_cb(OnDataRecv);
  
  // Pair the receiver ESP only
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  // Pair RECEIVER  
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Wait after the connection
  delay(1000);
}

void loop() {
  // Set LEDs as BLUE at the start
  for(int i=0; i<NUMPIXELS; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(0, 0, 150));
    pixels.show();
  }

  // Wait for data receive flag (triggered by the button on the second IMU)
  while(!flag_receive);

  // Clear the receive flag immediately
  flag_receive = 0;

  // Clear LEDs after the press (on the second IMU)
  for(int i=0; i<NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    pixels.show();
  }

  // 4 seconds for preparation for the tenniss serve
  delay(4000);

  // Set LEDs as GREEN : Data Collection In Progress
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 150, 0));
    pixels.show();
  }


  // Data collection cycle. Number of iteration depends on the number of data points desired per serve
  for(int i=0; i <= Sample; i++){
    sensors_event_t orientationData , angVelocityData , linearAccelData, magnetometerData, accelerometerData, gravityData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
    bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
    bno.getEvent(&magnetometerData, Adafruit_BNO055::VECTOR_MAGNETOMETER);
    bno.getEvent(&accelerometerData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
    bno.getEvent(&gravityData, Adafruit_BNO055::VECTOR_GRAVITY);

    printEvent(&orientationData);
    printEvent(&angVelocityData);
    printEvent(&linearAccelData);
    printEvent(&magnetometerData);
    printEvent(&accelerometerData);
    printEvent(&gravityData);

    // uint8_t system, gyro, accel, mag = 0;
    // bno.getCalibration(&system, &gyro, &accel, &mag);
    // Serial.println();
    // Serial.print(i);
    // Serial.print("Calibration: Sys=");
    // Serial.print(system);
    // Serial.print(" Gyro=");
    // Serial.print(gyro);
    // Serial.print(" Accel=");
    // Serial.print(accel);
    // Serial.print(" Mag=");
    // Serial.println(mag);
    // Serial.println("--");

    // In-sample delay
    delay(80);  
  }

  // Set LEDs as BLUE
  for(int i=0; i<NUMPIXELS; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 0, 150));
    pixels.show();
  }

  // End of data collection cycle

}



void printEvent(sensors_event_t* event) {
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  if (event->type == SENSOR_TYPE_ACCELEROMETER) {
    Xacc1 = event->acceleration.x;
    Yacc1 = event->acceleration.y;
    Zacc1 = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_ORIENTATION) {
    Xori1 = event->orientation.x;
    Yori1 = event->orientation.y;
    Zori1 = event->orientation.z;
  }
  else if (event->type == SENSOR_TYPE_MAGNETIC_FIELD) {
    Xmag1 = event->magnetic.x;
    Ymag1 = event->magnetic.y;
    Zmag1 = event->magnetic.z;
  }
  else if (event->type == SENSOR_TYPE_GYROSCOPE) {
    Xgyro1 = event->gyro.x;
    Ygyro1 = event->gyro.y;
    Zgyro1 = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_ROTATION_VECTOR) {
    Xrot1 = event->gyro.x;
    Yrot1 = event->gyro.y;
    Zrot1 = event->gyro.z;
  }
  else if (event->type == SENSOR_TYPE_LINEAR_ACCELERATION) {
    Xlin1 = event->acceleration.x;
    Ylin1 = event->acceleration.y;
    Zlin1 = event->acceleration.z;
  }
  else if (event->type == SENSOR_TYPE_GRAVITY) {
    Xgrav1 = event->acceleration.x;
    Ygrav1 = event->acceleration.y;
    Zgrav1 = event->acceleration.z;
  }
  else {

  }


  if ((millis() - lastTime) > timerDelay) {
    myData.Xacc = Xacc1;
    myData.Yacc= Yacc1; 
    myData.Zacc = Zacc1 ;
    myData.Xori = Xori1 ;
    myData.Yori = Yori1 ;
    myData.Zori = Zori1;
    myData.Xmag = Xmag1;
    myData.Ymag = Ymag1;
    myData.Zmag = Zmag1 ;
    myData.Xgyro = Xgyro1 ;
    myData.Ygyro = Ygyro1;
    myData.Zgyro = Zgyro1;
    myData.Xrot = Xrot1;
    myData.Yrot = Yrot1;
    myData.Zrot = Zrot1 ;
    myData.Xlin = Xlin1;
    myData.Ylin = Ylin1;
    myData.Zlin = Zlin1 ;
    myData.Xgrav = Xgrav1;
    myData.Ygrav = Ygrav1;
    myData.Zgrav =Zgrav1 ;
   
  
    //Send message via ESP-NOW
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));


   
    if (result == ESP_OK) {
      Serial.println("Sent with success");
    }
    else {
      Serial.println("Error sending the data");
    }
  }  
}


// ********** FUNCTIONS DEFINITIONS **********

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void OnDataRecv(const unsigned char * mac_addr, const unsigned char *incomingData, int len) {
  char macStr[18];
  Serial.printf("Packet received from IMU Button: %d \n", &incomingData);

  // Trigger flag receive to begin data collection cycle in the loop()
  flag_receive = 1;
  
}
