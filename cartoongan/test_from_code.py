import time
import os

import numpy as np
from PIL import Image

import torch
import torchvision.transforms as transforms
from torch.autograd import Variable

from cartoongan.network.Transformer import Transformer


def transformAll(logger, inputFolder, outputFolder, load_size=450, gpu=-1):
    styles = ["Hosoda", "Hayao", "Shinkai", "Paprika"]
    for images in os.listdir(inputFolder):
        logger.info("transformAll: "+ images)
        inputPath = os.path.join(inputFolder, images)
        combinedImgPath = os.path.join(outputFolder, 'combined_'+ images)        
        combinedImg = inputPath
        
        #resize input image        
        image1 = Image.open(inputPath)
        image1 = image1.resize((load_size, load_size))
        image1.save(inputPath)

        for style in styles:
            logger.info("===> Style: "+ style)
            outputPath = transform(style, inputPath, outputFolder, load_size, gpu)
            logger.info("combinedImg: "+combinedImg)
            logger.info("outputPath: "+outputPath)
            logger.info("combinedImgPath: "+combinedImgPath)
            combinedImg = mergeImage(combinedImg, outputPath, combinedImgPath)
    return 'Done'


def mergeImage(img1, img2, newImgName):
    image1 = Image.open(img1)
    image2 = Image.open(img2)

    image1_size = image1.size
    image2_size = image2.size
        
    new_image = Image.new('RGB',(image1_size[0]+image2_size[0], image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0],0))
    
    # new_image.save(newImgName, os.path.splitext(os.path.basename(newImgName))[1].upper())
    new_image.save(newImgName, "JPEG")
    return newImgName

def transform(style, input, output, load_size=450, gpu=-1):

    models = {}
    model = Transformer()
    model.load_state_dict(torch.load(os.path.join("./cartoongan/pretrained_models/", style + '_net_G_float.pth')))
    model.eval()
    models[style] = model

    if gpu > -1:
        model.cuda()
    else:
        model.float()

    input_image = Image.open(input).convert("RGB")
    h, w = input_image.size

    ratio = h * 1.0 / w

    if ratio > 1:
        h = load_size
        w = int(h * 1.0 / ratio)
    else:
        w = load_size
        h = int(w * ratio)

    input_image = input_image.resize((h, w), Image.BICUBIC)
    input_image = np.asarray(input_image)

    input_image = input_image[:, :, [2, 1, 0]]
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)

    input_image = -1 + 2 * input_image
    if gpu > -1:
        input_image = Variable(input_image).cuda()
    else:
        input_image = Variable(input_image).float()

    t0 = time.time()
    print("input shape", input_image.shape)
    with torch.no_grad():
        output_image = model(input_image)[0]
    print(f"inference time took {time.time() - t0} s")

    output_image = output_image[[2, 1, 0], :, :]
    output_image = output_image.data.cpu().float() * 0.5 + 0.5

    output_image = output_image.numpy()

    output_image = np.uint8(output_image.transpose(1, 2, 0) * 255)
    output_image = Image.fromarray(output_image)

    file_name = os.path.splitext(os.path.basename(input))[0]
    ext = os.path.splitext(os.path.basename(input))[1]

    output_path = os.path.join(output , file_name + '_' + style + ext)
    output_image.save(output_path)

    # return output_image
    return output_path
