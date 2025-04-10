from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import AutoPipelineForText2Image
import torch
import os
from dotenv import load_dotenv

load_dotenv()

device = 'mps' if torch.backends.mps.is_available() else 'cpu'

app = FastAPI(title = "Logo Generator Service")

# Initialize the SDXL Turbo pipeline
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", 
                                                torch_dtype=torch.float16, 
                                                variant="fp16")
pipe = pipe.to(device)

class LogoRequest(BaseModel):
    prompt: str




@app.post("/generate-logo")
async def generate_logo(request: LogoRequest):
    try:
        # Generate image
        image = pipe(
            prompt=request.prompt,
            num_inference_steps=20
            #guidance_scale=0.0
        ).images[0]
        
        # Save the image
        output_path = "generated_logo.png"
        image.save(output_path)
        
        return {"status": "success", "image_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
