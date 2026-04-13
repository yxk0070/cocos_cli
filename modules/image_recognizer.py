import cv2
import numpy as np

def find_image_position(main_image_path, template_image_path, threshold=0.8):
    '''
    使用模板匹配在主图中查找子图位置。
    返回匹配的中心坐标 (x, y) 和宽高 (w, h)
    '''
    img = cv2.imread(main_image_path)
    if img is None:
        raise ValueError(f"Cannot read main image: {main_image_path}")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    template = cv2.imread(template_image_path, 0)
    if template is None:
        raise ValueError(f"Cannot read template image: {template_image_path}")
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    matches = []
    for pt in zip(*loc[::-1]):
        center_x = int(pt[0] + w // 2)
        center_y = int(pt[1] + h // 2)
        matches.append({
            "x": center_x,
            "y": center_y,
            "w": w,
            "h": h,
            "score": float(res[pt[1]][pt[0]])
        })
    
    # 简单过滤重叠结果
    unique_matches = []
    for m in matches:
        is_unique = True
        for u in unique_matches:
            if abs(m["x"] - u["x"]) < w // 2 and abs(m["y"] - u["y"]) < h // 2:
                is_unique = False
                break
        if is_unique:
            unique_matches.append(m)
            
    return unique_matches
