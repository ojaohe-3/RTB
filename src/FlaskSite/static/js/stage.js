let actors = new Map();
let structures = new Map();
let activites = new Map();
let stage = null;
let layer1 = null;
let staticPoly = new Map();
let polyArray = new Map();
let camera = new Camera();

let a_c,ac_c = false;
let konvaInit = false;
function updateStatic() {
    camera.updateTranslation();
    structures.forEach((v,k)=>{
       let poly = staticPoly.get(k);
       poly.fire("structureEvent", camera.translate((v.shape)));
    });
    activites.forEach((v,k)=>{
       let poly = polyArray.get(k);
       poly.fire("activityEvent", camera.translatePos(v.pos), v.status);
    });

    layer1.batchDraw();
}

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

        updateStatic();
        e.preventDefault();
        layer1.batchDraw();
      });

    layer1 = new Konva.Layer();


    stage.add(layer1);
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
        layer1.add(poly)
        staticPoly.set(k, poly);
        poly.on('structureEvent', (evt) => {
            poly.attrs.fill = '#e21d00';
            poly.attrs.points = konvaShape(evt);
            layer1.batchDraw();
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
         poly.on('activityEvent', (pos,status) => {
            poly.attrs.visible = status;
            poly.x( pos[0]);
            poly.y( pos[1]);
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
        updateStatic();
        poly.fire('moveEvent', shape);

    });
}

/***
 *
 * @param data
 */
function updateStructureData(data){
    let dataEntries = data["payload"];

    dataEntries.forEach((v)=>{
        let structure = v["structure"];
        structures.set(structure["Name"], new Structure(structure["shape"],structure["position"],structure["Name"]));
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
            let activity = v["events"];
            activites.set(activity["Name"], new Activity(activity["position"],activity["Name"],activity["status"]));
        });
    }else{
        dataEntries.forEach((v)=>{
            let k = v["events"];
            let event = activites.get(k["Name"])
            event.setStatus(k["status"]);
        });
    }

    if(!a_c){
        initActivites();
        a_c = true
    }
        activites.forEach((v,k)=>{
            let poly = polyArray.get(k);
            camera.updateTranslation();
            let pos = camera.translatePos(v.pos);
            poly.fire('activityEvent', pos, v.status);

    });
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
