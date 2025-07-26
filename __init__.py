import copy
import math
import os
import random
import sys
import traceback
import shlex
import numpy as np
import torch
import hashlib
import json

from PIL import Image, ImageOps
from comfy.cli_args import args
from PIL.PngImagePlugin import PngInfo
from datetime import datetime
import pickle
import re
import folder_paths

def clean_filename(filename: str) -> str:
    # Remove any character that is not a-z, A-Z, 0-9, space, dot, underscore, or hyphen
    cleaned = re.sub(r'[^\w\s.-]', '', filename)
    # Optionally replace spaces with underscores (or remove)
    cleaned = cleaned.replace(' ', '_')
    return cleaned
    
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0)

def ensure_stack_dir(stackpath, key):
    path = os.path.join(stackpath, clean_filename(key))
    os.makedirs(path, exist_ok=True)
    return path
 
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
                "input_image": ("IMAGE",)
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
            
        path = ensure_stack_dir(stackpath,key)  
        
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

            filename = "stack" + now.strftime("%Y%m%d%H%M%S%f") + str(batch_number) + ".png"
            img.save(os.path.join(path, filename), pnginfo=metadata, compress_level=8)
            counter += 1
        
        return ( None, )

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
        
        path = ensure_stack_dir(stackpath,key)  
       
        #for (batch_number, stringv) in enumerate(stringvalue): 
        now = datetime.now()            
        
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S%f") + "._st")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(stringvalue)
        
        return ( None, )

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
        
        path = ensure_stack_dir(stackpath,key)  
        
 #       for (batch_number, num) in enumerate(numbervalue):     
        now = datetime.now()
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S%f") + "._nu")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(numbervalue))
         
        return ( None, )

class StackPushFloat:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "numbervalue": ("FLOAT",)
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
        
        path = ensure_stack_dir(stackpath,key)      
        
 #       for (batch_number, num) in enumerate(numbervalue):     
        now = datetime.now()
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S%f") + "._fl")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(numbervalue))
         
        return ( None, )

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
        
        path = ensure_stack_dir(stackpath,key)  
        
 #       for (batch_number, num) in enumerate(numbervalue):     
        now = datetime.now()
        filename = os.path.join(path,"stack" + now.strftime("%Y%m%d%H%M%S%f") + "._pkl")
        
        with open(filename, 'wb') as f:
            pickle.dump(object, f)
         
        return ( None, )

                        

class StackPopImage:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "fallback_enabled": ("BOOLEAN", {"default": False}),
                "override_enabled": ("BOOLEAN", {"default": False}),
                "stackmode": ( ['Normal', 'Peek', 'Pop Bottom', 'Peek Bottom'], {"default": "Normal"} ),
            },
            
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
                "fallback_item": ("IMAGE",),
                "override_item": ("IMAGE",),
            },
            
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, fallback_enabled, override_enabled, stackmode, fallback_item=None, override_item=None, stackpath="./ComfyUI/Stack/"):
        
        if override_enabled:
            return (override_item,)
            
        path = os.path.join(stackpath,key)  
        
        images = []
        
        if not os.path.exists(path):
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception(f"Key doesn't exist") 
            
        # Get all .png files sorted by name
        sorted_files = sorted([f for f in os.listdir(path) if f.lower().endswith('.png')] )

        last_file = ""

        # Check if there are any PNG files
        if sorted_files:
            if stackmode == 'Normal' or stackmode == 'Peek':
                last_file = os.path.join(path, sorted_files[-1])
            else:
                last_file = os.path.join(path, sorted_files[0])

            image = Image.open(last_file)
            #print(f"Opened: {last_file}")
        else:
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception("No image files found. Stack Empty.")
            
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = pil2tensor(image).unsqueeze(0)
                
        images.append(image)
        
        if stackmode == 'Normal' or stackmode == 'Pop Bottom':
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
                "fallback_enabled": ("BOOLEAN", {"default": False}),
                "override_enabled": ("BOOLEAN", {"default": False}),
                "stackmode": ( ['Normal', 'Peek', 'Pop Bottom', 'Peek Bottom'], {"default": "Normal"} ),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
                "fallback_item": ("STRING",),
                "override_item": ("STRING",),
            },
            
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, fallback_enabled, fallback_item, override_enabled, override_item, stackmode, stackpath="./ComfyUI/Stack/"):
        
        if override_enabled:
            return (override_item,)
            
        path = os.path.join(stackpath,key)  
        
        images = []
        
        if not os.path.exists(path):
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception(f"Key doesn't exist") 
                
        # Get all ._st files sorted by name
        sorted_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._st')] )

        last_file = ""

        result = ""

        # Check if there are any string files
        if sorted_files:
            if stackmode == 'Normal' or stackmode == 'Peek':
                last_file = os.path.join(path, sorted_files[-1])
            else:
                last_file = os.path.join(path, sorted_files[0])

            with open(last_file, 'r', encoding='utf-8') as f:
                result = f.read()
            #print(f"Opened: {last_file}")
        else:
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception("No string files found. Stack Empty.")
                     
        if stackmode == 'Normal' or stackmode == 'Pop Bottom':
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
                "fallback_enabled": ("BOOLEAN", {"default": False}),
                "override_enabled": ("BOOLEAN", {"default": False}),
                "stackmode": ( ['Normal', 'Peek', 'Pop Bottom', 'Peek Bottom'], {"default": "Normal"} ),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
                "fallback_item": ("INT",),
                "override_item": ("INT",),
            },
            
        }
        
    RETURN_TYPES = ("INT",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, fallback_enabled, fallback_item, override_enabled, override_item, stackmode, stackpath="./ComfyUI/Stack/"):
        
        if override_enabled:
            return (override_item,)

        path = os.path.join(stackpath,key)  
        
        images = []
        
        if not os.path.exists(path):
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception(f"Key doesn't exist") 
                
        # Get all ._nu files sorted by name
        sorted_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._nu')] )

        last_file = ""

        result = ""

        # Check if there are any int files
        if sorted_files:
            if stackmode == 'Normal' or stackmode == 'Peek':
                last_file = os.path.join(path, sorted_files[-1])
            else:
                last_file = os.path.join(path, sorted_files[0])
                
            with open(last_file, 'r', encoding='utf-8') as f:
                result = f.read()
            #print(f"Opened: {last_file}")
        else:
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception("No integer files found. Stack Empty.")
                      
        if stackmode == 'Normal' or stackmode == 'Pop Bottom':
            os.remove(last_file)
        
        return (int(result), )

class StackPopFloat:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "fallback_enabled": ("BOOLEAN", {"default": False}),
                "override_enabled": ("BOOLEAN", {"default": False}),
                "stackmode": ( ['Normal', 'Peek', 'Pop Bottom', 'Peek Bottom'], {"default": "Normal"} ),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
                "fallback_item": ("FLOAT",),
                "override_item": ("FLOAT",),
            },
            
        }
        
    RETURN_TYPES = ("FLOAT",)

    FUNCTION = "execute"

    CATEGORY = "ConCarne"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
   
    def execute(self, key, fallback_enabled, fallback_item, override_enabled, stackmode, override_item, stackpath="./ComfyUI/Stack/"):
        
        if override_enabled:
            return (override_item,)
            
        path = os.path.join(stackpath,key)  
        
        images = []
        
        if not os.path.exists(path):
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception(f"Key doesn't exist") 
                
        # Get all ._fl files sorted by name
        sorted_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._fl')] )

        last_file = ""

        result = ""

        # Check if there are any float files
        if sorted_files:
            if stackmode == 'Normal' or stackmode == 'Peek':
                last_file = os.path.join(path, sorted_files[-1])
            else:
                last_file = os.path.join(path, sorted_files[0])
            with open(last_file, 'r', encoding='utf-8') as f:
                result = f.read()
            #print(f"Opened: {last_file}")
        else:
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception("No float files found. Stack Empty.")
                      
        if stackmode == 'Normal' or stackmode == 'Pop Bottom':
            os.remove(last_file)
        
        return (float(result), )

class StackPopObject:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "default"}),
                "fallback_enabled": ("BOOLEAN", {"default": False}),
                "override_enabled": ("BOOLEAN", {"default": False}),
                "stackmode": ( ['Normal', 'Peek', 'Pop Bottom', 'Peek Bottom'], {"default": "Normal"} ),
            },
            "optional": {
                "stackpath": ("STRING",{"default": "./ComfyUI/Stack/"}),
                "fallback_item": (any, {}),
                "override_item": (any, {}),
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
   
    def execute(self, key, fallback_enabled, override_enabled, stackmode, override_item=None, fallback_item=None, stackpath="./ComfyUI/Stack/"):
        
        if not os.path.exists(os.path.join(folder_paths.get_user_directory(), "allow_generic_types.plz")):
            raise Exception("Generic object popping not allowed until dummy file \"allow_generic_types.plz\" exists in user folder ("+folder_paths.get_user_directory()+"). You should not do this unless you understand the risks of loading generic objects.")
                
        if override_enabled:
            return (override_item,)

        path = os.path.join(stackpath,key)  
        
        images = []
        
        if not os.path.exists(path):
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception(f"Key doesn't exist") 
                
        # Get all .pkl files sorted by name
        sorted_files = sorted([f for f in os.listdir(path) if f.lower().endswith('._pkl')] )

        last_file = ""

        result = ""

        # Check if there are any pickle files
        if sorted_files:
            if stackmode == 'Normal' or stackmode == 'Peek':
                last_file = os.path.join(path, sorted_files[-1])
            else:
                last_file = os.path.join(path, sorted_files[0])

            with open(last_file, 'rb') as f:
                loaded_object = pickle.load(f)
            #print(f"Opened: {last_file}")
        else:
            if (fallback_enabled):
                return ( fallback_item, )
            else:
                raise Exception("No object files found. Stack Empty.")
                      
        if stackmode == 'Normal' or stackmode == 'Pop Bottom':
            os.remove(last_file)
        
        return (loaded_object,)#loaded_object,loaded_object,loaded_object )

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "StackPushImage": StackPushImage,
    "StackPushString": StackPushString,
    "StackPushInt": StackPushInt,
    "StackPushFloat": StackPushFloat,
    "StackPushObject": StackPushObject,
    "StackPopImage": StackPopImage,
    "StackPopString": StackPopString,
    "StackPopInt": StackPopInt,
    "StackPopFloat": StackPopFloat,
    "StackPopObject": StackPopObject,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "StackPushImage": "StackPushImage",
    "StackPushString": "StackPushString",
    "StackPushInt": "StackPushInt",
    "StackPushFloat": "StackPushFloat",
    "StackPushObject": "StackPushObject",
    "StackPopImage": "StackPopImage",
    "StackPopString": "StackPopString",
    "StackPopInt": "StackPopInt",
    "StackPopFloat": "StackPopFloat",
    "StackPopObject": "StackPopObject",
}
