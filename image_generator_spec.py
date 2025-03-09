from pathlib import Path

import pytest
from unittest.mock import Mock, patch
from PIL import Image
import torch
from image_generator import GenerateImage
from stable_diffusion_gateway import StableDiffusionGateway


@pytest.fixture
def mock_gateway():
    gateway = Mock(spec=StableDiffusionGateway)
    # Create a small test image
    test_image = Image.new('RGB', (64, 64), color='red')
    gateway.generate_image.return_value = test_image
    return gateway

def test_generate_image_run(mock_gateway, tmp_path):
    tool = GenerateImage(gateway=mock_gateway)
    full_path = tool.run("test description", "test")
    assert Path(full_path).name == "test.png"
    mock_gateway.generate_image.assert_called_once_with("test description")
