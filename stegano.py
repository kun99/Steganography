import numpy as np
from PIL import Image

def encode():
    cover_image = Image.open("images/bird.jpg")
    image_to_hide = Image.open("images/cat.jpg")
    
    image_bytes = np.array(cover_image)
    hidden_image_bytes = np.array(image_to_hide)
    new_image = np.empty_like(np.asarray(cover_image))
    
    h = hidden_image_bytes.shape[0]
    w = hidden_image_bytes.shape[1]
    rgb = hidden_image_bytes.shape[2]

    if(len(image_bytes) > len(hidden_image_bytes)):
        for i, nested_array in enumerate(image_bytes):
            for j, array_bytes in enumerate(nested_array):
                for k, byte in enumerate(array_bytes):
                    cover = np.unpackbits(byte)
                    # replacing two lsbs from byte from cover image
                    # with two msbs from byte from image to hide
                    if i < h and j < w and k < rgb:
                        to_hide = np.unpackbits(hidden_image_bytes[i][j][k])
                        cover[6] = to_hide[0]
                        cover[7] = to_hide[1]
                        changed_byte = np.packbits(cover)
                        new_image[i][j][k] = changed_byte[0]
                    # replacing two lsbs from byte from cover image
                    # with 0 so when unpacked it is a black pixel
                    else:
                        cover[6] = 0
                        cover[7] = 0
                        new_image[i][j][k] = np.packbits(cover)
        save_image = Image.fromarray(new_image)
        save_image.save("images/got_steganoed.png")
    else:
        print("cover image too small")

def decode():
    decode_image = Image.open("images/got_steganoed.png")
    decode_bytes = np.array(decode_image)
    
    new_image = np.empty_like(np.asarray(decode_bytes))
    
    for i, nested_array in enumerate(decode_bytes):
        for j, array_bytes in enumerate(nested_array):
            for k, byte in enumerate(array_bytes):
                binary = np.unpackbits(byte)
                new_image[i][j][k] = str(binary[6]) + str(binary[7])
    PILimage = Image.fromarray(new_image)
    PILimage.save("decoded.png")

encode()
decode()