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

   
  
