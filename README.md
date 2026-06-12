# docshokage

Scan a Django project, extract relevant files (views, models, serializers, urls), and send them to a hosted backend for API documentation generation.

## Installation

```bash
pip install docshokage
```

## Usage

```bash
# Save your API key (first time only)
docshokage --kagi <your-api-key>

# Run the pipeline
docshokage arise

# With custom options
docshokage arise --input-dir ./my-project --api-url https://your-backend.com
```

## How it works

1. **Scan** — walks through your project directory, collecting all text files
2. **Filter** — keeps only relevant files (views, models, serializers, urls)
3. **Send** — POSTs the structured data to your hosted backend
