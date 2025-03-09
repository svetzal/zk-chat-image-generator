from pathlib import Path
from typing import Optional

from mojentic.llm import LLMBroker
from mojentic.llm.tools.llm_tool import LLMTool

from stable_diffusion_gateway import StableDiffusionGateway


class GenerateImage(LLMTool):
    """Tool to generate images from a description using the StableDiffusion 3.5 Medium model."""

    def __init__(self, vault: str, llm: LLMBroker, gateway: Optional[StableDiffusionGateway] = None):
        """Initialize the tool with an optional gateway."""
        super().__init__()
        self.vault = vault
        self.gateway = gateway or StableDiffusionGateway()

    def run(self, image_description: str, base_filename: str) -> str:
        """Generate an image based on the description and save it to a file.

        Parameters
        ----------
        image_description : str
            The text description of the image to generate
        base_filename : str
            The base name for the output file (without extension)

        Returns
        -------
        str
            The filename relative to the vault path
        """
        filename = Path(self.vault) / f"{base_filename}.png"
        image = self.gateway.generate_image(image_description)
        image.save(filename)
        return f"""
The image has been generated and saved at `{base_filename}.png`.
You can embed it in your markdown file using the following syntax: `![image]({base_filename}.png)`
""".strip()

    @property
    def descriptor(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": "generate_image",
                "description": "Generates a PNG image from a description using the StableDiffusion 3.5 Medium model, and return a relative path to that image that can be used in a markdown file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_description": {
                            "type": "string",
                            "description": "A detailed description of the image you wish to generate. Include information about the subject, background, mood or tone, lighting, camera angle, and any other relevant details."
                        },
                        "base_filename": {
                            "type": "string",
                            "description": "The filename to save the generated image as, without the PNG extension."
                        }
                    },
                    "required": ["image_description"]
                }
            }
        }
