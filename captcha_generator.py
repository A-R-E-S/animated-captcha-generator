from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import numpy as np
from scipy.special import comb
import os
import math

# =============================================
# ПАРАМЕТРЫ ДЛЯ НАСТРОЙКИ
# =============================================
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 75
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
MAX_ROTATION_ANGLE = 60
NUM_POINTS = 950
NUM_CONTROL_POINTS = 8
CURVE_WIDTH = 2
FONT_SIZE = 40

FONT_PATHS = {
    'Papyrus': '1papyrus.ttf',
    'Book Antiqua': 'book_antiqua.ttf',
    'Bookman Old Style': 'bookmanoldstyle.ttf',
    'Captcha Code': 'captchacode.otf',
    'Courier New': 'couriernew.ttf',
    'Courier New Bold': 'couriernewbold.ttf',
    'Courier New Bold Italic': 'couriernewbolditalic.ttf',
    'Courier New Italic': 'couriernewitalic.ttf',
    'LED Dot Matrix': 'LEDDotMatrix.ttf',
    'Lucida Handwriting': 'lucidahandwriting_italic.ttf',
    'Mistral': 'mistral.ttf',
    'Tahoma': 'tahoma.ttf',
    'Tahoma Bold': 'tahoma_bold.ttf',
}

# Параметры синусоидальной траектории текста
SINE_AMPLITUDE = 10
SINE_FREQUENCY = 1
SINE_PHASE = 0
RANDOM_AMPLITUDE = 3
RANDOM_FREQUENCY = 0.03
RANDOM_PHASE_CHANGE = 2.0
CENTER_BIAS = 0.5
MIN_ANGLE_STEP = np.pi / 1
MAX_ANGLE_STEP = np.pi / 360
RADIUS_VARIATION = 2000
MAX_SPIRAL_POINTS = 100
CHAR_SPACING = 0
BLUR_RADIUS = 0.73

# =============================================
# ПАРАМЕТРЫ GIF-АНИМАЦИИ
# =============================================
GIF_FRAMES = 24            # количество кадров
GIF_FRAME_DURATION = 70    # длительность кадра (мс)
BOUNCE_AMPLITUDE = 6       # амплитуда подпрыгивания цифр
BLUR_RECT_WIDTH = 220      # ширина блюр-полосы
BLUR_RECT_RADIUS = 4       # сила размытия внутри полосы
BLUR_RECT_FEATHER = 12     # мягкость краёв полосы
BLUR_RECT_DIRECTION = 1   # -1 = едет влево, 1 = едет вправо

output_folder = "captchas"
os.makedirs(output_folder, exist_ok=True)

# =============================================
# ПРОВЕРКА ШРИФТОВ ПРИ ЗАПУСКЕ
# =============================================
def load_available_fonts():
    available = {}
    for name, path in FONT_PATHS.items():
        if not os.path.exists(path):
            print(f"Внимание: файл шрифта не найден, пропускаем: {path}")
            continue
        try:
            ImageFont.truetype(path, FONT_SIZE)
            available[name] = path
        except OSError:
            print(f"Внимание: шрифт не читается, пропускаем: {path}")
    if not available:
        raise FileNotFoundError("Не найдено ни одного рабочего шрифта в папке со скриптом!")
    return available

AVAILABLE_FONTS = load_available_fonts()

# =============================================
# ГЕНЕРАЦИЯ КРИВОЙ
# =============================================
def bezier_curve(points, n=NUM_POINTS):
    n_points = len(points)
    t = np.linspace(0, 1, n).reshape(-1, 1)
    bern = np.array([comb(n_points - 1, i) * (t ** i) * (1 - t) ** (n_points - 1 - i)
                     for i in range(n_points)])
    curve = np.sum(bern.T.reshape(n, n_points, 1) * points, axis=1)
    return curve

def generate_control_points():
    points = []
    center = (IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2)
    points.append((
        random.gauss(center[0], IMAGE_WIDTH * (1 - CENTER_BIAS) / 4),
        random.gauss(center[1], IMAGE_HEIGHT * (1 - CENTER_BIAS) / 4)
    ))
    angle = random.uniform(0, 2 * np.pi)
    spiral_points = random.randint(1, MAX_SPIRAL_POINTS)
    for i in range(1, NUM_CONTROL_POINTS):
        if i <= spiral_points:
            angle += random.uniform(MIN_ANGLE_STEP, MAX_ANGLE_STEP)
            radius = min(IMAGE_WIDTH, IMAGE_HEIGHT) * RADIUS_VARIATION * random.uniform(0.2, 1)
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
        else:
            x = random.gauss(center[0], IMAGE_WIDTH * (1 - CENTER_BIAS) / 3)
            y = random.gauss(center[1], IMAGE_HEIGHT * (1 - CENTER_BIAS) / 3)
        x = max(0, min(IMAGE_WIDTH - 1, x))
        y = max(0, min(IMAGE_HEIGHT - 1, y))
        points.append((x, y))
    return np.array(points)

# =============================================
# ПОДГОТОВКА ЭЛЕМЕНТОВ КАПЧИ
# =============================================
def prepare_captcha_elements():
    digits = ''.join(random.choices('0123456789', k=7))

    font_name, font_path = random.choice(list(AVAILABLE_FONTS.items()))
    font = ImageFont.truetype(font_path, FONT_SIZE)

    amp = SINE_AMPLITUDE + random.uniform(-RANDOM_AMPLITUDE, RANDOM_AMPLITUDE)
    freq = SINE_FREQUENCY + random.uniform(-RANDOM_FREQUENCY, RANDOM_FREQUENCY)
    phase = SINE_PHASE + random.uniform(0, RANDOM_PHASE_CHANGE)

    dummy = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(dummy)
    full_bbox = draw.textbbox((0, 0), digits, font=font)
    text_width = full_bbox[2] - full_bbox[0]
    text_height = full_bbox[3] - full_bbox[1]
    start_x = (IMAGE_WIDTH - text_width - CHAR_SPACING * (len(digits) - 1)) // 2
    start_y = (IMAGE_HEIGHT - text_height) // 2

    chars = []
    current_x = start_x
    for digit in digits:
        char_bbox = font.getbbox(digit)
        char_width = char_bbox[2] - char_bbox[0]
        y_offset = amp * math.sin(2 * math.pi * freq * current_x + phase)
        chars.append({
            'digit': digit,
            'x': current_x,
            'base_y': start_y + int(y_offset),
            'before': random.choice([True, False]),
            'angle': random.uniform(-MAX_ROTATION_ANGLE, MAX_ROTATION_ANGLE),
            'bounce_phase': random.uniform(0, 2 * math.pi),
            'bounce_cycles': random.randint(1, 2),
        })
        current_x += char_width + CHAR_SPACING

    curve = bezier_curve(generate_control_points())
    return {'digits': digits, 'font': font, 'chars': chars, 'curve': curve}

# =============================================
# ОТРИСОВКА ОДНОГО КАДРА
# =============================================
def draw_digit(image, font, digit, x, y, angle):
    bbox = font.getbbox(digit)
    left, top, right, bottom = bbox
    w = right - left
    h = bottom - top
    temp_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((-left, -top), digit, fill=TEXT_COLOR, font=font)
    rotated_img = temp_img.rotate(angle, expand=True, resample=Image.BICUBIC)
    char_center_x = x + left + w / 2
    char_center_y = y + top + h / 2
    rw, rh = rotated_img.size
    paste_x = int(char_center_x - rw / 2)
    paste_y = int(char_center_y - rh / 2)
    image.paste(rotated_img, (paste_x, paste_y), rotated_img)

def render_frame(elements, bounce_offsets):
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    chars = elements['chars']
    font = elements['font']

    for i, ch in enumerate(chars):
        if ch['before']:
            draw_digit(image, font, ch['digit'], ch['x'], ch['base_y'] + bounce_offsets[i], ch['angle'])

    curve = elements['curve']
    for i in range(1, len(curve)):
        p1 = tuple(curve[i - 1].astype(int))
        p2 = tuple(curve[i].astype(int))
        draw.line([p1, p2], fill=LINE_COLOR, width=CURVE_WIDTH)

    for i, ch in enumerate(chars):
        if not ch['before']:
            draw_digit(image, font, ch['digit'], ch['x'], ch['base_y'] + bounce_offsets[i], ch['angle'])

    image = image.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
    return image

# =============================================
# БЛЮР-ПОЛОСА С БЕСШОВНЫМ ЗАВОРАЧИВАНИЕМ
# =============================================
def make_feather_mask(width, height, feather):
    mask = Image.new('L', (width, height), 255)
    px = mask.load()
    for x in range(width):
        if x < feather:
            v = int(255 * x / feather)
        elif x >= width - feather:
            v = int(255 * (width - 1 - x) / feather)
        else:
            v = 255
        for y in range(height):
            px[x, y] = v
    return mask

BLUR_RECT_MASK = make_feather_mask(BLUR_RECT_WIDTH, IMAGE_HEIGHT, BLUR_RECT_FEATHER)

def apply_blur_rect(image, x):
    blurred = image.filter(ImageFilter.GaussianBlur(radius=BLUR_RECT_RADIUS))
    mask = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), 0)
    x = int(round(x)) % IMAGE_WIDTH

    if x + BLUR_RECT_WIDTH <= IMAGE_WIDTH:
        # полоса целиком на экране
        mask.paste(BLUR_RECT_MASK, (x, 0))
    else:
        # полоса завернулась: правая часть у края экрана...
        first_w = IMAGE_WIDTH - x
        mask.paste(BLUR_RECT_MASK.crop((0, 0, first_w, IMAGE_HEIGHT)), (x, 0))
        # ...а продолжение въезжает с противоположного края
        second_w = BLUR_RECT_WIDTH - first_w
        mask.paste(BLUR_RECT_MASK.crop((first_w, 0, BLUR_RECT_WIDTH, IMAGE_HEIGHT)), (0, 0))

    image.paste(blurred, (0, 0), mask)
    return image

# =============================================
# ГЕНЕРАЦИЯ PNG И GIF
# =============================================
def generate_png():
    elements = prepare_captcha_elements()
    zeros = [0] * len(elements['chars'])
    image = render_frame(elements, zeros)
    return image, elements['digits']

def generate_gif():
    elements = prepare_captcha_elements()
    chars = elements['chars']
    frames = []
    for f in range(GIF_FRAMES):
        t = f / GIF_FRAMES
        bounce_offsets = [
            int(round(BOUNCE_AMPLITUDE * math.sin(2 * math.pi * ch['bounce_cycles'] * t + ch['bounce_phase'])))
            for ch in chars
        ]
        frame = render_frame(elements, bounce_offsets)
        # полоса за цикл проезжает ровно IMAGE_WIDTH пикселей -> шов не виден
        x = (BLUR_RECT_DIRECTION * IMAGE_WIDTH * t) % IMAGE_WIDTH
        frame = apply_blur_rect(frame, x)
        frames.append(frame)
    return frames, elements['digits']

# =============================================
# ЗАПУСК
# =============================================
if __name__ == "__main__":
    fmt = input("Формат капчи (png / gif): ").strip().lower()
    while fmt not in ("png", "gif"):
        fmt = input("Неверный формат. Введите 'png' или 'gif': ").strip().lower()

    num_captchas = int(input("Сколько каптч сгенерировать: "))

    for i in range(num_captchas):
        if fmt == "png":
            img, digits = generate_png()
            filename = f"{digits}.png"
            img.save(os.path.join(output_folder, filename))
        else:
            frames, digits = generate_gif()
            filename = f"{digits}.gif"
            frames[0].save(
                os.path.join(output_folder, filename),
                save_all=True,
                append_images=frames[1:],
                duration=GIF_FRAME_DURATION,
                loop=0,
            )
        print(f"Сохранено: {filename}")