let actors = new Map();
let stage = null;
let layer1 = null;
let polyArray = new Map();
let camera = new Camera();
function init(){

    stage = new Konva.Stage({
      container: 'container',   // id of container <div>
      width: 1920,
      height: 600
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
            layer1.draw();
         });
    });
    stage.add(layer1);
    //update(layer1);
    console.log( "ready!" );
}




//will be called via ajax
function updateData(data){
    let dataEntries = data["payload"];

    dataEntries.forEach((v)=>{
        let actor = v["actor"];
        actors.set(actor["Name"], new Actor(actor["position"],actor["shape"],actor["Name"]));
    });


    if(polyArray.size !== actors.size) {
        init();
    }else{
        actors.forEach((v,k)=>{
            let poly = polyArray.get(k);
            camera.updateTranslation();
            let shape = camera.translate(v.shape);

            poly.fire('moveEvent', shape);

        });

        layer1.draw();
    }
}


function konvaShape(vectorshape){
    let shape = [];
    for (let i = 0; i < vectorshape.length; i++){
        shape = shape.concat(vectorshape[i]);
    }
    return shape
}
