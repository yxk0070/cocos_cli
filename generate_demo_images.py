import cv2
import numpy as np
import os

os.makedirs('demo/assets/textures', exist_ok=True)

# 1. 生成打砖块的完整设计图 (主图) 800x600
main_img = np.zeros((600, 800, 3), dtype=np.uint8)

# 绘制挡板 (Paddle) - 白色
# 坐标：中心点在 x=400, y=550。挡板宽=120, 高=20
cv2.rectangle(main_img, (340, 540), (460, 560), (255, 255, 255), -1)

# 绘制球 (Ball) - 红色
cv2.circle(main_img, (400, 530), 10, (0, 0, 255), -1)

# 绘制一些砖块 (Bricks) - 绿色
for i in range(5):
    for j in range(3):
        x1 = 100 + i * 130
        y1 = 100 + j * 40
        cv2.rectangle(main_img, (x1, y1), (x1 + 100, y1 + 25), (0, 255, 0), -1)

cv2.imwrite('demo/assets/textures/design_main.png', main_img)
print("Saved design_main.png")

# 2. 生成挡板切图 (模板图) 120x20
template_img = np.zeros((20, 120, 3), dtype=np.uint8)
cv2.rectangle(template_img, (0, 0), (120, 20), (255, 255, 255), -1)
cv2.imwrite('demo/assets/textures/paddle_template.png', template_img)
print("Saved paddle_template.png")
