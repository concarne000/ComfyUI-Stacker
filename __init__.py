import copy
import math
import os
import random
import sys
import traceback
import shlex
import os
import numpy as np
import torch
import hashlib
import json

from PIL import Image, ImageOps
from comfy.cli_args import args
from PIL.PngImagePlugin import PngInfo
from datetime import datetime
import pickle

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0)
 
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
        
any = AnyType("*")
 
class StackPushImage:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "input_image": ("IMAGE",)
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "execute"

    CATEGORY = "ConCarne"

    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, input_image, stackpath="./ComfyUI/Stack/", prompt=None, extra_pnginfo=None):
        if (key == ""):
            key = "default"
        
        print("Pushing stack")
        
        path = stackpath + key + "/"

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created path: {path}")      
        
        counter = 0
        
        for (batch_number, image) in enumerate(input_image):
            now = datetime.now()
            
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))

            filename = "stack" + now.strftime("%Y%m%d%H%M%S") + str(batch_number) + ".png"
            img.save(os.path.join(path, filename), pnginfo=metadata, compress_level=8)
            counter += 1
        
        return { "ui": { "dunnohowtofixyet": "null" } }

class StackPushString:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "stringvalue": ("STRING",)
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "execute"

    CATEGORY = "ConCarne"

    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, stringvalue, stackpath="./ComfyUI/Stack/"):
        if (key == ""):
            key = "default"
        
        print("Pushing stack")
        
        path = stackpath + key + "/"

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created path: {path}")      
        
        #for (batch_number, stringv) in enumerate(stringvalue): 
        now = datetime.now()            
        
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S") + "._st")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(stringvalue)
        
        return { "ui": { "dunnohowtofixyet": "null" } }

class StackPushInt:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "numbervalue": ("INT",)
            },
             "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "execute"

    CATEGORY = "ConCarne"

    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, numbervalue, stackpath="./ComfyUI/Stack/"):
        if (key == ""):
            key = "default"
        
        print("Pushing stack")
        
        path = stackpath + key + "/"

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created path: {path}")      
        
 #       for (batch_number, num) in enumerate(numbervalue):     
        now = datetime.now()
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S") + "._nu")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(numbervalue))
         
        return { "ui": { "dunnohowtofixyet": "null" } }

class StackPushObject:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "object": (any, {})
            },
             "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
        }

    RETURN_TYPES = ()

    FUNCTION = "execute"

    CATEGORY = "ConCarne"

    OUTPUT_NODE = True
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, object, stackpath="./ComfyUI/Stack/"):
        if (key == ""):
            key = "default"
        
        print("Pushing stack")
        
        path = stackpath + key + "/"

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created path: {path}")      
        
 #       for (batch_number, num) in enumerate(numbervalue):     
        now = datetime.now()
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S") + "._pkl")
        
        with open(filename, 'wb') as f:
            pickle.dump(object, f)
         
        return { "ui": { "dunnohowtofixyet": "null" } }

                        

class StackPopImage:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
            },
            
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
            
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, stackpath="./ComfyUI/Stack/"):
        path = stackpath + key + "/"
        
        images = []
        
        if not os.path.exists(path):
            print(f"Key doesn't exist\n")      
            
        # Get all .png files sorted by name
        png_files = sorted([f for f in os.listdir(path) if f.lower().endswith('.png')] )

        last_file = ""

        # Check if there are any PNG files
        if png_files:
            last_file = os.path.join(path, png_files[-1])
            image = Image.open(last_file)
            print(f"Opened: {last_file}")
        else:
            raise Exception("No image files found. Stack Empty.")
            
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = pil2tensor(image).unsqueeze(0)
                
        images.append(image)
        
        os.remove(last_file)
        
        return ( torch.cat(images, dim=0), )

class StackPopString:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
            
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, stackpath="./ComfyUI/Stack/"):
        path = stackpath + key + "/"
        
        images = []
        
        if not os.path.exists(path):
            print(f"Key doesn't exist\n")      
            
        # Get all .png files sorted by name
        png_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._st')] )

        last_file = ""

        result = ""

        # Check if there are any PNG files
        if png_files:
            last_file = os.path.join(path, png_files[-1])
            with open(last_file, 'r', encoding='utf-8') as f:
                result = f.read()
            print(f"Opened: {last_file}")
        else:
            raise Exception("No string files found. Stack Empty.")
                     
        os.remove(last_file)
        
        return (result, )

class StackPopInt:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
            
        }
        
    RETURN_TYPES = ("INT",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, stackpath="./ComfyUI/Stack/"):
        path = stackpath + key + "/"
        
        images = []
        
        if not os.path.exists(path):
            print(f"Key doesn't exist\n")      
            
        # Get all .png files sorted by name
        png_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._nu')] )

        last_file = ""

        result = ""

        # Check if there are any PNG files
        if png_files:
            last_file = os.path.join(path, png_files[-1])
            with open(last_file, 'r', encoding='utf-8') as f:
                result = f.read()
            print(f"Opened: {last_file}")
        else:
            raise Exception("No integer files found. Stack Empty.")
                      
        os.remove(last_file)
        
        return (int(result), )

class StackPopObject:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
            },
            
        }
        
    RETURN_TYPES = (any,)
    RETURN_NAMES = ("any",)
#    RETURN_TYPES = ("CONDITIONING","LATENT","IMAGE","STRING")
#    OUTPUT_NODE = True
    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, stackpath="./ComfyUI/Stack/"):
        path = stackpath + key + "/"
        
        images = []
        
        if not os.path.exists(path):
            print(f"Key doesn't exist\n")      
            
        # Get all .png files sorted by name
        png_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._pkl')] )

        last_file = ""

        result = ""

        # Check if there are any PNG files
        if png_files:
            last_file = os.path.join(path, png_files[-1])
            with open(last_file, 'rb') as f:
                loaded_object = pickle.load(f)
            print(f"Opened: {last_file}")
        else:
            raise Exception("No integer files found. Stack Empty.")
                      
        os.remove(last_file)
        
        return (loaded_object,)#loaded_object,loaded_object,loaded_object )

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "StackPushImage": StackPushImage,
    "StackPushString": StackPushString,
    "StackPushInt": StackPushInt,
    "StackPushObject": StackPushObject,
    "StackPopImage": StackPopImage,
    "StackPopString": StackPopString,
    "StackPopInt": StackPopInt,
    "StackPopObject": StackPopObject,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "StackPushImage": "StackPushImage",
    "StackPushString": "StackPushString",
    "StackPushInt": "StackPushInt",
    "StackPushObject": "StackPushObject",
    "StackPopImage": "StackPopImage",
    "StackPopString": "StackPopString",
    "StackPopInt": "StackPopInt",
    "StackPopObject": "StackPopObject",
}
