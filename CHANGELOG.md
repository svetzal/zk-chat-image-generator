# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-26

### Changed
- **Breaking**: Migrated to new zk-chat service provider architecture
- Constructor now accepts `service_provider` parameter instead of `vault` and `llm` parameters
- Updated to use `service_provider.get_config()` to access vault path
- Renamed package from `zk-rag-image-generator` to `zk-chat-image-generator`
- Updated mojentic dependency to `>=0.6.1` for compatibility with new plugin architecture
- Plugin now inherits directly from `LLMTool` using service provider pattern

### Migration Notes
- Existing installations should uninstall the old `zk-rag-image-generator` package and install `zk-chat-image-generator`
- Plugin functionality remains the same but uses the new extensible service provider interface

## [1.1.0] - 2024-03-09

### Changed
- **Breaking**: GenerateImage class now requires LLMBroker parameter in constructor
- Updated test suite to accommodate new LLMBroker requirement

## [1.0.0] - 2024-01-09

### Added
- Initial release of the zk-rag-image-generator plugin
- GenerateImage tool for creating images using Stable Diffusion 3.5 Medium model
- Integration with mojentic LLM tools framework
- Basic error handling and gateway pattern implementation
- Support for PNG image generation and saving
- Comprehensive test suite and development guidelines
