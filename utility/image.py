import csv
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

BG_RGB = (222, 189, 140)
FONT_PATH = "./asset/font.ttf"
FONT_SIZE = 20
HEADER_ROW = ["شام", "نهار", "صبحانه", "روز"]
CELL_HEIGHT = 50
PADDING = 10

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except IOError:
        print("Font not found. Using default font.")
        return ImageFont.load_default()

def generate_current_program_image(program) -> BytesIO:
    
    # [date, [[breakfast: [name, place, status]], [lunch: [...]], [dinner: []]]]
    
    data = [HEADER_ROW]
    
    for day_entry, day_meals in program:
        formatted_meals = [f"{meal[0]} . {meal[1]} . {meal[2]}" for meal in day_meals]
        row = [day_entry] + formatted_meals
        row.reverse()
        data.append(row)

    font = load_font(FONT_SIZE)

    cell_widths = []
    for col_index in range(len(data[0])):
        col_max_width = max([ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), row[col_index], font=font)[2] for row in data])
        cell_widths.append(col_max_width + 2 * PADDING)
        
    total_width = sum(cell_widths)
    total_height = len(data) * CELL_HEIGHT

    img = Image.new('RGB', (total_width, total_height), color=BG_RGB)
    draw = ImageDraw.Draw(img)

    y = 0
    for row_index, row in enumerate(data):
        x = 0
        for col_index, cell in enumerate(row):
            text_bbox = draw.textbbox((0, 0), cell, font=font)
            text_width = text_bbox[2]
            text_height = text_bbox[3]

            text_x = x + (cell_widths[col_index] - text_width) // 2
            text_y = y + (CELL_HEIGHT - text_height) // 2

            draw.text((text_x, text_y), cell, font=font, fill="black")

            draw.rectangle([x, y, x + cell_widths[col_index], y + CELL_HEIGHT], outline="black")
            x += cell_widths[col_index]
        y += CELL_HEIGHT

    byte_stream = BytesIO()
    img.save(byte_stream, format='PNG')
    byte_stream.seek(0)

    return byte_stream
