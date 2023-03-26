import numpy as np
from PIL import Image

# to do: 
def encode():
    cover_image = Image.open("bird.jpg")
    image_to_hide = Image.open("cat.jpg")
    
    image_bytes = np.array(cover_image)
    hidden_image_bytes = np.array(image_to_hide)
    new_image = np.empty_like(np.asarray(cover_image))
    
    print(image_bytes.shape)
    h = hidden_image_bytes.shape[0]
    w = hidden_image_bytes.shape[1]
    t = hidden_image_bytes.shape[2]

    if(len(image_bytes) > len(hidden_image_bytes)*2):
        for i, nested_array in enumerate(image_bytes):
            for j, array_bytes in enumerate(nested_array):
                for k, byte in enumerate(array_bytes):
                    cover = np.unpackbits(byte)
                    if i < h and j < w and k < t:
                        to_hide = np.unpackbits(hidden_image_bytes[i][j][k])
                        cover[6] = to_hide[0]
                        cover[7] = to_hide[1]
                        changed_byte = np.packbits(cover)
                        new_image[i][j][k] = changed_byte[0]
                    else:
                        new_image[i][j][k] = np.packbits(cover)
        new_image[new_image.shape[0]-1][new_image.shape[1]-1] = [h,w,t]
        print(new_image[new_image.shape[0]-1][new_image.shape[1]-1])
        save_image = Image.fromarray(new_image)
        save_image.save("got_steganoed.png")
    else:
        print("cover image too small")

def decode():
    decode_image = Image.open("got_steganoed.png")
    decode_bytes = np.array(decode_image)
    #new_image = np.empty_like(np.asarray(decode_bytes))
    # h = decode_bytes[decode_bytes.shape[0]-1][decode_bytes.shape[1]-1][0]
    # w = decode_bytes[decode_bytes.shape[0]-1][decode_bytes.shape[1]-1][1]
    # t = decode_bytes[decode_bytes.shape[0]-1][decode_bytes.shape[1]-1][2]
    h = 463
    w = 703
    t = 3
    new_image = np.empty((h,w,t), dtype = np.uint8)
    print(h, w, t)
    for i, nested_array in enumerate(decode_bytes):
        for j, array_bytes in enumerate(nested_array):
            for k, byte in enumerate(array_bytes):
                if i < h and j < w and k < t:
                    binary = np.unpackbits(byte)
                    new_image[i][j][k] = str(binary[6]) + str(binary[7])
                # else:
                #     new_image[i][j][k] =  byte
    PILimage = Image.fromarray(new_image)
    PILimage.save("decoded.png")

#encode()
decode()