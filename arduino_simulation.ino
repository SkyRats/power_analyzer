int i=100;
int led = 7;
int sup;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led,OUTPUT);
 }


void loop() 
{
      Serial.print('<');
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.print(i);
      Serial.print(',');
      Serial.println('>');
      delay(10000);
      Serial.flush();
      i++;
}
