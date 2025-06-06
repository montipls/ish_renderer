from PIL import Image


img = Image.open('circle.jpeg').convert('RGB')
img = img.resize((68, 68))

width, height = img.size

output_lines = []

for y in range(0, height, 2):
    line_chars = []
    for x in range(width):
        bg = img.getpixel((x, y)) # top pixel
        fg = img.getpixel((x, y + 1)) # bottom pixel

        char = f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m\033[48;2;{bg[0]};{bg[1]};{bg[2]}m▄\033[0m"
        line_chars.append(char)
    output_lines.append(''.join(line_chars))

output_string = '\n'.join(output_lines)

print('\n'*4)
print(output_string)
