"""QR Code Generator with Logo and Gradient"""

import qrcode
from PIL import Image, ImageDraw
import os
import math

# Configuration
LINKS_FILE = 'links.txt'
CODES_FILE = 'codes.txt'
OUTPUT_FOLDER = 'qr_codes/'
LOGO_PATH = 'logo.png'

# Colors
SVG_CENTER = "#530a0f"
SVG_EDGE = "#222020"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(color1, color2, factor):
    """Interpolate between two colors"""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    
    return (r, g, b)

def create_working_qr(data):
    """Create QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    return qr

def apply_working_gradient(qr_image):
    """Apply gradient to QR code"""
    if qr_image.mode != 'RGB':
        qr_image = qr_image.convert('RGB')
    
    width, height = qr_image.size
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2
    
    result = Image.new('RGB', (width, height), (255, 255, 255))
    qr_pixels = qr_image.load()
    result_pixels = result.load()
    
    for y in range(height):
        for x in range(width):
            if qr_pixels[x, y][0] < 128:
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                factor = min(distance / max_radius, 1.0)
                color = interpolate_color(SVG_CENTER, SVG_EDGE, factor)
                result_pixels[x, y] = color
            else:
                result_pixels[x, y] = (255, 255, 255)
    
    return result

def is_corner_eye_area(x, y, qr_size, module_size, border_size):
    """Check if position is in a corner eye (finder pattern) area"""
    # Calculate module position in QR matrix
    module_x = (x - border_size) // module_size
    module_y = (y - border_size) // module_size
    
    # Calculate QR matrix size
    matrix_modules = (qr_size - 2 * border_size) // module_size
    
    # Corner eye areas are 7x7 modules in each corner
    # Top-left corner
    if 0 <= module_x < 7 and 0 <= module_y < 7:
        return True
    # Top-right corner
    if matrix_modules - 7 <= module_x < matrix_modules and 0 <= module_y < 7:
        return True
    # Bottom-left corner
    if 0 <= module_x < 7 and matrix_modules - 7 <= module_y < matrix_modules:
        return True
    
    return False

def draw_corner_eyes(draw, qr_size, module_size, border_size, gradient_center_x, gradient_center_y, max_radius):
    """Draw corner eyes (finder patterns) like traditional QR codes"""
    # Calculate QR matrix size
    matrix_modules = (qr_size - 2 * border_size) // module_size
    
    # Corner positions (top-left of each 7x7 area)
    corners = [
        (0, 0),  # Top-left
        (matrix_modules - 7, 0),  # Top-right
        (0, matrix_modules - 7),  # Bottom-left
    ]
    
    for corner_module_x, corner_module_y in corners:
        # Convert to pixel coordinates
        corner_x = border_size + corner_module_x * module_size
        corner_y = border_size + corner_module_y * module_size
        
        # Calculate gradient colors for corner eye parts
        outer_size = 7 * module_size
        corner_radius = module_size // 3
        
        # Outer square gradient color
        outer_center_x = corner_x + outer_size // 2
        outer_center_y = corner_y + outer_size // 2
        outer_distance = math.sqrt((outer_center_x - gradient_center_x)**2 + (outer_center_y - gradient_center_y)**2)
        outer_factor = min(outer_distance / max_radius, 1.0)
        outer_color = interpolate_color(SVG_CENTER, SVG_EDGE, outer_factor)
        
        # Draw outer square
        draw.rounded_rectangle([
            corner_x, corner_y,
            corner_x + outer_size, corner_y + outer_size
        ], radius=corner_radius, fill=outer_color)
        
        # Draw inner white square
        inner_margin = module_size
        inner_size = 5 * module_size
        draw.rounded_rectangle([
            corner_x + inner_margin, corner_y + inner_margin,
            corner_x + inner_margin + inner_size, corner_y + inner_margin + inner_size
        ], radius=corner_radius, fill=(255, 255, 255))
        
        # Center square gradient color
        center_margin = 2 * module_size
        center_size = 3 * module_size
        center_center_x = corner_x + center_margin + center_size // 2
        center_center_y = corner_y + center_margin + center_size // 2
        center_distance = math.sqrt((center_center_x - gradient_center_x)**2 + (center_center_y - gradient_center_y)**2)
        center_factor = min(center_distance / max_radius, 1.0)
        center_color = interpolate_color(SVG_CENTER, SVG_EDGE, center_factor)
        
        # Draw center circle
        center_circle_x = corner_x + center_margin + center_size // 2
        center_circle_y = corner_y + center_margin + center_size // 2
        center_radius = center_size // 2
        draw.ellipse([
            center_circle_x - center_radius, center_circle_y - center_radius,
            center_circle_x + center_radius, center_circle_y + center_radius
        ], fill=center_color)

def create_minimal_logo_clearance(qr_image):
    """Create QR with logo clearance and corner eyes"""
    if qr_image.mode != 'RGB':
        qr_image = qr_image.convert('RGB')
    
    width, height = qr_image.size
    center_x, center_y = width // 2, height // 2
    module_size = 15
    border_size = 4 * module_size  # Standard QR border
    
    # Logo clearance parameters
    logo_size = min(width, height) * 18 // 100
    bg_size = int(logo_size * 1.2)
    clearance_radius = bg_size // 2
    
    # Create result image
    result = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(result)
    original_pixels = qr_image.load()
    
    # Calculate gradient parameters for corner eyes
    max_radius = min(width, height) // 2
    
    # Draw corner eyes first
    draw_corner_eyes(draw, width, module_size, border_size, center_x, center_y, max_radius)
    
    # Draw circles for data modules, skipping corner eyes and logo area
    for y in range(0, height, module_size):
        for x in range(0, width, module_size):
            if x + module_size <= width and y + module_size <= height:
                module_center_x = x + module_size // 2
                module_center_y = y + module_size // 2
                
                # Skip corner eye areas
                if is_corner_eye_area(x, y, width, module_size, border_size):
                    continue
                
                # Check distance from center for logo clearance
                distance_from_center = math.sqrt(
                    (module_center_x - center_x)**2 + (module_center_y - center_y)**2
                )
                
                # Skip if in clearance area
                if distance_from_center < clearance_radius:
                    continue
                
                if module_center_x < width and module_center_y < height:
                    pixel_color = original_pixels[module_center_x, module_center_y]
                    
                    if pixel_color[0] < 200 or pixel_color[1] < 200 or pixel_color[2] < 200:
                        radius = int(module_size * 0.95 / 2)
                        draw.ellipse([
                            module_center_x - radius, module_center_y - radius,
                            module_center_x + radius, module_center_y + radius
                        ], fill=pixel_color)
    
    return result

def add_clean_logo(qr_image, logo_path):
    """Add transparent logo directly on QR code"""
    if not os.path.exists(logo_path):
        return qr_image
    
    try:
        logo = Image.open(logo_path)
        qr_width, qr_height = qr_image.size
        
        # Logo size
        logo_size = min(qr_width, qr_height) * 18 // 100
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Center logo on QR code
        result = qr_image.copy()
        center_x = qr_width // 2
        center_y = qr_height // 2
        logo_position = (center_x - logo.size[0] // 2, center_y - logo.size[1] // 2)
        
        # Paste logo with transparency support
        if logo.mode == 'RGBA':
            result.paste(logo, logo_position, logo)
        else:
            result.paste(logo, logo_position)
        
        return result
        
    except Exception as e:
        print(f"Could not add logo: {e}")
        return qr_image

def create_final_qr(data):
    """Create the final QR code"""
    
    # Create base
    qr = create_working_qr(data)
    base_img = qr.make_image(fill_color='black', back_color='white')
    
    # Apply gradient
    gradient_img = apply_working_gradient(base_img)
    
    # Create with minimal clearance
    cleared_img = create_minimal_logo_clearance(gradient_img)
    
    # Add clean logo
    if os.path.exists(LOGO_PATH):
        final_img = add_clean_logo(cleared_img, LOGO_PATH)
    else:
        final_img = cleared_img
    
    return final_img

def main():
    """Generate QR codes for base link + codes combination"""
    print("QR Code Generator")
    print("=" * 20)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Read base link
    try:
        with open(LINKS_FILE, 'r') as f:
            base_links = f.read().splitlines()
    except FileNotFoundError:
        print(f"❌ Error: '{LINKS_FILE}' not found.")
        return
    
    if not base_links:
        print(f"❌ Error: No base link found in '{LINKS_FILE}'.")
        return
    
    base_link = base_links[0].strip()  # Use first line as base link
    if not base_link:
        print(f"❌ Error: Base link is empty in '{LINKS_FILE}'.")
        return
    
    # Read codes
    try:
        with open(CODES_FILE, 'r') as f:
            codes = f.read().splitlines()
    except FileNotFoundError:
        print(f"❌ Error: '{CODES_FILE}' not found.")
        return
    
    if not codes:
        print(f"❌ Error: No codes found in '{CODES_FILE}'.")
        return
    
    # Filter out empty codes
    codes = [code.strip() for code in codes if code.strip()]
    
    logo_status = "with logo" if os.path.exists(LOGO_PATH) else "without logo"
    print(f"Base Link: {base_link}")
    print(f"Processing {len(codes)} codes {logo_status}")
    print()
    
    for i, code in enumerate(codes):
        # Combine base link with code
        full_link = base_link + code
        
        print(f"Creating QR code {i+1}/{len(codes)} for code: {code}")
        
        # Create the QR code
        final_qr = create_final_qr(full_link)
        filename = f"{OUTPUT_FOLDER}{code}.png"
        final_qr.save(filename, 'PNG', quality=95)
        print(f"Saved: {filename}")
        
        if (i + 1) % 10 == 0:
            print(f"Progress: {i+1}/{len(codes)} completed")
        
        print()
    
    print("QR code generation complete!")
    print(f"{len(codes)} QR codes saved in {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()