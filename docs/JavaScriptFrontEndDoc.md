# Java Script Structure
packages :
* jQuery
* konva

classes:
* Activity
* Actor
* Structure
* Camera
* Globals (stage and ajax)

## Activity class
Ment to represent an activity from the simulation, represented as a triangle in konva.
attributes: 
  * pos [x,y] 
  * name unique name
  * status bool is it active?
  * radius float

## Actor class
Movable object, maintains only its attributes
attributes:
  * shape 2xn array
  * pos [x,y]
  * name unique name

## Structure class
 Same as Actor object, future proff.
 
## Camera class
  Translate the screen, allows rotation, translation (to its offset) and zoom. allow only one object per sceen
  
 attributes: 
  * pos [x,y] offset
  * zoom float 
  * transFormationMatrix 3x3 transformation matrix
### Methods
#### translate(shape)
       Translates a inputed shape to given transformation matrix, note there is some bug with position translatino
       when zoom is negative. also when zoom is close to zero,
       no motion is possible when zoom is zero (not weird since it is multiplicative to the translation),
       future the values will be clamped in a arbitrary region.
       
       returns translated shape 
       
#### translatePos(pos)
      Translates an position vector, same as translate shape.
      returns translated postion

####  generateTransformationMatrix()
      generates a translation matrix and store it localy, does return a transformation matrix given cameras attributes.
 
##### How to use
When writing a new shape, it when renderd must be translated
example: 
```javascript
 let shape = camera.translatePos(v.shape);
 poly.attr.shape = shape;
 draw();
```
## Stage.js and Globals
Globals is utillized to poll data from the backend and to print the new data on the screen. Polling was achived by ajax and simply request every 50ms for actors, 1000ms for activites though this feature is legacy for now.

attributes:
* actors : Map(string, Actor)
* activites: Map(string, Activites)
* structures: Map(string, Structures)
* polyArray: Map(string, Konva.shape)
* polyStatic: Map(string, Konva.shape)
* camera: Camera()
there is additional variables that are simply there for functional purposes. 
### Methods
#### Update Methods
Update is called from ajax and is continous for every actor and activity, updating the Map with respective class type as value.  
Structures does not update only initilazies first time it is sent, to keep it concurent with transformation when camera is moving we need to transform the motion through updateStatic.
```javascript
function updateStatic()
```
```javascript
function updateData(data)
```
```javascript
function updateActivityData(data)
```
```javascript
function updateStructureData(data)
```
#### init methods
During the first run, a lot of initilazion need to take place, first the stage objects need to be created with its layer. Secondly once one update have been done in 
Actor, Activity or structure is completed it need to be transformed to konva object to be drawn.
```javascript
function initKonva()
```

```javascript
function initActors() 
```
```javascript
function initStructures()
```
```javascript
function initActivites()
```

#### helper functions
Konva do not have an 2d array of points to represent points, instead its in the format x1,y1,x2,y2... etc. This converts the 2d array to konva compatible format.
```javascript
function konvaShape(vectorshape)
```

These are css related and simply on a buttom press from the main html toggle the objects visability on the screen. Implemented to support a checkbox and jquery.

```javascript
function setActors(attr)
```


```javascript
function setActivites(attr)
```


```javascript
function setStructures(attr)
```

