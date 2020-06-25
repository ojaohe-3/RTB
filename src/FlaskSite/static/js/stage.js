let actors = new Map();

//will be called via ajax
function updateData(data){
    // Json actor object
    //    "name": self.name,
    //    "position": self.pos,
    //    "shape": self.shape
    var actor = data["payload"]
    if (!actors.has(actor["name"])){
        actors.set(actor["name"], new Actor(actor["positions"], actor["shape"]))

    }

}