let actors = new Map();
let structures = new Map();
let activites = new Map();
let stage = null;
let layer1 = null;
let layer2 = null;
let staticPoly = new Map();
let polyArray = new Map();
let camera = new Camera();

let a_c,ac_c = false;
let konvaInit = false;
/***
 *
 */
function initKonva() {

    stage = new Konva.Stage({
      container: 'container',  // id of container <div>
        width: 1000,
        height: 1000
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


    stage.add(layer1);
    stage.add(layer2);
    layer2.moveToTop();
    console.log( "ready!" );
}

/***
 *
 */
function initActors() {
    if(!konvaInit){
        initKonva();
        konvaInit = true;
    }
    //generate polygons from actor
    actors.forEach((v, k) => {

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
            layer1.batchDraw();
        });
    });
}

/***
 *
 */
function initStructures() {
    if(!konvaInit){
        initKonva();
        konvaInit = true;
    }
    structures.forEach((v, k) => {
        let poly = new Konva.Line({
            points: konvaShape(v.shape),
            fill: '#0ca307',
            stroke: 'black',
            strokeWidth: 1,
            closed: true,
        });
        layer2.add(poly)
        staticPoly.set(k, poly);
        poly.on('structureCollision', (evt) => {
            poly.attrs.fill = '#e21d00';
            layer2.draw();
        });
    });
}

/***
 *
 */
function initActivites(){
    if(!konvaInit){
        initKonva();
        konvaInit = true;
    }
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
            layer1.batchDraw();
         });
    });


}


/***
 *
 * @param data
 */
function updateData(data){
    let dataEntries = data["payload"];

    if(actors.size === 0){
        dataEntries.forEach((v)=>{
            let actor = v["actor"];
            actors.set(actor["Name"], new Actor(actor["position"],actor["shape"],actor["Name"]));
        });
    }else {
        dataEntries.forEach((v)=>{
            let k = v["actor"];
            let actor = actors.get(k["Name"]);
            actor.pos = k["position"];
            actor.shape = k["shape"];
        });
    }

    if(!ac_c){
        initActors();
        ac_c = true;
    }


    actors.forEach((v,k)=>{
        let poly = polyArray.get(k);
        camera.updateTranslation();
        let shape = camera.translate(v.shape);

        poly.fire('moveEvent', shape);

    });

    layer1.batchDraw();

}

/***
 *
 * @param data
 */
function updateStructureData(data){
    let dataEntries = data["payload"];

    dataEntries.forEach((v)=>{
        let structure = v["structure"];
        structures.set(structure["Name"], new Structure(structure["position"],structure["shape"],structure["Name"]));
    });
    initStructures();
}


/***
 *
 * @param data
 */
function updateActivityData(data) {
    let dataEntries = data["payload"];
    if(activites.size === 0){
        dataEntries.forEach((v)=>{
            let activity = v["event"];
            activites.set(activity["Name"], new Activity(activity["position"],activity["Name"],activity["status"]));
        });
    }else{
        dataEntries.forEach((v)=>{
            let k = v["event"];
            let event = activites.get(activity["Name"])
            event.setStatus(k["status"]);
            event.fire('activityComplete',event.status);
        });
    }

    if(!a_c){
        initActivites();
        a_c = true
    }

}

/***
 *
 * @param vectorshape
 * @returns {[]}
 */
function konvaShape(vectorshape){
    let shape = [];
    for (let i = 0; i < vectorshape.length; i++){
        shape = shape.concat(vectorshape[i]);
    }
    return shape
}


