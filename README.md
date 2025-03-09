# zk-rag-image-generator

A plugin for zk-rag that enables image generation using Stable Diffusion 3.5 Medium model.

## Description

This plugin provides a tool to generate images from textual descriptions using the Stable Diffusion 3.5 Medium model. It can be used to enhance your RAG (Retrieval-Augmented Generation) applications with image generation capabilities.

## Features

- Generate images from textual descriptions
- Save generated images as PNG files
- Integration with mojentic LLM tools
- Comprehensive error handling
- Configurable through a gateway pattern

## Installation

```bash
pip install zk-rag-image-generator
```

## Usage

The plugin will be automatically discovered by zk-rag when installed. It provides the `GenerateImage` tool which can be used to create images from textual descriptions.

Example usage through zk-rag:

```python
from zk_rag import get_tool

image_tool = get_tool("generate_image")
filename = image_tool.run(
    image_description="A serene mountain landscape at sunset with snow-capped peaks and a clear lake reflecting the orange sky",
    base_filename="mountain_sunset"
)
print(f"Image saved as: {filename}")  # Will print: Image saved as: mountain_sunset.png
```

## Requirements

- Python >= 3.11
- mojentic (LLM tools framework)
- torch, torchvision, torchaudio (PyTorch stack)
- diffusers (Stable Diffusion implementation)
- transformers (Hugging Face Transformers)
- accelerate (Hardware acceleration support)
- safetensors (Model weight handling)
- Additional dependencies: scipy, protobuf, sentencepiece

For the complete list with specific versions, see `requirements.txt`.

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```
3. Install pre-commit hooks (recommended):
   ```bash
   # Create a pre-commit hook that runs pytest
   cat > .git/hooks/pre-commit << 'EOL'
   #!/bin/sh

   # Run pytest
   echo "Running pytest..."
   python -m pytest

   # Store the exit code
   exit_code=$?

   # Exit with pytest's exit code
   exit $exit_code
   EOL

   # Make the hook executable
   chmod +x .git/hooks/pre-commit
   ```

## Testing Guidelines

- Tests are co-located with implementation files
- Run tests: `pytest`
- Linting: `flake8 src`
- Code style:
  - Max line length: 127
  - Max complexity: 10
  - Follow numpy docstring style

### Testing Best Practices
- Use pytest for testing, with mocker if you require mocking
- Do not use unittest or MagicMock directly
- Use @fixture markers for pytest fixtures
- Break up fixtures into smaller fixtures if they are too large
- Separate test phases with a single blank line
- Each test must fail for only one clear reason
- Only write mocks for our own gateway classes

## License

MIT License

## Author

Stacey Vetzal (stacey@vetzal.com)
