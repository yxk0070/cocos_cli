const { ccclass, property } = cc._decorator;

@ccclass
export default class GameManager extends cc.Component {
    player: cc.Node = null;
    enemies: cc.Node[] = [];
    bullets: any[] = [];
    spawnTimer: number = 0;
    shootTimer: number = 0;
    score: number = 0;
    scoreLabel: cc.Label = null;

    moveDir: cc.Vec2 = cc.v2(0, 0);

    onLoad() {
        let canvas = this.node;

        // Background
        let bg = new cc.Node('Bg');
        bg.parent = canvas;
        let bgCtx = bg.addComponent(cc.Graphics);
        bgCtx.fillColor = new cc.Color(30, 40, 30, 255);
        bgCtx.rect(-1000, -1000, 2000, 2000);
        bgCtx.fill();

        // Score Label
        let scoreNode = new cc.Node('Score');
        scoreNode.parent = canvas;
        scoreNode.y = 280;
        this.scoreLabel = scoreNode.addComponent(cc.Label);
        this.scoreLabel.string = "Score: 0";
        this.scoreLabel.fontSize = 30;

        // Player
        this.player = new cc.Node('Player');
        this.player.parent = canvas;
        let pCtx = this.player.addComponent(cc.Graphics);
        pCtx.fillColor = cc.Color.CYAN;
        pCtx.circle(0, 0, 20);
        pCtx.fill();

        // Input listeners
        cc.systemEvent.on(cc.SystemEvent.EventType.KEY_DOWN, this.onKeyDown, this);
        cc.systemEvent.on(cc.SystemEvent.EventType.KEY_UP, this.onKeyUp, this);
    }

    onKeyDown(event) {
        switch (event.keyCode) {
            case cc.macro.KEY.w: this.moveDir.y = 1; break;
            case cc.macro.KEY.s: this.moveDir.y = -1; break;
            case cc.macro.KEY.a: this.moveDir.x = -1; break;
            case cc.macro.KEY.d: this.moveDir.x = 1; break;
        }
    }

    onKeyUp(event) {
        switch (event.keyCode) {
            case cc.macro.KEY.w: if (this.moveDir.y === 1) this.moveDir.y = 0; break;
            case cc.macro.KEY.s: if (this.moveDir.y === -1) this.moveDir.y = 0; break;
            case cc.macro.KEY.a: if (this.moveDir.x === -1) this.moveDir.x = 0; break;
            case cc.macro.KEY.d: if (this.moveDir.x === 1) this.moveDir.x = 0; break;
        }
    }

    update(dt: number) {
        // Move Player
        if (this.moveDir.magSqr() > 0) {
            let dir = this.moveDir.normalize();
            this.player.x += dir.x * 200 * dt;
            this.player.y += dir.y * 200 * dt;
        }

        // Spawn Enemies
        this.spawnTimer += dt;
        if (this.spawnTimer > 1.0) {
            this.spawnTimer = 0;
            this.spawnEnemy();
        }

        // Move Enemies towards player
        for (let e of this.enemies) {
            let dir = this.player.position.sub(e.position).normalize();
            e.x += dir.x * 100 * dt;
            e.y += dir.y * 100 * dt;
        }

        // Auto Shoot
        this.shootTimer += dt;
        if (this.shootTimer > 0.5 && this.enemies.length > 0) {
            this.shootTimer = 0;
            this.shoot();
        }

        // Move Bullets & Check Collisions
        for (let i = this.bullets.length - 1; i >= 0; i--) {
            let b = this.bullets[i];
            b.node.x += b.dir.x * 600 * dt;
            b.node.y += b.dir.y * 600 * dt;

            let hit = false;
            for (let j = this.enemies.length - 1; j >= 0; j--) {
                let e = this.enemies[j];
                if (b.node.position.sub(e.position).mag() < 30) {
                    e.destroy();
                    this.enemies.splice(j, 1);
                    hit = true;
                    this.score += 10;
                    this.scoreLabel.string = "Score: " + this.score;
                    break;
                }
            }
            
            if (hit || b.node.position.sub(this.player.position).mag() > 800) {
                b.node.destroy();
                this.bullets.splice(i, 1);
            }
        }
        
        // Check Player Death
        for (let e of this.enemies) {
            if (this.player.position.sub(e.position).mag() < 30) {
                this.scoreLabel.string = "Game Over! Score: " + this.score;
                this.enabled = false; // stop game
            }
        }
    }

    spawnEnemy() {
        let enemy = new cc.Node('Enemy');
        enemy.parent = this.node;
        let angle = Math.random() * Math.PI * 2;
        let radius = 600;
        enemy.x = this.player.x + Math.cos(angle) * radius;
        enemy.y = this.player.y + Math.sin(angle) * radius;

        let ctx = enemy.addComponent(cc.Graphics);
        ctx.fillColor = cc.Color.RED;
        ctx.rect(-15, -15, 30, 30);
        ctx.fill();

        this.enemies.push(enemy);
    }

    shoot() {
        let closest = null;
        let minDist = 999999;
        for (let e of this.enemies) {
            let d = this.player.position.sub(e.position).mag();
            if (d < minDist) { minDist = d; closest = e; }
        }

        if (closest) {
            let bulletNode = new cc.Node('Bullet');
            bulletNode.parent = this.node;
            bulletNode.position = this.player.position;
            let ctx = bulletNode.addComponent(cc.Graphics);
            ctx.fillColor = cc.Color.YELLOW;
            ctx.circle(0, 0, 8);
            ctx.fill();

            let dir = closest.position.sub(this.player.position).normalize();
            this.bullets.push({ node: bulletNode, dir: dir });
        }
    }
}