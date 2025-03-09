## Development Setup
1. Install Python 3.11 or higher
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
- Tests are co-located with implementation files (test file must be in the same folder as the implementation)
- Run tests: `pytest`
- Linting: `flake8 src`
- Code style:
  - Max line length: 127
  - Max complexity: 10
  - Follow numpy docstring style

### Testing Best Practices
- Use pytest for testing, with mocker if you require mocking
- Do not use unittest or MagicMock directly, use it through the mocker wrapper
- Use @fixture markers for pytest fixtures
- Break up fixtures into smaller fixtures if they are too large
- Do not write Given/When/Then or Act/Arrange/Assert comments
- Separate test phases with a single blank line
- Do not write conditional statements in tests
- Each test must fail for only one clear reason
- "Don't Mock what you don't own" only write mocks for our own gateway classes, do not mock other library internals or
  even private functions or methods in our own code.
- Don't test gateway classes, only test the code that uses the gateway classes

## Best Practices
1. Follow the existing project structure
2. Write tests for new functionality
3. Document using numpy-style docstrings
4. Keep code complexity low
5. Use type hints for all functions and methods
6. Co-locate tests with implementation
7. Favor declarative code styles over imperative code styles
8. Use pydantic (not @dataclass) for data objects with strong types
9. Favor list and dictionary comprehensions over for loops
