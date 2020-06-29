let actors = new Map();
let stage = null;
let layer1 = null;
let polyArray = new Map();
function init(){
    stage = new Konva.Stage({
      container: 'container',   // id of container <div>
      width: 600,
      height: 600
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
        actor = v["actor"];
        actors.set(actor["Name"], new Actor(actor["position"],actor["shape"],actor["Name"]));
    });


    if(polyArray.size !== actors.size) {
        init();
    }else{
        actors.forEach((v,k)=>{
            let poly = polyArray.get(k);
            poly.fire('moveEvent',v.shape);

        })
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