````instructions
# Project Guidelines for zk-chat-image-generator

## Project Architecture

This is a **plugin for the zk-chat ecosystem** that provides AI image generation functionality using Stable Diffusion 3.5 Medium model. The plugin follows the **Mojentic LLMTool pattern** with service provider architecture introduced in v2.0.0.

### Core Components

- **`image_generator.py`**: Main plugin implementation containing:
  - `GenerateImage` - Main tool class inheriting from `mojentic.llm.tools.llm_tool.LLMTool`
- **`stable_diffusion_gateway.py`**: Gateway class handling Stable Diffusion model interactions
- **Plugin Discovery**: Uses `pyproject.toml` entry points: `zk_rag_plugins = { image_generator = "image_generator:GenerateImage" }`

### Key Plugin Patterns

1. **Service Provider Architecture** (v2.0.0+): Constructor accepts `service_provider` parameter instead of deprecated `vault`/`llm` parameters
2. **Gateway Pattern**: Uses `StableDiffusionGateway` for model interactions with dependency injection support
3. **File System Integration**: Uses service provider to access vault path for saving generated images
4. **Tool Descriptor**: Implements `@property descriptor` returning OpenAI function call schema

## Code Organization

### Import Structure
1. Imports should be grouped in the following order, with one blank line between groups:
   - Standard library imports
   - Third-party library imports
   - Local application imports
2. Within each group, imports should be sorted alphabetically

### Naming Conventions
1. Use descriptive variable names that indicate the purpose or content
2. Prefix test mock objects with 'mock_' (e.g., mock_gateway)
3. Prefix test data variables with 'test_' (e.g., test_description)
4. Use '_' for unused variables or return values

### Type Hints and Documentation
1. Use type hints for method parameters and class dependencies
2. Include return type hints when the return type isn't obvious
3. Use docstrings for methods that aren't self-explanatory
4. Class docstrings should describe the purpose and behavior of the component
5. Follow numpy docstring style

### Logging Conventions
1. Use structlog for all logging
2. Initialize logger at module level using `logger = structlog.get_logger()`
3. Include relevant context data in log messages
4. Use appropriate log levels:
   - INFO for normal operations
   - DEBUG for detailed information
   - WARNING for concerning but non-critical issues
   - ERROR for critical issues
5. Use print statements only for direct user feedback

### Code Conventions
1. Do not write comments that just restate what the code does
2. Use pydantic BaseModel classes, do not use @dataclass

## Testing Guidelines

### General Rules
1. Use pytest for all testing
2. Test files:
   - Named with `_spec.py` suffix
   - Co-located with implementation files (same folder as the test subject)
3. Code style:
   - Max line length: 127
   - Max complexity: 10
4. Run tests with: `pytest`
5. Run linting with: `flake8 .`

### BDD-Style Tests
We follow a Behavior-Driven Development (BDD) style using the "Describe/should" pattern to make tests readable and focused on component behavior.

#### Test Structure
1. Tests are organized in classes that start with "Describe" followed by the component name
2. Test methods:
   - Start with "should_"
   - Describe the expected behavior in plain English
   - Follow the Arrange/Act/Assert pattern (separated by blank lines)
3. Do not use comments (eg Arrange, Act, Assert) to delineate test sections - just use a blank line
4. No conditional statements in tests - each test should fail for only one clear reason
5. Do not test private methods directly (those starting with '_') - test through the public API

#### Fixtures and Mocking
1. Use pytest @fixture for test prerequisites:
   - Break large fixtures into smaller, reusable ones
   - Place fixtures in module scope for sharing between classes
   - Place module-level fixtures at the top of the file
2. Mocking:
   - Use pytest's `mocker` for dependencies
   - Use Mock's spec parameter for type safety (e.g., `Mock(spec=ServiceProvider)`)
   - Mock the `StableDiffusionGateway` for all model interactions
   - Do not mock library internals or private functions
   - Do not use unittest or MagicMock directly

#### Best Practices
1. Test organization:
   - Place instantiation/initialization tests first
   - Group related scenarios together (success and failure cases)
   - Keep tests focused on single behaviors
2. Assertions:
   - One assertion per line for better error identification
   - Use 'in' operator for partial string matches
   - Use '==' for exact matches
3. Test data:
   - Use fixtures for reusable prerequisites
   - Define complex test data structures within test methods

### Plugin-Specific Testing Patterns
- **Gateway Mocking**: Mock `StableDiffusionGateway.generate_image()` to avoid actual model calls
- **File System**: Mock file operations and verify correct paths are used
- **Error Scenarios**: Test vault path unavailability and image generation failures
- **Return Format**: Verify proper markdown-formatted responses with image embedding syntax

## Plugin Development Best Practices

### 1. Error Handling
Always handle errors gracefully and return meaningful error messages:

```python
def run(self, image_description: str, base_filename: str) -> str:
    try:
        # Plugin logic here
        config = self.service_provider.get_config()
        if not config or not config.vault:
            return "Error: Vault path not available"

        filename = Path(config.vault) / f"{base_filename}.png"
        image = self.gateway.generate_image(image_description)
        image.save(filename)

        return f"Image generated and saved at `{base_filename}.png`"
    except Exception as e:
        logger.error("Image generation error", error=str(e), description=image_description)
        return f"Error generating image: {str(e)}"
```

### 2. Input Validation
Validate inputs and provide clear feedback:

```python
def run(self, image_description: str, base_filename: str = None) -> str:
    if not image_description:
        return "Error: image_description parameter is required"

    if not image_description.strip():
        return "Error: image_description cannot be empty"

    if not base_filename:
        # Generate a default filename from description
        base_filename = "generated_image"

    if not base_filename.replace('_', '').replace('-', '').isalnum():
        return "Error: base_filename must contain only letters, numbers, hyphens, and underscores"

    # Continue with plugin logic...
```

### 3. Descriptive Function Descriptors
Make your tool easy for the LLM to understand and use:

```python
@property
def descriptor(self) -> dict:
    return {
        "type": "function",
        "function": {
            "name": "generate_image",
            "description": "Generates a PNG image from a detailed description using the StableDiffusion 3.5 Medium model. Use this when the user wants to create, generate, or visualize an image from a text description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_description": {
                        "type": "string",
                        "description": "A detailed description of the image to generate. Include subject, style, mood, lighting, composition, and any other visual details. More detail produces better results."
                    },
                    "base_filename": {
                        "type": "string",
                        "description": "The filename to save the generated image as, without the PNG extension. Use descriptive names that relate to the image content."
                    }
                },
                "required": ["image_description"]
            }
        }
    }
```

### 4. Use Structured Logging
Include relevant context in your log messages:

```python
logger.info(
    "Image generation completed",
    description_length=len(image_description),
    filename=f"{base_filename}.png",
    vault_path=config.vault
)
```

### 5. Service Availability Checking
Always check for required services:

```python
def run(self, image_description: str, base_filename: str) -> str:
    # Check for required configuration service
    try:
        config = self.service_provider.require_service(ServiceType.CONFIG)
        if not config.vault:
            return "Error: No vault configured for saving images"
    except RuntimeError as e:
        return f"Configuration service not available: {e}"

    # Continue with image generation...
```

## Available Runtime Services

### Service Provider Access Pattern
Use the service provider to access zk-chat services:

```python
from zk_chat.services import ServiceProvider, ServiceType

def __init__(self, service_provider: ServiceProvider):
    super().__init__()
    self.service_provider = service_provider
    self.gateway = gateway or StableDiffusionGateway()

    # Access services through convenient methods
    config = service_provider.get_config()
    # Image generator primarily needs config for vault path
```

### Available Services for Image Generator

#### 1. Configuration Service (Required)
- **Purpose**: Access vault path for saving generated images
- **Usage**: Get vault directory to save PNG files
- **Access**: `service_provider.get_config()`

```python
def get_vault_path(self) -> str:
    """Get the vault path for saving images."""
    config = self.service_provider.get_config()
    if not config or not config.vault:
        raise RuntimeError("Vault path not configured")
    return config.vault
```

#### 2. Filesystem Gateway (Optional)
- **Purpose**: Consistent file operations integrated with zk-chat
- **Usage**: Alternative to direct Path operations for file handling
- **Access**: `service_provider.get_filesystem_gateway()`

#### 3. Smart Memory (Optional)
- **Purpose**: Remember user preferences for image generation
- **Usage**: Store preferred styles, common prompts, generation settings
- **Access**: `service_provider.get_smart_memory()`

```python
def remember_generation_preference(self, preference: str) -> str:
    """Store image generation preferences."""
    memory = self.service_provider.get_smart_memory()
    if memory:
        memory.store(f"Image generation preference: {preference}")
        return "Preference stored"
    return "Memory service not available"
```

#### 4. LLM Broker (Optional)
- **Purpose**: Enhance or analyze image descriptions
- **Usage**: Improve prompt quality, generate variations
- **Access**: `service_provider.get_llm_broker()`

```python
def enhance_description(self, description: str) -> str:
    """Use LLM to enhance image description."""
    llm = self.service_provider.get_llm_broker()
    if llm:
        prompt = f"Enhance this image description for AI generation: {description}"
        return llm.send(prompt)
    return description
```

### Example

```python
class DescribeGenerateImage:
    """
    Tests for the image generation tool plugin
    """
    def should_be_instantiated_with_service_provider(self):
        mock_service_provider = Mock(spec=ServiceProvider)
        mock_gateway = Mock(spec=StableDiffusionGateway)

        tool = GenerateImage(mock_service_provider, mock_gateway)

        assert isinstance(tool, GenerateImage)
        assert tool.service_provider == mock_service_provider
        assert tool.gateway == mock_gateway
```

## Development Workflow

### Local Setup
```bash
pip install -e .[dev]  # Editable install with dev dependencies
```

### Testing Commands
```bash
pytest                    # Run all tests with spec output
python -m build          # Build wheel and source dist
flake8 .                 # Run linting
```

## Integration Points

### Plugin Registration
The tool is auto-discovered via `pyproject.toml` entry points when zk-chat scans for plugins. The `image_generator` key maps to the class.

### External Dependencies
- **PyTorch ecosystem**: `torch`, `torchvision`, `torchaudio` for ML operations
- **Diffusers**: `diffusers`, `transformers`, `accelerate` for Stable Diffusion
- **Support libraries**: `safetensors`, `scipy`, `protobuf`, `sentencepiece`
- **`mojentic`**: Plugin framework providing `LLMTool` base class

### File System Integration
- Uses service provider to access vault configuration
- Saves generated images directly to the vault directory
- Returns markdown-formatted embedding syntax for immediate use

## Release Process

This project follows [Semantic Versioning](https://semver.org/) (SemVer) for version numbering. The version format is MAJOR.MINOR.PATCH, where:

1. MAJOR version increases for incompatible API changes
2. MINOR version increases for backward-compatible functionality additions
3. PATCH version increases for backward-compatible bug fixes

### Preparing a Release

When preparing a release, follow these steps:

1. **Update CHANGELOG.md**:
   - Move items from the "[Next]" section to a new version section
   - Add the new version number and release date: `## [x.y.z] - YYYY-MM-DD`
   - Ensure all changes are properly categorized under "Added", "Changed", "Deprecated", "Removed", "Fixed", or "Security"
   - Keep the empty "[Next]" section at the top for future changes

2. **Update Version Number**:
   - Update the version number in `pyproject.toml`
   - Ensure the version number follows semantic versioning principles based on the nature of changes:
     - **Major Release**: Breaking changes that require users to modify their code
     - **Minor Release**: New features that don't break backward compatibility
     - **Patch Release**: Bug fixes that don't add features or break compatibility

3. **Update Documentation**:
   - Review and update `README.md` to reflect any new features, changed behavior, or updated requirements
   - Update any other documentation files that reference features or behaviors that have changed
   - Ensure installation instructions and examples are up to date

4. **Synchronize Dependencies**:
   - Ensure that dependencies in `pyproject.toml` optional-dependencies match dev requirements
   - Update version constraints if necessary, especially for PyTorch ecosystem packages

5. **Final Verification**:
   - Run all tests to ensure they pass
   - Verify that the plugin works as expected with the updated version
   - Check that all documentation accurately reflects the current state of the project
   - Test image generation functionality if possible

### Release Types

#### Major Releases (x.0.0)

Major releases may include:
- Breaking API changes (eg service provider interface changes)
- Significant architectural changes
- Model version upgrades that change behavior
- Changes that require users to modify their code or workflow

For major releases, consider:
- Providing migration guides
- Updating all documentation thoroughly
- Highlighting breaking changes prominently in the CHANGELOG

#### Minor Releases (0.x.0)

Minor releases may include:
- New image generation features
- Additional model parameters or options
- Non-breaking enhancements
- Deprecation notices (but not removal of deprecated features)
- Performance improvements

For minor releases:
- Document all new features
- Update README to highlight new capabilities
- Ensure backward compatibility

#### Patch Releases (0.0.x)

Patch releases should be limited to:
- Bug fixes
- Security updates
- Performance improvements that don't change behavior
- Documentation corrections
- Dependency updates (unless they change behavior)

For patch releases:
- Clearly describe the issues fixed
- Avoid introducing new features
- Maintain strict backward compatibility

## Common Tasks

### Adding New Features
1. Extend `GenerateImage.run()` method for new parameters
2. Update `descriptor` property for new function parameters
3. Modify `StableDiffusionGateway` if model interaction changes
4. Add corresponding test methods in `DescribeGenerateImage`

### Model Updates
1. Update dependencies in `pyproject.toml` for new model versions
2. Test compatibility with existing functionality
3. Update documentation if model behavior changes

### Publishing
GitHub Actions automatically publishes to PyPI on release creation using trusted publishing (no API keys needed).
````