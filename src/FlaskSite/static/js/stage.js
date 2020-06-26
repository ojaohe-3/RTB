let actors = new Map();
let stage = null;
let layer1 = null;
function init(){
    stage = new Konva.Stage({
      container: 'container',   // id of container <div>
      width: 600,
      height: 600
    });
    layer1 = new Konva.Layer();
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
    update();
}
function update()
{
    if(typeof layer1 === "undefined" || layer1 === null){
        init();
    }
    actors.forEach((value , key)=>{
        let shape = [];
        for (let i = 0; i < value.shape.length; i++){
            shape = shape.concat(value.shape[i]);
        }

             let poly = new Konva.Line({
        points: shape,
        fill: '#00D2FF',
        stroke: 'black',
        strokeWidth: 5,
        closed: true,
      });
        layer1.add(poly)
    })
    layer1.draw();
}
