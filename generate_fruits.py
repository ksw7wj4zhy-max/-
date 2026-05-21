#!/usr/bin/env python3
"""
生成合成大西瓜游戏的水果图片素材（纯净圆形背景版）
输出：assets/fruit_00.png ~ assets/fruit_10.png
"""
from PIL import Image, ImageDraw
import os

# 水果配置
FRUITS = [
    {'emoji': '🍒', 'r': 15, 'bg': (255, 0, 64),    'name': 'fruit_00'},
    {'emoji': '🍓', 'r': 21, 'bg': (255, 51, 102),  'name': 'fruit_01'},
    {'emoji': '🍇', 'r': 27, 'bg': (139, 92, 246),  'name': 'fruit_02'},
    {'emoji': '🍊', 'r': 33, 'bg': (255, 149, 0),   'name': 'fruit_03'},
    {'emoji': '🍋', 'r': 39, 'bg': (255, 214, 10),  'name': 'fruit_04'},
    {'emoji': '🍎', 'r': 45, 'bg': (34, 197, 94),   'name': 'fruit_05'},
    {'emoji': '🍐', 'r': 51, 'bg': (251, 191, 36),  'name': 'fruit_06'},
    {'emoji': '🍑', 'r': 57, 'bg': (255, 107, 138), 'name': 'fruit_07'},
    {'emoji': '🍍', 'r': 64, 'bg': (245, 158, 11),  'name': 'fruit_08'},
    {'emoji': '🥥', 'r': 72, 'bg': (161, 98, 7),    'name': 'fruit_09'},
    {'emoji': '🍉', 'r': 82, 'bg': (21, 128, 61),   'name': 'fruit_10'},
]

IMG_SIZE = 512
OUTPUT_DIR = '/Users/black/WorkBuddy/20260507222124/assets'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def lighten(rgb, amount=80):
    return tuple(min(255, c + amount) for c in rgb)

def darken(rgb, amount=50):
    return tuple(max(0, c - amount) for c in rgb)

def make_circle_image(radius_px, bg_color):
    """生成单个圆形水果背景图（无emoji）"""
    size = IMG_SIZE
    cx, cy = size // 2, size // 2
    # 缩放到512尺寸
    r = int(radius_px * (IMG_SIZE / 200.0))

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    main_col = bg_color
    hi_col   = lighten(bg_color, 90)
    shadow   = darken(bg_color, 60)

    # 柔和外阴影
    for i in range(6, 0, -1):
        alpha = max(0, 15 - i * 2)
        draw.ellipse([cx-r-i*3, cy-r-i*3, cx+r+i*3, cy+r+i*3],
                     fill=(*darken(bg_color, 80), alpha))

    # 径向渐变：从外向内多层圆（越靠边越暗，越靠中心越亮）
    steps = 30
    for step in range(steps, 0, -1):
        t = step / steps  # 0=中心(亮), 1=边缘(暗)
        rr = int(r * t)
        if rr < 1: continue
        # 颜色插值：边缘用main_col，中心用hi_col
        rr_c = int(main_col[0]*t + hi_col[0]*(1-t))
        gg_c = int(main_col[1]*t + hi_col[1]*(1-t))
        bb_c = int(main_col[2]*t + hi_col[2]*(1-t))
        draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr],
                     fill=(rr_c, gg_c, bb_c, 255))

    # 深色轮廓线
    draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                 outline=(*darken(bg_color, 70), 180), width=2)

    # 主高光（左上椭圆）
    hx = cx - int(r * 0.3)
    hy = cy - int(r * 0.3)
    hr = int(r * 0.38)
    for i in range(hr, 0, -1):
        a = int(110 * ((hr - i) / hr) ** 1.5)
        draw.ellipse([hx-i, hy-i, hx+i, hy+i],
                     fill=(255, 255, 255, a))

    # 次高光（右下小白点）
    hx2 = cx + int(r * 0.22)
    hy2 = cy + int(r * 0.22)
    hr2 = int(r * 0.14)
    for i in range(hr2, 0, -1):
        a = int(55 * ((hr2 - i) / hr2) ** 1.5)
        draw.ellipse([hx2-i, hy2-i, hx2+i, hy2+i],
                     fill=(255, 255, 255, a))

    return img

# 生成所有图片
for fruit in FRUITS:
    img = make_circle_image(fruit['r'], fruit['bg'])
    path = os.path.join(OUTPUT_DIR, f"{fruit['name']}.png")
    img.save(path, 'PNG')
    used = sum(1 for x in range(512) for y in range(512)
               if img.getpixel((x, y))[3] > 0)
    print(f'Saved: {path}  (r={fruit["r"]}, coverage={used}px)')

print(f'\n✅ 生成了 {len(FRUITS)} 张水果圆形背景图！')
print('   → 游戏中会优先加载这些PNG图片')
print('   → 如需自定义水果，替换对应PNG文件即可')
