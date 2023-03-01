/*  
 *  *** NeoCortex 2023 ***
 *  ESP8266 IMU RECEIVER FIRMWARE
 *
 *  This program controls the receiver for two IMU modules concerned
 *  and sends their payload via USART.
 *
 *  Can also be connected to Arduino MKR0 to log data through the on-board
 *  micro SD memory card module (for example using Petit FatFS library)
 *
 */
#include <ESP8266WiFi.h>
#include <espnow.h>

char in[] = "in";
char out[] = "out";
char save[] = "save";
char nosave[] = "nosv";
char cam[]="sync";


// IMU module features data structure
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

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the readings from each board
struct_message board1;
struct_message board2;

// Create an array with all the structures
struct_message boardsStruct[2] = {board1, board2};

// Callback function that will be executed when data is received
void OnDataRecv(uint8_t * mac_addr, uint8_t *incomingData, uint8_t len) {
    if (!strcmp((char*)incomingData, cam)){
    Serial.printf("sync"); 
    Serial.println();
  }
  char macStr[18];
  //Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);

  


  if (!strcmp((char*)incomingData, in)){
    Serial.printf("in"); 
    Serial.println();
  }
  else if (!strcmp((char*)incomingData, out)){
    Serial.printf("out");
    Serial.println();
  }
  else if (!strcmp((char*)incomingData, nosave)){
    Serial.printf("nosave");
    Serial.println();
  }
  else if (!strcmp((char*)incomingData, save)){
    Serial.printf("save");
    Serial.println();
  }
  else{
    memcpy(&myData, incomingData, sizeof(myData));
    
    
    // Xacc, Yacc, Zacc, Xori, Yori, Zori, Xmag, Ymag ,Zmag, Xgyro, Ygyro, Zgyro, Xrot, Yrot, Zrot, Xlin,Ylin, Zlin, Xgrav, Ygrav, Zgrav); //21
    Serial.printf("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",myData.Xacc, myData.Yacc, myData.Zacc, myData.Xori, myData.Yori, myData.Zori, myData.Xmag, myData.Ymag , myData.Zmag, myData.Xgyro, myData.Ygyro, myData.Zgyro, myData.Xrot, myData.Yrot, myData.Zrot, myData.Xlin,myData.Ylin, myData.Zlin, myData.Xgrav, myData.Ygrav, myData.Zgrav);
    Serial.println();
  }
}
 

void setup() {

  // Open USART at 115200 baud rate
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Callback function executed when ANY ESP data is received
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);
}

void loop(){

  // Keep this loop empty

}