let actors = new Map();

//will be called via ajax
function updateData(data){
    data.forEach((v) => {
        console.log(v);
    })
}
function update(layer)
{
    actors.forEach((key , value)=>{
        let poly = new Konva.Line({
        points: [23, 20, 23, 160, 70, 93, 150, 109, 290, 139, 270, 93],
        fill: '#00D2FF',
        stroke: 'black',
        strokeWidth: 5,
        closed: true,
      });
        layer.add(poly)
    })
    layer.draw();
}
let stage = new Konva.Stage({
  container: 'container',   // id of container <div>
  width: 600,
  height: 600
});
let layer1 = new Konva.Layer();
stage.add(layer1);
update(layer1);
