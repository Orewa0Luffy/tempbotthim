from PIL import Image, ImageDraw, ImageFont
import os

def generate_thumbnail(template_name, title, synopsis, user_image_path):
    template_path = f"templates/{template_name}.jpg"
    output_path = f"generated/{title.replace(' ', '_')}.jpg"

    base = Image.open(template_path).convert("RGBA")
    user_img = Image.open(user_image_path).convert("RGBA").resize((500, 280))
    base.paste(user_img, (50, 100))

    draw = ImageDraw.Draw(base)

    # Load default fonts for safety
    try:
        font_title = ImageFont.truetype("arial.ttf", 50)
        font_info = ImageFont.truetype("arial.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_info = ImageFont.load_default()

    draw.text((50, 30), title, font=font_title, fill="white")
    draw.text((50, 400), synopsis, font=font_info, fill="white")
    draw.text((base.width - 300, base.height - 50), "@Animes_Union", font=font_info, fill="white")

    os.makedirs("generated", exist_ok=True)
    base.save(output_path)
    return output_path
