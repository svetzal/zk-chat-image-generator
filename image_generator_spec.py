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

def test_generate_image_run(mock_gateway, tmp_path, mocker):
    tool = GenerateImage(vault=str(tmp_path), llm=mocker.MagicMock(), gateway=mock_gateway)
    relative_path = tool.run("test description", "test")

    assert "test.png" in relative_path

    mock_gateway.generate_image.assert_called_once_with("test description")
