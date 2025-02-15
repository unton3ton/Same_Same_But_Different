from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch
import ollama

response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': ['output.png']
    }]
)

# print(response.message.content)

repo_id = "stabilityai/stable-diffusion-2-base"
pipe = DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, variant="fp16")

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

prompt = response.message.content
image = pipe(prompt, num_inference_steps=25).images[0]
image.save('neurogenerate.png')