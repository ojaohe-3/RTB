class Activity{
    constructor(pos, name, status){
        this.pos = pos;
        this.name = name;
        this.status = status === "complete" ? false: true;
        this.radius = 8.5;
    }
}