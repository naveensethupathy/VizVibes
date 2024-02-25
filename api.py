from auth_token import auth_token
from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
device = "cuda"
#model_id = "CompVis/stable-diffusion-v1-4"
model_id = "SG161222/Realistic_Vision_V2.0"
#pipe = StableDiffusionPipeline.from_pretrained(model_id,torch_dtype=torch.float16, variant='fp16', use_auth_token = auth_token)
pipe = StableDiffusionPipeline.from_pretrained(model_id,torch_dtype=torch.float16, use_auth_token = auth_token)
pipe.to(device)

@app.get("/")
def generate(prompt:str):
    base_prompt = "((detailed face)),((Full body)),((wide-angle)),((detailed facial feature)),stockphoto,high-quality,high-resolution,8k,HD,high resolution photography, insanely detailed, fine details, professional color grading, 8k octane rendering, best quality, 8k, HD, DSLR, Fujifilm XT3, film grain, award winning,perfect face, perfect hand"
    neg_base_prompt = "blurred, grainy, pixelated, low quality, oversaturated, overexposed, text, web address, artist name, signature, watermark, bad proportions, mutation, furry, mutated, extra_limb, extra limb, watermark, missing limbs, distortion, black and white, low resolution, missing hands, low detail, closeup, censored, deformed hands, out of focus, bad framing, tiling, doll, grainy, cat, feet, fashion, shoes, grayscale, monotone, old, blind, amputation, watermarked, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, words, letters, blurry, oversaturated colors, overblown contrast, doubling, multiple copies, double torso, glare, lens flare, ((two heads)), ((double heads)), white background, feathers, censored, twin, second person,"
    with autocast(device):
        image = pipe(prompt + base_prompt,negative_prompt=neg_base_prompt,guidance_scale=7.5,height = 600 ,width=600).images[0]
    image.save("testimage.png")
    buffer = BytesIO()
    image.save(buffer,format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())
    
    return Response(content=imgstr,media_type="image/png")