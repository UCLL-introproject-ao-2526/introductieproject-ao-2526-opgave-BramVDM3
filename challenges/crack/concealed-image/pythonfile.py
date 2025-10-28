from PIL import Image

img = Image.open("whoami.png")
pixels = list(img.getdata())

bits = []
for pixel in pixels:
    # take one channel (R) LSB
    if isinstance(pixel, int):  # grayscale
        bits.append(pixel & 1)
    else:  # RGB or RGBA
        bits.append(pixel[0] & 1)

# convert bits to bytes
byte_list = [sum([bits[i*8 + j] << (7-j) for j in range(8)]) for i in range(len(bits)//8)]
hidden = ''.join([chr(b) for b in byte_list if 32 <= b <= 126])

print(hidden)
