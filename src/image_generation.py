import torch
from diffusers import AutoPipelineForText2Image


MODEL_ID = "stabilityai/sd-turbo"


def generate_classroom_image(prompt, output_path="outputs/generated_classroom.png"):

    print("Loading local SD-Turbo model...")

    pipe = AutoPipelineForText2Image.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float32
    )

    pipe = pipe.to("cpu")

    print("Generating image...")

    image = pipe(
        prompt=prompt,
        num_inference_steps=1,
        guidance_scale=0.0,
        height=512,
        width=512
    ).images[0]

    image.save(output_path)

    print(f"Image saved to: {output_path}")


if __name__ == "__main__":

    prompt = (
        "A realistic university classroom with students attending a lecture, "
        "energy-efficient lighting, only necessary lights turned on, "
        "efficient air conditioning, modern academic environment, "
        "photorealistic"
    )

    generate_classroom_image(prompt)