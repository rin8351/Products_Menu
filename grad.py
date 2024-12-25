import colorsys

def generate_gradient(n):
    start_hue = 0 / 360
    end_hue = 120 / 360
    
    colors = []
    for i in range(n):
        hue = start_hue + (end_hue - start_hue) * i / (n - 1)
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        rgb_int = tuple(int(x * 255) for x in rgb)
        colors.append(rgb_int)
    
    return colors

gradient_colors = generate_gradient(15)

# Вывод результатов в формате, удобном для копирования
print("RGB значения для градиента от красного до зеленого:")
print("[")
for color in gradient_colors:
    print(f"    {color},")
print("]")