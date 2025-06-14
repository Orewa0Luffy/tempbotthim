from PIL import Image, ImageDraw, ImageFont
import os

def generate_thumbnail(template_name, title, synopsis, user_image_path):
    template_path = f"templates/{template_name}.jpg"
    output_path = f"generated/{title.replace(' ', '_')}.jpg"

    # Load template
    base = Image.open(template_path).convert("RGBA")

    # Load user image and resize
    user_img = Image.open(user_image_path).convert("RGBA").resize((500, 280))
    base.paste(user_img, (50, 100))

    # Draw title and synopsis
    draw = ImageDraw.Draw(base)

    # Load fonts (adjust path and size)
    font_title = ImageFont.truetype("arial.ttf", 50)
    font_info = ImageFont.truetype("arial.ttf", 30)

    # Draw text
    draw.text((50, 30), title, font=font_title, fill="white")
    draw.text((50, 400), synopsis, font=font_info, fill="white")

    # Replace watermark
    draw.text((base.width - 300, base.height - 50), "@Animes_Union", font=font_info, fill="white")

    # Save output
    os.makedirs("generated", exist_ok=True)
    base.save(output_path)
    return output_path
