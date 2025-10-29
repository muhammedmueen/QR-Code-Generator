
# QR Code Generator with Logo and Gradient

This project generates custom QR codes with logos and gradient effects for batch processing of multiple codes.

## Features

- **Gradient colors** from dark red center (#530a0f) to gray edges (#222020)
- **Logo integration** (18% size) with transparent background support
- **Circular dots** for data modules instead of square pixels
- **Corner eye patterns** with gradient effects
- **Batch processing** for multiple codes
- **High error correction** for reliable scanning

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. **Base Link**: Add your base URL to `links.txt` (first line will be used)
2. **Codes**: Add your codes to `codes.txt` (one per line)
3. **Logo**: Place your logo as `logo.png` (optional)

## Usage

Generate QR codes for all your codes:
```bash
python generate_umr_qr.py
```

This will create QR codes in the `qr_codes/` folder, named after each code (e.g., `CODE1.png`, `CODE2.png`)

## Configuration

### Input Files

- **`links.txt`**: Contains the base URL (first line used)
- **`codes.txt`**: Contains codes to append to base URL (one per line)
- **`logo.png`**: Your logo file (optional, PNG recommended)

### Customization

Edit `generate_umr_qr.py` to customize:

#### Colors
```python
SVG_CENTER = "#530a0f"  # Dark red center
SVG_EDGE = "#222020"    # Dark gray edge
```

#### Logo Size
```python
logo_size = min(qr_width, qr_height) * 18 // 100  # Change 18 to desired %
```

#### Output Folder
```python
OUTPUT_FOLDER = 'qr_codes/'  # Change output directory
```

## Technical Details

- **QR Version**: Auto-fit (starts with version 1)
- **Error Correction**: High (ERROR_CORRECT_H)
- **Module Size**: 15 pixels
- **Border**: 4 modules
- **Logo Size**: 18% of QR code size
- **Logo Clearance**: 20% larger than logo size
- **Output Format**: PNG with 95% quality

## File Structure
```
project/
├── generate_umr_qr.py     # Main QR generator script
├── requirements.txt       # Python dependencies
├── links.txt             # Base URL
├── codes.txt             # Codes to process
├── logo.png              # Logo file (optional)
├── qr_codes/             # Generated QR codes
│   ├── CODE1.png         # QR code for CODE1
│   ├── CODE2.png         # QR code for CODE2
│   └── ...               # More QR codes
└── README.md             # This file
```

## Example

If your `links.txt` contains:
```
https://example.com/redirect?code=
```

And your `codes.txt` contains:
```
ABC123
DEF456
GHI789
```

The script will generate:
- `qr_codes/ABC123.png` → QR code for `https://example.com/redirect?code=ABC123`
- `qr_codes/DEF456.png` → QR code for `https://example.com/redirect?code=DEF456`
- `qr_codes/GHI789.png` → QR code for `https://example.com/redirect?code=GHI789`
=======
# QR-Code-Generator
>>>>>>> 58983094404808e95b87735ab344f31a98da5b90
