# -*- coding: utf-8 -*-
"""segmentation"""

from PIL import Image, ImageOps, ImageFilter
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from model.u2net import U2NET, U2NETP  

def load_model(model_path: str):
    
    if "u2netp" in model_path.lower():        
        net = U2NETP(3, 1)
    else:                                    
        net = U2NET(3, 1)

    net.load_state_dict(torch.load(model_path, map_location="cpu"))
    net.eval()
    return net

def get_segmentation_mask(image: Image.Image, model):
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])])

    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        d1, *_ = model(input_tensor)
    
    mask = d1[0][0].numpy()
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask = Image.fromarray((mask * 255).astype(np.uint8)).resize(image.size)
    return mask