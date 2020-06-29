const Id_2d_m = [[1,0,0],[0,1,0],[0,0,1]];

class Camera{
    constructor(){
        this.pos = [0,0];
        this.zoom = [100.0, 100.0];
        this.theta = 0;
        this.scale = 3.2;
        this.transFormationMatrix = this.generateTransformationMatrix();
    }

    /***
     * Update Translation Matrix, will effect the translation of each object
     * @param pos
     * @param zoom
     * @param scale
     * @param rotation
     */
    updateTranslation(pos=[0,0], zoom=[100,100], scale=3.2, rotation=0){
        this.pos = pos;
        this.zoom = zoom;
        this.scale = scale;
        this.theta = rotation;
        this.transFormationMatrix = this.generateTransformationMatrix();
    }

    /***
     * Pass in a reference object to translate its points towards the camera.
     * @param {polygon}
     */
    translate(obj){
        let T = this.transFormationMatrix;
        let new_shape = obj.shape.map((v)=>{
            let x = v[0];
            let y = v[1];

            let p = [x,y,1];
            //todo make this matrix multiplication clearer
            let Tp = [p[0]*T[0][0]+p[1]*T[0][1]+T[0][2],
                p[0]*T[1][0]+p[1]*T[1][1]+T[1][2]];
            return Tp;
         });
        obj.shape = new_shape;

    }

    /***
     * Get
     * @returns {number[][]}
     */
    generateTransformationMatrix() {
        let translation = Id_2d_m;
        translation[0] = [Math.cos(this.theta)*this.zoom[0]*this.scale, -Math.sin(this.theta)*this.zoom[1]*this.scale, this.pos[0]];
        translation[1] = [Math.sin(this.theta)*this.zoom[0]*this.scale, Math.cos(this.theta)*this.zoom[1]*this.scale, this.pos[1]];
        return translation;
    }
}