declare namespace cc {
  class Node {
    parent: Node;
    x: number;
    y: number;
    position: Vec2;
    addComponent(type: any): any;
    getComponent(type: any): any;
    on(type: string, callback: (event: any) => void, target?: any): void;
    destroy(): void;
  }
  class Component {
    node: Node;
    enabled: boolean;
  }
  class Prefab {}
  function instantiate(prefab: Prefab): Node;
  class Graphics {
    fillColor: Color;
    strokeColor: Color;
    lineWidth: number;
    rect(x: number, y: number, w: number, h: number): void;
    fill(): void;
    stroke(): void;
    circle(x: number,w y: number, r: number): void;
    clear(): void;
  }
  class Label {
    string: string;
    fontSize: number;
  }
  class Color {
    constructor(r: number, g: number, b: number, a?: number);
    static WHITE: Color;
    static RED: Color;
    static CYAN: Color;
    static YELLOW: Color;
  }
  class Vec2 {
    x: number;
    y: number;
    magSqr(): number;
    normalize(): Vec2;
    sub(other: Vec2): Vec2;
    mag(): number;
  }
  function v2(x: number, y: number): Vec2;
  class Rect {
    intersects(rect: Rect): boolean;
  }
  function rect(x: number, y: number, w: number, h: number): Rect;

  namespace _decorator {
    function ccclass(target: any): void;
    function property(target: any, propertyKey?: string): void;
  }

  namespace Node {
    namespace EventType {
      const TOUCH_MOVE: string;
    }
  }

  namespace Event {
    class EventTouch {
      getDelta(): Vec2;
    }
  }

  namespace SystemEvent {
    namespace EventType {
      const KEY_DOWN: string;
      const KEY_UP: string;
    }
  }

  class SystemEvent {
    on(type: string, callback: (event: any) => void, target?: any): void;
  }

  const systemEvent: SystemEvent;

  namespace macro {
    namespace KEY {
      const w: number;
      const a: number;
      const s: number;
      const d: number;
    }
  }
}
