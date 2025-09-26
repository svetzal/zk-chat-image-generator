from unittest.mock import Mock
from pathlib import Path

import pytest
from PIL import Image

from image_generator import GenerateImage
from stable_diffusion_gateway import StableDiffusionGateway


@pytest.fixture
def mock_service_provider():
    """Create a mock service provider with config service."""
    service_provider = Mock()
    config = Mock()
    config.vault = None
    service_provider.get_config.return_value = config
    return service_provider


@pytest.fixture
def mock_gateway():
    """Create a mock gateway that returns a test image."""
    gateway = Mock(spec=StableDiffusionGateway)
    test_image = Image.new('RGB', (64, 64), color='red')
    gateway.generate_image.return_value = test_image
    return gateway


class DescribeGenerateImage:
    """Tests for the image generation tool plugin"""

    def should_be_instantiated_with_service_provider(self):
        mock_service_provider = Mock()
        mock_gateway = Mock(spec=StableDiffusionGateway)

        tool = GenerateImage(mock_service_provider, mock_gateway)

        assert isinstance(tool, GenerateImage)
        assert tool.service_provider == mock_service_provider
        assert tool.gateway == mock_gateway

    def should_generate_image_and_save_to_vault(self, mock_service_provider, mock_gateway, tmp_path):
        mock_service_provider.get_config.return_value.vault = str(tmp_path)
        tool = GenerateImage(mock_service_provider, mock_gateway)
        test_description = "a red test image"
        test_filename = "test_image"

        result = tool.run(test_description, test_filename)

        mock_gateway.generate_image.assert_called_once_with(test_description)
        assert "test_image.png" in result
        assert "generated and saved" in result
        assert Path(tmp_path / "test_image.png").exists()

    def should_return_error_when_vault_not_available(self, mock_service_provider, mock_gateway):
        mock_service_provider.get_config.return_value = None
        tool = GenerateImage(mock_service_provider, mock_gateway)

        result = tool.run("test description", "test")

        assert "Error: Vault path not available" in result
        mock_gateway.generate_image.assert_not_called()

    def should_return_error_when_config_vault_is_none(self, mock_service_provider, mock_gateway):
        config = Mock()
        config.vault = None
        mock_service_provider.get_config.return_value = config
        tool = GenerateImage(mock_service_provider, mock_gateway)

        result = tool.run("test description", "test")

        assert "Error: Vault path not available" in result
        mock_gateway.generate_image.assert_not_called()
