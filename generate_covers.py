#!/usr/bin/env python3
"""
Album Cover Generator for "Mutually Assured Distraction" by Younger Brother
Creates 3 concept variations with iconic, geometric, design-led aesthetics
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Constants
SIZE = 3000
CENTER = SIZE // 2

# Color palettes
COLORS = {
    'concept1': {
        'bg': '#0a0a0f',
        'primary': '#00d4ff',
        'secondary': '#ff3366',
        'accent': '#ffffff'
    },
    'concept2': {
        'bg': '#0f0f14',
        'primary': '#ffffff',
        'secondary': '#ff6b35',
        'accent': '#00ff88'
    },
    'concept3': {
        'bg': '#050508',
        'primary': '#ffcc00',
        'secondary': '#ff0066',
        'accent': '#ffffff'
    }
}


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_text(draw, img, band_name, album_title, colors, font_size_band=120, font_size_album=80, y_offset=0):
    """Draw band name and album title with clean typography"""
    # Try to use a clean sans-serif font, fallback to default
    try:
        font_band = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_band)
        font_album = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size_album)
    except:
        try:
            font_band = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size_band)
            font_album = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font_size_album)
        except:
            font_band = ImageFont.load_default()
            font_album = ImageFont.load_default()

    # Band name at top
    band_bbox = draw.textbbox((0, 0), band_name, font=font_band)
    band_width = band_bbox[2] - band_bbox[0]
    band_x = (SIZE - band_width) // 2
    band_y = 180 + y_offset

    # Draw with subtle letter spacing effect
    draw.text((band_x, band_y), band_name, fill=hex_to_rgb(colors['accent']), font=font_band)

    # Album title at bottom
    album_bbox = draw.textbbox((0, 0), album_title, font=font_album)
    album_width = album_bbox[2] - album_bbox[0]
    album_x = (SIZE - album_width) // 2
    album_y = SIZE - 280 + y_offset

    draw.text((album_x, album_y), album_title, fill=hex_to_rgb(colors['accent']), font=font_album)


def concept1_split_focus():
    """
    Concept 1: SPLIT FOCUS
    Two large opposing circles representing dual attention/distraction
    With interference patterns between them suggesting fragmented focus
    """
    colors = COLORS['concept1']
    img = Image.new('RGBA', (SIZE, SIZE), hex_to_rgb(colors['bg']) + (255,))
    draw = ImageDraw.Draw(img)

    # Two opposing circles (like eyes or radar dishes)
    circle_radius = 550
    circle_y = CENTER
    left_circle_x = CENTER - 450
    right_circle_x = CENTER + 450

    # Draw outer rings for left circle (cyan)
    for i in range(5, 0, -1):
        r = circle_radius - (i * 60)
        if r > 0:
            alpha = int(255 * (1 - i * 0.15))
            ring_color = hex_to_rgb(colors['primary'])
            # Draw ring
            draw.ellipse(
                [left_circle_x - r, circle_y - r, left_circle_x + r, circle_y + r],
                outline=ring_color + (alpha,),
                width=8
            )

    # Draw outer rings for right circle (magenta/red)
    for i in range(5, 0, -1):
        r = circle_radius - (i * 60)
        if r > 0:
            alpha = int(255 * (1 - i * 0.15))
            ring_color = hex_to_rgb(colors['secondary'])
            draw.ellipse(
                [right_circle_x - r, circle_y - r, right_circle_x + r, circle_y + r],
                outline=ring_color + (alpha,),
                width=8
            )

    # Draw fragmented lines between the circles (interference/distraction)
    num_lines = 25
    for i in range(num_lines):
        y = CENTER - 400 + (i * 32)
        # Create broken/fragmented line segments
        x_start = left_circle_x + 200
        x_end = right_circle_x - 200

        segment_length = (x_end - x_start) // 8
        for j in range(8):
            if (i + j) % 3 != 0:  # Create gaps for fragmentation effect
                seg_x1 = x_start + j * segment_length
                seg_x2 = seg_x1 + segment_length - 20

                # Gradient from cyan to magenta
                ratio = j / 7
                r = int(hex_to_rgb(colors['primary'])[0] * (1-ratio) + hex_to_rgb(colors['secondary'])[0] * ratio)
                g = int(hex_to_rgb(colors['primary'])[1] * (1-ratio) + hex_to_rgb(colors['secondary'])[1] * ratio)
                b = int(hex_to_rgb(colors['primary'])[2] * (1-ratio) + hex_to_rgb(colors['secondary'])[2] * ratio)

                alpha = int(180 * (1 - abs(i - num_lines//2) / (num_lines//2) * 0.7))
                draw.line([(seg_x1, y), (seg_x2, y)], fill=(r, g, b, alpha), width=3)

    # Draw center cores of circles
    core_radius = 80
    draw.ellipse(
        [left_circle_x - core_radius, circle_y - core_radius,
         left_circle_x + core_radius, circle_y + core_radius],
        fill=hex_to_rgb(colors['primary']) + (255,)
    )
    draw.ellipse(
        [right_circle_x - core_radius, circle_y - core_radius,
         right_circle_x + core_radius, circle_y + core_radius],
        fill=hex_to_rgb(colors['secondary']) + (255,)
    )

    # Add typography
    draw_text(draw, img, "YOUNGER BROTHER", "MUTUALLY ASSURED DISTRACTION", colors)

    return img


def concept2_fractured_prism():
    """
    Concept 2: FRACTURED PRISM
    A bold triangle (like Dark Side of the Moon) but shattered into fragments
    representing the breaking/fracturing of attention
    """
    colors = COLORS['concept2']
    img = Image.new('RGBA', (SIZE, SIZE), hex_to_rgb(colors['bg']) + (255,))
    draw = ImageDraw.Draw(img)

    # Main triangle parameters
    tri_size = 1400
    tri_top = (CENTER, CENTER - tri_size // 2 - 100)
    tri_left = (CENTER - tri_size // 2, CENTER + tri_size // 3)
    tri_right = (CENTER + tri_size // 2, CENTER + tri_size // 3)

    # Draw the main triangle outline
    draw.polygon([tri_top, tri_left, tri_right], outline=hex_to_rgb(colors['primary']), width=6)

    # Create fracture lines from center
    fracture_center = (CENTER, CENTER - 50)
    num_fractures = 12

    for i in range(num_fractures):
        angle = (i / num_fractures) * 2 * math.pi - math.pi / 2
        length = 600 + (i % 3) * 150

        end_x = fracture_center[0] + math.cos(angle) * length
        end_y = fracture_center[1] + math.sin(angle) * length

        # Draw fracture line
        if i % 2 == 0:
            color = hex_to_rgb(colors['secondary'])
        else:
            color = hex_to_rgb(colors['accent'])

        # Fragmented fracture lines
        segments = 5
        for s in range(segments):
            if s % 2 == 0:
                s_start = s / segments
                s_end = (s + 0.7) / segments
                sx1 = fracture_center[0] + math.cos(angle) * length * s_start
                sy1 = fracture_center[1] + math.sin(angle) * length * s_start
                sx2 = fracture_center[0] + math.cos(angle) * length * s_end
                sy2 = fracture_center[1] + math.sin(angle) * length * s_end
                draw.line([(sx1, sy1), (sx2, sy2)], fill=color + (200,), width=4)

    # Draw scattered geometric fragments
    fragments = [
        # Small triangles scattered around
        [(CENTER - 300, CENTER - 200), (CENTER - 250, CENTER - 280), (CENTER - 200, CENTER - 220)],
        [(CENTER + 280, CENTER - 180), (CENTER + 350, CENTER - 200), (CENTER + 320, CENTER - 130)],
        [(CENTER - 100, CENTER + 200), (CENTER - 50, CENTER + 280), (CENTER + 20, CENTER + 220)],
        [(CENTER + 150, CENTER + 180), (CENTER + 220, CENTER + 250), (CENTER + 250, CENTER + 160)],
        [(CENTER - 400, CENTER + 50), (CENTER - 350, CENTER + 120), (CENTER - 320, CENTER + 30)],
    ]

    fragment_colors = [colors['secondary'], colors['accent'], colors['secondary'], colors['accent'], colors['secondary']]

    for frag, col in zip(fragments, fragment_colors):
        draw.polygon(frag, outline=hex_to_rgb(col), width=3)

    # Central impact point
    impact_radius = 40
    draw.ellipse(
        [fracture_center[0] - impact_radius, fracture_center[1] - impact_radius,
         fracture_center[0] + impact_radius, fracture_center[1] + impact_radius],
        fill=hex_to_rgb(colors['secondary']) + (255,)
    )

    # Inner glow ring
    for r in range(3):
        ring_r = impact_radius + 20 + r * 25
        alpha = 150 - r * 40
        draw.ellipse(
            [fracture_center[0] - ring_r, fracture_center[1] - ring_r,
             fracture_center[0] + ring_r, fracture_center[1] + ring_r],
            outline=hex_to_rgb(colors['accent']) + (alpha,),
            width=2
        )

    # Add typography
    draw_text(draw, img, "YOUNGER BROTHER", "MUTUALLY ASSURED DISTRACTION", colors, y_offset=50)

    return img


def concept3_opposing_forces():
    """
    Concept 3: OPPOSING FORCES
    Two bold arrows/chevrons pointing at each other but fragmenting before impact
    representing the tension of mutually assured destruction/distraction
    """
    colors = COLORS['concept3']
    img = Image.new('RGBA', (SIZE, SIZE), hex_to_rgb(colors['bg']) + (255,))
    draw = ImageDraw.Draw(img)

    # Arrow/chevron parameters
    arrow_width = 400
    arrow_height = 800
    gap = 200  # Gap between arrows at center

    # Left arrow (pointing right) - Gold
    left_tip = (CENTER - gap // 2, CENTER)
    left_top = (CENTER - gap // 2 - arrow_width, CENTER - arrow_height // 2)
    left_bottom = (CENTER - gap // 2 - arrow_width, CENTER + arrow_height // 2)
    left_inner_top = (CENTER - gap // 2 - 150, CENTER - arrow_height // 3)
    left_inner_bottom = (CENTER - gap // 2 - 150, CENTER + arrow_height // 3)

    # Draw left arrow as outline chevron
    left_chevron = [
        left_top,
        left_tip,
        left_bottom,
        left_inner_bottom,
        (CENTER - gap // 2 - 280, CENTER),
        left_inner_top
    ]
    draw.polygon(left_chevron, outline=hex_to_rgb(colors['primary']), width=8)

    # Right arrow (pointing left) - Magenta
    right_tip = (CENTER + gap // 2, CENTER)
    right_top = (CENTER + gap // 2 + arrow_width, CENTER - arrow_height // 2)
    right_bottom = (CENTER + gap // 2 + arrow_width, CENTER + arrow_height // 2)
    right_inner_top = (CENTER + gap // 2 + 150, CENTER - arrow_height // 3)
    right_inner_bottom = (CENTER + gap // 2 + 150, CENTER + arrow_height // 3)

    right_chevron = [
        right_top,
        right_tip,
        right_bottom,
        right_inner_bottom,
        (CENTER + gap // 2 + 280, CENTER),
        right_inner_top
    ]
    draw.polygon(right_chevron, outline=hex_to_rgb(colors['secondary']), width=8)

    # Draw fragmentation particles in the gap
    num_particles = 40
    for i in range(num_particles):
        # Random-ish distribution in the gap area
        px = CENTER + ((i * 17) % gap) - gap // 2
        py = CENTER + ((i * 31) % 600) - 300

        # Particle size varies
        size = 5 + (i % 8) * 3

        # Alternate colors
        if i % 3 == 0:
            p_color = hex_to_rgb(colors['primary'])
        elif i % 3 == 1:
            p_color = hex_to_rgb(colors['secondary'])
        else:
            p_color = hex_to_rgb(colors['accent'])

        alpha = 100 + (i % 10) * 15

        # Draw as small squares for geometric feel
        draw.rectangle(
            [px - size, py - size, px + size, py + size],
            fill=p_color + (alpha,),
            outline=None
        )

    # Add horizontal lines emanating from impact point
    for i in range(-8, 9):
        if i == 0:
            continue
        y = CENTER + i * 35

        # Left side lines (gold fading)
        for seg in range(5):
            x_start = CENTER - gap // 2 - 50 - seg * 80
            x_end = x_start - 50
            alpha = 200 - seg * 35
            if alpha > 0:
                draw.line([(x_start, y), (x_end, y)],
                         fill=hex_to_rgb(colors['primary']) + (alpha,), width=2)

        # Right side lines (magenta fading)
        for seg in range(5):
            x_start = CENTER + gap // 2 + 50 + seg * 80
            x_end = x_start + 50
            alpha = 200 - seg * 35
            if alpha > 0:
                draw.line([(x_start, y), (x_end, y)],
                         fill=hex_to_rgb(colors['secondary']) + (alpha,), width=2)

    # Central tension point - bright white
    tension_size = 30
    draw.ellipse(
        [CENTER - tension_size, CENTER - tension_size,
         CENTER + tension_size, CENTER + tension_size],
        fill=hex_to_rgb(colors['accent']) + (255,)
    )

    # Outer glow rings
    for r in range(4):
        ring_r = tension_size + 15 + r * 20
        alpha = 180 - r * 40
        draw.ellipse(
            [CENTER - ring_r, CENTER - ring_r,
             CENTER + ring_r, CENTER + ring_r],
            outline=hex_to_rgb(colors['accent']) + (alpha,),
            width=2
        )

    # Add typography
    draw_text(draw, img, "YOUNGER BROTHER", "MUTUALLY ASSURED DISTRACTION", colors)

    return img


def create_transparent_version(img):
    """Create a version with transparent background"""
    # Get the background color from top-left pixel
    bg_color = img.getpixel((0, 0))[:3]

    # Create new image with transparency
    trans_img = img.copy()
    datas = trans_img.getdata()

    new_data = []
    tolerance = 15
    for item in datas:
        # If pixel is close to background color, make it transparent
        if (abs(item[0] - bg_color[0]) < tolerance and
            abs(item[1] - bg_color[1]) < tolerance and
            abs(item[2] - bg_color[2]) < tolerance):
            new_data.append((item[0], item[1], item[2], 0))
        else:
            new_data.append(item)

    trans_img.putdata(new_data)
    return trans_img


def main():
    """Generate all album cover concepts"""
    output_dir = "/home/user/yb-album-cover/output"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating album covers for 'Mutually Assured Distraction' by Younger Brother")
    print("=" * 70)

    # Generate Concept 1
    print("\n[1/3] Creating Concept 1: Split Focus...")
    concept1 = concept1_split_focus()
    concept1.save(os.path.join(output_dir, "concept1_split_focus.png"), "PNG")
    trans1 = create_transparent_version(concept1)
    trans1.save(os.path.join(output_dir, "concept1_split_focus_transparent.png"), "PNG")
    print("      Saved: concept1_split_focus.png")

    # Generate Concept 2
    print("\n[2/3] Creating Concept 2: Fractured Prism...")
    concept2 = concept2_fractured_prism()
    concept2.save(os.path.join(output_dir, "concept2_fractured_prism.png"), "PNG")
    trans2 = create_transparent_version(concept2)
    trans2.save(os.path.join(output_dir, "concept2_fractured_prism_transparent.png"), "PNG")
    print("      Saved: concept2_fractured_prism.png")

    # Generate Concept 3
    print("\n[3/3] Creating Concept 3: Opposing Forces...")
    concept3 = concept3_opposing_forces()
    concept3.save(os.path.join(output_dir, "concept3_opposing_forces.png"), "PNG")
    trans3 = create_transparent_version(concept3)
    trans3.save(os.path.join(output_dir, "concept3_opposing_forces_transparent.png"), "PNG")
    print("      Saved: concept3_opposing_forces.png")

    print("\n" + "=" * 70)
    print("All covers generated successfully!")
    print(f"Output directory: {output_dir}")
    print("\nFiles created:")
    for f in sorted(os.listdir(output_dir)):
        filepath = os.path.join(output_dir, f)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  - {f} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
