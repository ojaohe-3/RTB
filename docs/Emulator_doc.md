# Emulator

## Classes
  * Emulator
  * SiteObject
  * Actor
  * Activity
  * Collision
  * Map
  * Structure

  
  ### Emulator class
   Emulator class is an class for producing data sending it to RabbitMQ.
   Life time is simply to produce data, only one class object is needed.
   It handles internaly the connection setup and obtains connection information from config.toml as it is not meant to be a dynamic system but more of a test.
  no relavent attributes
   
   #### Methods
   ```python
    def send_message(self, msg, routing_key):
   ```
  Is a method to send msg with routing_key. routing_key is meant for what channel RabbitMQ should post the connection, for the test "send_exchange" is the only valid, but the method
 was meant to be future prof
 
 ```python
    def get_sensor_data(self, object):
 ```
   meant to gather the data from an SiteObject class, and gets a json with a timestamp (for logging), Object Type and payload with relevant position data, name and polygon shape
   
   ### SiteObject class
   Site Object is meant to repricent all object as a super, it contains relevant information as attribute share for all object that is to be mapped.
   it has a position vector, a shape polygon and internally it generates a radius attribute with the largest drawable circle, it was intended for collision but is since not in use.
   
   * pos Position point [x,y] where x,y is float
   * shape Polygon [[x1,y2],[x2,y2],...,[xn,yn]] where x,y if float
   * name string
   * radius float
   #### Methods
   ```python
    def toJson(self):
   ```
   Generates a Json from its own attributes
   
   ### Actor class
   Actor is a movable object on the screen, it inherits SiteObject but have additional attributes such as velocity vel (a magnitude of a vector) and a type  
  * vel float magnitude of a vector
  * type_ string
  * activity Activity scheduler object, future might include an accual schedual
  * status string indicator of object being in use or not, is not implemented yet
  
  #### Methods 
  ```python
    def updatePos(self,npos):
   ```
   Generates an velocity vector with the npos <- self.pos vector as direction, it then takes a step in that direction.
   
   ```python
    def setPos(self,npos):
   ```
  Sets the position of the actor without taking any steps.
  
 ### Activity class
 An activity is an objectiv for actor, it has a lifetime and is ultimatly simulate work being done. Is a child of SiteObject
 * stime Start time, float
 * type string
 * status string, its current status
 #### Methods 
  ```python
    def isActive(self):
   ```
   returns a boolean True if it is active, active as in current status is not completed, inactive or likewise status indicators and it is time to activate.
   
   
  ### Collision
  [JuantAldea separting-Axis-Theorem](https://github.com/JuantAldea/Separating-Axis-Theorem)
 
 ### Map class
 just contains a polgon shape. not really relavent as of yet
 * shape polygon [[x1,y1],[x2,y2],...,[xn,yn]]
 ### Structure class
 generates Static objects, it has no intention of moving and works as an obstacle of actors, is a chilf of SiteObject
 no attributes
 #### Methods
  ```python
     def generateConvexStructure(self, edges,size):
  ```
  generates an convex shape polygond, it takes edges and size (maximum magnitude between to vectors in the shape) and is called on object creation with random parameters. 
 
 
