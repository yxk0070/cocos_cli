const {ccclass, property} = cc._decorator;

@ccclass
export default class PaddleController extends cc.Component {
    @property
    speed: number = 500;

    start () {
        console.log("Paddle script initialized!");
    }

    update (dt) {
        // Move paddle logic
    }
}
