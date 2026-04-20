import cv2
import numpy as np

def find_image_position(main_image_path, template_image_path, threshold=0.8,
                        design_size=None, parent_anchor=(0.5, 0.5), node_anchor=(0.5, 0.5)):
    '''
    使用模板匹配在主图中查找子图位置。
    增加处理逻辑：
    - design_size: 设计分辨率 (width, height)，如果不传则默认和主图尺寸一致。
    - parent_anchor: 目标节点的父节点的锚点，默认 (0.5, 0.5) (即父节点坐标原点在中心)。
    - node_anchor: 目标节点自身的锚点，默认 (0.5, 0.5)。
    '''
    img = cv2.imread(main_image_path)
    if img is None:
        raise ValueError(f"Cannot read main image: {main_image_path}")
    main_h, main_w = img.shape[:2]
    
    if design_size:
        canvas_w, canvas_h = design_size
        scale_x = canvas_w / main_w
        scale_y = canvas_h / main_h
    else:
        canvas_w, canvas_h = main_w, main_h
        scale_x, scale_y = 1.0, 1.0

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    template = cv2.imread(template_image_path, 0)
    if template is None:
        raise ValueError(f"Cannot read template image: {template_image_path}")
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    matches = []
    for pt in zip(*loc[::-1]):
        img_left, img_top = pt[0], pt[1]
        
        # 将像素坐标和尺寸映射到逻辑设计分辨率
        log_left = img_left * scale_x
        log_top = img_top * scale_y
        log_w = w * scale_x
        log_h = h * scale_y
        
        # 计算目标节点在父节点局部坐标系下的左上角坐标 (Cocos 坐标系 Y 轴向上)
        tl_x = -canvas_w * parent_anchor[0] + log_left
        tl_y = canvas_h * (1.0 - parent_anchor[1]) - log_top
        
        # 加上目标节点自身锚点产生的偏移，得到最终应该写入 _position 的坐标
        cocos_x = tl_x + log_w * node_anchor[0]
        cocos_y = tl_y - log_h * (1.0 - node_anchor[1])

        matches.append({
            "x": cocos_x,       # Cocos 坐标
            "y": cocos_y,       # Cocos 坐标
            "cv_x": img_left + w // 2, # 原始 OpenCV 像素中心 X
            "cv_y": img_top + h // 2,  # 原始 OpenCV 像素中心 Y
            "w": log_w,
            "h": log_h,
            "score": float(res[pt[1]][pt[0]])
        })
    
    # 简单过滤重叠结果
    unique_matches = []
    for m in matches:
        is_unique = True
        for u in unique_matches:
            if abs(m["cv_x"] - u["cv_x"]) < w // 2 and abs(m["cv_y"] - u["cv_y"]) < h // 2:
                is_unique = False
                break
        if is_unique:
            unique_matches.append(m)
            
    return unique_matches
