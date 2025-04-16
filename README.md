# Markdown to LaTeX Converter (mdtotex)

A Python tool for converting Markdown documents to LaTeX format, specifically optimized for academic and technical writing with proper math equation support.

## Features

- Converts Markdown to LaTeX while preserving:
  - Headers and sections
  - Math expressions (both inline `$...$` and display `\[...\]`)
  - Text formatting (bold, italics)
  - Horizontal rules (`---` to `\hrulefill`)
- Handles complex mathematical content
- Lightweight and fast

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mdtotex.git
cd mdtotex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv (faster):
```bash
uv pip install -r requirements.txt
```

## Usage

Basic conversion:
```bash
python md2tex.py input.md output.tex
```

Example:
```bash
python md2tex.py paper.md paper.tex
```

## Development

To install in development mode:
```bash
uv pip install -e .
```

## License

MIT

