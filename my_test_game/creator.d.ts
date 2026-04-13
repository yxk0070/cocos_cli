declare namespace cc {
  class Node {
    parent: Node;
    x: number;
    y: number;
    addComponent(type: any): any;
    on(type: string, callback: (event: any) => void, target?: any): void;
    destroy(): void;
  }
  class Component {
    node: Node;
  }
  class Graphics {
    fillColor: Color;
    strokeColor: Color;
    lineWidth: number;
    rect(x: number, y: number, w: number, h: number): void;
    fill(): void;
    stroke(): void;
    circle(x: number, y: number, r: number): void;
  }
  class Color {
    constructor(r: number, g: number, b: number, a?: number);
    static WHITE: Color;
    static RED: Color;
  }
  class Vec2 {
    x: number;
    y: number;
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
}
