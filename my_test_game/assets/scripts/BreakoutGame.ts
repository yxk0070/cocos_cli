const { ccclass, property } = cc._decorator;

@ccclass
export default class BreakoutGame extends cc.Component {
  @property(cc.Prefab)
  brickPrefab: cc.Prefab = null;

  paddle: cc.Node = null;
  ball: cc.Node = null;
  bricks: cc.Node[] = [];

  ballVelocity: cc.Vec2 = cc.v2(300, 300);

  onLoad() {
    let canvas = this.node; // Attach this script to Canvas

    // Create dark background
    let bg = new cc.Node("Bg");
    bg.parent = canvas;
    let bgCtx = bg.addComponent(cc.Graphics);
    bgCtx.fillColor = new cc.Color(30, 30, 30, 255);
    bgCtx.rect(-480, -320, 960, 640);
    bgCtx.fill();

    // Create Paddle
    this.paddle = new cc.Node("Paddle");
    this.paddle.parent = canvas;
    this.paddle.y = -250;
    let pCtx = this.paddle.addComponent(cc.Graphics);
    pCtx.fillColor = cc.Color.WHITE;
    pCtx.rect(-60, -10, 120, 20);
    pCtx.fill();

    // Paddle Movement via Touch/Mouse
    canvas.on(cc.Node.EventType.TOUCH_MOVE, (event: cc.Event.EventTouch) => {
      let delta = event.getDelta();
      this.paddle.x += delta.x;
      if (this.paddle.x < -420) this.paddle.x = -420;
      if (this.paddle.x > 420) this.paddle.x = 420;
    });

    // Create Ball
    this.ball = new cc.Node("Ball");
    this.ball.parent = canvas;
    this.ball.y = -200;
    let bCtx = this.ball.addComponent(cc.Graphics);
    bCtx.fillColor = cc.Color.RED;
    bCtx.circle(0, 0, 12);
    bCtx.fill();

    // Create Bricks (6 columns x 4 rows)
    if (this.brickPrefab) {
      for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 4; j++) {
          let brick = cc.instantiate(this.brickPrefab);
          brick.parent = canvas;
          brick.x = -375 + i * 150;
          brick.y = 100 + j * 50;

          this.bricks.push(brick);
        }
      }
    } else {
      console.warn("Brick Prefab is not assigned!");
    }
  }

  update(dt: number) {
    if (!this.ball) return;

    // Update ball position
    this.ball.x += this.ballVelocity.x * dt;
    this.ball.y += this.ballVelocity.y * dt;

    // Wall collision (assuming 960x640 canvas, origin at center)
    if (this.ball.x <= -468 || this.ball.x >= 468) {
      this.ballVelocity.x *= -1;
      this.ball.x = this.ball.x <= -468 ? -468 : 468;
    }
    if (this.ball.y >= 308) {
      this.ballVelocity.y *= -1;
      this.ball.y = 308;
    }
    // Bottom bounds - reset game
    if (this.ball.y <= -320) {
      this.ball.x = 0;
      this.ball.y = -200;
      this.ballVelocity.y = Math.abs(this.ballVelocity.y);
      this.ballVelocity.x = 300;
    }

    // Simple AABB Collision
    let ballRect = cc.rect(this.ball.x - 12, this.ball.y - 12, 24, 24);

    // Paddle collision
    let paddleRect = cc.rect(this.paddle.x - 60, this.paddle.y - 10, 120, 20);
    if (ballRect.intersects(paddleRect) && this.ballVelocity.y < 0) {
      this.ballVelocity.y = Math.abs(this.ballVelocity.y);
      // Add slight x-axis influence based on hit position
      let hitOffset = this.ball.x - this.paddle.x;
      this.ballVelocity.x = hitOffset * 5;
    }

    // Brick collision
    for (let i = this.bricks.length - 1; i >= 0; i--) {
      let brick = this.bricks[i];
      let bRect = cc.rect(brick.x - 70, brick.y - 20, 140, 40);
      if (ballRect.intersects(bRect)) {
        this.ballVelocity.y *= -1;
        brick.destroy();
        this.bricks.splice(i, 1);
        break; // Break loop to avoid multiple bounces in one frame
      }
    }

    // Win condition
    if (this.bricks.length === 0) {
      this.ballVelocity = cc.v2(0, 0);
      console.log("You Win!");
    }
  }
}
