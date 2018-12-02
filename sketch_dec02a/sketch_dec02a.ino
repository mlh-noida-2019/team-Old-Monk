
#include <GSM.h>

#define PINNUMBER ""

GSM gsmAccess;
GSM_SMS sms;

void setup()
{
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  
  Serial.println("SMS Messages Sender");

  boolean notConnected = true;

  while(notConnected)
  {
    if(gsmAccess.begin(PINNUMBER)==GSM_READY)
      notConnected = false;
    else
    {
      Serial.println("Not connected");
      delay(1000);
    }
  }
  
  Serial.println("GSM initialized");
}

void loop()
{

    
  Serial.print("Enter SMS content: ");
  char *txtMsg = "Null";
  readSerial(txtMsg);
  Serial.println("SENDING");
  Serial.println();
  Serial.println("Message:");
  Serial.println(txtMsg);
  while(txtMsg != "Null"){
   ;
  }
  sms.beginSMS("7379445111");
  sms.print(txtMsg);
  sms.endSMS(); 
  Serial.println("\nCOMPLETE!\n");
}

int readSerial(char result[])
{
  int i = 0;
  while(1)
  {
    while (Serial.available() > 0)
    {
      char inChar = Serial.read();
      if (inChar == '\n')
      {
        result[i] = '\0';
        Serial.flush();
        return 0;
      }
      if(inChar!='\r')
      {
        result[i] = inChar;
        i++;
      }
    }
  }
}
