actors = {};
//will be called via ajax
function updateData(data){
    // Json actor object
    //    "name": self.name,
    //    "position": self.pos,
    //    "shape": self.shape
    actors = data["payload"]

}