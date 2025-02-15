# https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/stable_diffusion/stable_diffusion_2.md?ysclid=m709apofgc89030639

# pip install --upgrade pip
# pip install --upgrade diffusers[torch]
# pip install transformers

import torch
from diffusers import StableDiffusionDepth2ImgPipeline
from diffusers.utils import load_image, make_image_grid

pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
	    "stabilityai/stable-diffusion-2-depth",
	    torch_dtype=torch.float16,
	).to("cuda")


url = "000000039769.jpg" # "http://images.cocodataset.org/val2017/000000039769.jpg"
init_image = load_image(url)
prompt = "two tigers"
negative_prompt = "bad, deformed, ugly, bad anotomy"
image = pipe(prompt=prompt, image=init_image, negative_prompt=negative_prompt, strength=0.7).images[0]
make_image_grid([init_image, image], rows=1, cols=2)

image.save("output.png")
