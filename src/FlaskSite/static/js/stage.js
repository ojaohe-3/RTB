let actors = new Map();
let structures = new Map();
let activites = new Map();
let stage = null;
let layer1 = null;
let layer2 = null;
let staticPoly = new Map();
let polyArray = new Map();
let camera = new Camera();
function init(){

    stage = new Konva.Stage({
      container: 'container'  // id of container <div>

    });
    var container = stage.container();
      // make it focusable

      container.tabIndex = 1;
      // focus it
      // also stage will be in focus on its click
      container.focus();


       container.addEventListener('keydown', function (e) {
        switch (e.keyCode) {
            case 82:
                camera.zoom -= 0.1;
                break;
            case 70:
                camera.zoom += 0.1;
                break;
            case 81:
                  camera.theta+=0.01;
                  break;
            case 69:
                  camera.theta-=0.01;
                break;
            case 37:
            case 65:
                camera.pos[0] -= 15;
                break;
            case 38:
            case 87:
                camera.pos[1] -= 15;
                break;
            case 39:
            case 68:
                camera.pos[0] += 15;
                break;
            case 40:
            case 83:
                camera.pos[1] += 15;
                break;
            default:
                break;
        }

        camera.updateTranslation();
        e.preventDefault();
        layer1.batchDraw();
      });

    layer1 = new Konva.Layer();
    layer2 = new Konva.Layer();
    //generate polygons from actor
    actors.forEach((v,k)=>{

         let poly = new Konva.Line({
            points: konvaShape(v.shape),
            fill: '#00D2FF',
            stroke: 'black',
            strokeWidth: 1,
            closed: true,
          });
         polyArray.set(k, poly);
         layer1.add(poly);
         poly.on('moveEvent', (evt) => {
            poly.attrs.points = konvaShape(evt);
            layer1.Batchdraw();
         });
    });

    structures.forEach((v,k)=>{
        let poly = new Konva.Line({
            points: konvaShape(v.shape),
            fill: '#0ca307',
            stroke: 'black',
            strokeWidth: 1,
            closed: true,
          });
        layer2.add(poly)
        staticPoly.set(k,poly);
        poly.on('structureCollision', (evt) => {
            poly.attrs.fill = '#e21d00';
            layer2.draw();
         });
    });

    activites.forEach((v,k)=>{
         let poly = new Konva.RegularPolygon({
             x: v.pos[0],
             y: v.pos[1],
             fill: '#00D2FF',
             sides : 3,
             radius: v.radius,
             stroke: 'black',
             strokeWidth: 1,
             closed: true,
          });
         polyArray.set(k, poly);
         layer1.add(poly);
         poly.on('activityComplete', (evt) => {
            if(evt)
                poly.attrs.fill = '#ff0000';
            else
                poly.attrs.fill = '#00d2ff';
            layer1.Batchdraw();
         });
    });


    stage.add(layer1);
    stage.add(layer2);
    layer2.moveToTop();
    //update(layer1);
    console.log( "ready!" );
}


/***
 * Updates by Ajax
 */
function updateData(data){
    let dataEntries = data["payload"];

    dataEntries.forEach((v)=>{
        let actor = v["actor"];
        actors.set(actor["Name"], new Actor(actor["position"],actor["shape"],actor["Name"]));
    });



    actors.forEach((v,k)=>{
        let poly = polyArray.get(k);
        camera.updateTranslation();
        let shape = camera.translate(v.shape);

        poly.fire('moveEvent', shape);

    });

    layer1.batchDraw();

}

function updateStructureData(data){
      let dataEntries = data["payload"];

    dataEntries.forEach((v)=>{
        let structure = v["structure"];
        actors.set(structure["Name"], new Structure(structure["position"],structure["shape"],structure["Name"]));
    });

}


function updateActivityData(data) {


}
function konvaShape(vectorshape){
    let shape = [];
    for (let i = 0; i < vectorshape.length; i++){
        shape = shape.concat(vectorshape[i]);
    }
    return shape
}
