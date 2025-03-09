import torch
from diffusers import StableDiffusion3Pipeline


class StableDiffusionGateway:
    """Gateway for interacting with the Stable Diffusion API."""

    def __init__(self, num_inference_steps: int = 40, guidance_scale: float = 4.5):
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self._pipe = None

    @property
    def pipe(self):
        """Lazily initialize the pipeline on first access."""
        if self._pipe is None:
            self._pipe = StableDiffusion3Pipeline.from_pretrained(
                "stabilityai/stable-diffusion-3.5-medium",
                torch_dtype=torch.float16
            )
            self._pipe = self._pipe.to("mps")
        return self._pipe

    def generate_image(self, description: str) -> any:
        """Generate an image from a description."""
        return self.pipe(
            description,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
        ).images[0]
