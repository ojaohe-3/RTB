# Emulator

## Classes
  * Emulator
  * Activity
  * Collision
  * Map
  * Structure
  * Actor
  
  ### Emulator class
   Emulator class is an class for producing data sending it to RabbitMQ.
   Life time is simply to produce data, only one class object is needed.
   It handles internaly the connection setup and obtains connection information from config.toml as it is not meant to be a dynamic system but more of a test.
  
   
   #### Methods
   ```python
    def send_message(self, msg, routing_key):
   ```
  Is a method to send msg with routing_key. routing_key is meant for what channel RabbitMQ should post the connection, for the test "send_exchange" is the only valid, but the method
 was meant to be future prof
 
 ```python
    def get_sensor_data(self, object):
 ```
   meant to
   
   
  
  
