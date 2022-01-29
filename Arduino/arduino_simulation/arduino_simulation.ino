int i=100;
int led = 7;
int sup;


void format_and_send(int voltage, int current, int thrust);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led,OUTPUT);
 }


void loop() 
{
      format_and_send(i, i, i);
      i++;
}

void format_and_send(int voltage, int current, int thrust){
    Serial.print('<');
    Serial.print(',');
    Serial.print(voltage);
    Serial.print(',');
    Serial.print(current);
    Serial.print(',');
    Serial.print(thrust);
    Serial.print(',');
    Serial.println('>');
    delay(100);
    Serial.flush();
}
