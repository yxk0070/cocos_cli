const { ccclass, property } = cc._decorator;

@ccclass
export default class Brick extends cc.Component {
  onLoad() {
    // Automatically draw the brick graphics if it's not a Sprite
    let ctx = this.node.getComponent(cc.Graphics);
    if (!ctx) {
      ctx = this.node.addComponent(cc.Graphics);
    }

    if (ctx.clear) ctx.clear();
    ctx.fillColor = new cc.Color(50, 200, 100, 255);
    ctx.rect(-70, -20, 140, 40);
    ctx.fill();

    // Add white border to brick
    ctx.strokeColor = cc.Color.WHITE;
    ctx.lineWidth = 2;
    ctx.rect(-70, -20, 140, 40);
    ctx.stroke();
  }
}
