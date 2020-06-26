let actors = new Map();

//will be called via ajax
function updateData(data){
    // Json actor object
    //    "name": self.name,
    //    "position": self.pos,
    //    "shape": self.shape
    let actor = data["payload"];

    // create object actor from json respons, if it already existed update
    if (!actors.has(actor["name"])){
        actors.set(actor["name"], new Actor(actor["positions"], actor["shape"]));
    }else{
         let a = actors.get(actor["name"]);
         a.pos = actor["positions"];
         a.shape = actor["shape"];
         a.name = actor["name"];
         actors.replace(actor["name"],a); //if this is even necessary
    }
    //update()
    return data
}
function update(ctx) {
    actors.forEach((key , value)=>{
        ctx.write
    })
}
