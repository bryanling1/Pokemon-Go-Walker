import cv2
import argparse
import math
import pdb

def run(vidSource, crop=None, scale=1, dest="./images/", frameskip=1):
    """
    From a video source, generate images from each frame

    crop happens before resize

    PARAMETERS
    ----------
    vidsource: str
        video file source
    
    crop: Array-like
        dimensions of crop (x1, y2, x2, y2)
    
    out_dim: Array-like
        dimensions of output image after crop (w, h)
    
    desf: str(opt)
        destination of output image
    """
    name=vidSource.split(".")[-2].split("/")[-1]
    video = cv2.VideoCapture(vidSource)
    count = 0
    skip_count = 0
    while True:
        success, img = video.read()
        if img is None: 
            break
        skip_count += 1
        if crop: 
            img = img[crop[1]:crop[3], crop[0]:crop[2], :]
        if scale:
            ratio = img.shape[0] / img.shape[1]
            new_width = int(float(img.shape[0]) * scale)
            new_height = int(new_width * ratio)
            img = cv2.resize(img, (new_width, new_height))
        if skip_count == frameskip:
            skip_count = 0
            count += 1
            cv2.imwrite(dest+name+str(count)+".png", img)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="", required=True)
    parser.add_argument("--crop", help="")
    parser.add_argument("--frameskip", help="")
    parser.add_argument("--scale", help="")
    parser.add_argument("--dest", help="", required=True)
    args = parser.parse_args()

    crop = args.crop
    frameskip = int(args.frameskip)
    scale = float(args.scale)

    if crop is not None:
        crop = crop.split("/")
        crop = [int(x) for x in crop]
    if scale is None: 
        scale = 1
    
    run(args.file, crop=crop, frameskip=frameskip, dest=args.dest, scale=scale)

    

    
    