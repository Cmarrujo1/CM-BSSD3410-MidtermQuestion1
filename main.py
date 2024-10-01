from PIL import Image

def remove_chroma_key(fg_img_path, bg_img_path, output_img_path):
    fg_img = Image.open(fg_img_path).convert("RGBA")
    bg_img = Image.open(bg_img_path).convert("RGBA")

    fg_width, fg_height = fg_img.size
    bg_img = bg_img.resize((fg_width, fg_height))

    chroma_key = fg_img.getpixel((0, 0))

    def is_chroma(pixel, chroma_key, tolerance=100):
        return all(abs(p - c) < tolerance for p, c in zip(pixel[:3], chroma_key[:3]))

    composite_img = Image.new("RGBA", (fg_width, fg_height))

    for x in range(fg_width):
        for y in range(fg_height):
            fg_pixel = fg_img.getpixel((x, y))
            if is_chroma(fg_pixel, chroma_key):
                composite_img.putpixel((x, y), bg_img.getpixel((x, y)))
            else:
                composite_img.putpixel((x, y), fg_pixel)

    composite_img.save(output_img_path)

def main():
    remove_chroma_key("jack.jpg", "guard.jpg", "composite_output.png")

if __name__ == "__main__":
    main()
