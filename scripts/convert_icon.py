#!/usr/bin/env python3
"""
Convert SVG to ICO format for Windows application icon
"""

import os
import sys
from PIL import Image
import subprocess


def svg_to_png(svg_path: str, png_path: str, size: int) -> bool:
    """Convert SVG to PNG using Inkscape or rsvg-convert"""
    try:
        # Try Inkscape first
        subprocess.run(
            [
                "inkscape",
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={size}",
                f"--export-height={size}",
                svg_path,
            ],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try rsvg-convert
            with open(png_path, "wb") as f:
                subprocess.run(
                    ["rsvg-convert", "-w", str(size), "-h", str(size), svg_path],
                    check=True,
                    stdout=f,
                )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Neither Inkscape nor rsvg-convert found")
            print("Please install Inkscape or librsvg2-bin")
            return False


def png_to_png(png_path: str, output_path: str, size: int) -> bool:
    """Convert PNG to PNG with specific size using PIL"""
    try:
        with Image.open(png_path) as img:
            # Resize image to target size
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_img.save(output_path, "PNG")
            return True
    except Exception as e:
        print(f"Error converting PNG: {e}")
        return False


def jpg_to_png(jpg_path: str, output_path: str, size: int) -> bool:
    """Convert JPG/JPEG to PNG with specific size using PIL"""
    try:
        with Image.open(jpg_path) as img:
            # Convert to RGBA if needed (for transparency support)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            # Resize image to target size
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_img.save(output_path, "PNG")
            return True
    except Exception as e:
        print(f"Error converting JPG: {e}")
        return False


def convert_to_png(input_path: str, output_path: str, size: int) -> bool:
    """Convert input file (SVG, PNG, or JPG) to PNG with specific size"""
    if input_path.lower().endswith(".svg"):
        return svg_to_png(input_path, output_path, size)
    elif input_path.lower().endswith(".png"):
        return png_to_png(input_path, output_path, size)
    elif input_path.lower().endswith((".jpg", ".jpeg")):
        return jpg_to_png(input_path, output_path, size)
    else:
        print(f"Unsupported file format: {input_path}")
        return False


def create_ico_from_pngs(png_files: list[str], ico_path: str) -> None:
    """Create ICO file from multiple PNG files using a manual approach"""
    # Sort files by size to ensure proper order
    png_files.sort(key=lambda f: int(f.split("_")[-1].split(".")[0]))

    # Load all images and ensure they're in RGBA format
    images = []
    sizes = []
    for png_file in png_files:
        img = Image.open(png_file)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        images.append(img)
        sizes.append(img.size[0])

    # Create ICO file manually by concatenating individual ICO files
    # This is a workaround for PIL's limited multi-size ICO support

    # First, try the standard method
    try:
        # Use the largest image as it's most likely to be used
        largest_img = images[-1]  # Last image should be the largest due to sorting
        largest_img.save(ico_path, format="ICO")
        print(
            f"Created ICO with largest size: {largest_img.size[0]}x{largest_img.size[1]}"
        )
        print(
            "Note: PIL has limited multi-size ICO support. For better multi-size support, consider using a dedicated ICO library."
        )
    except Exception as e:
        print(f"Error creating ICO: {e}")
        return

    # For better multi-size support, we could use external tools like ImageMagick
    # But for now, we'll create a single-size ICO with the largest image


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    # Check for SVG, PNG, and JPG input files
    svg_path = os.path.join(project_dir, "resources/icons/app_icon.svg")
    png_path = os.path.join(project_dir, "resources/icons/app_icon.png")
    jpg_path = os.path.join(project_dir, "resources/icons/app_icon.jpg")
    jpeg_path = os.path.join(project_dir, "resources/icons/app_icon.jpeg")
    ico_path = os.path.join(project_dir, "resources/icons/app_icon.ico")

    # Determine input file with priority: SVG > PNG > JPG/JPEG
    input_path = None
    if os.path.exists(svg_path):
        input_path = svg_path
    elif os.path.exists(png_path):
        input_path = png_path
    elif os.path.exists(jpg_path):
        input_path = jpg_path
    elif os.path.exists(jpeg_path):
        input_path = jpeg_path
    else:
        print(
            "Error: No supported icon file found (app_icon.svg, app_icon.png, app_icon.jpg, or app_icon.jpeg)"
        )
        return 1

    # Check if ICO file already exists and is newer than input
    if os.path.exists(ico_path):
        input_mtime = os.path.getmtime(input_path)
        ico_mtime = os.path.getmtime(ico_path)
        if ico_mtime >= input_mtime:
            print(f"ICO file already exists and is up-to-date: {ico_path}")
            return 0

    print(f"Converting {input_path} to {ico_path}")

    # Sizes needed for ICO file
    sizes = [16, 32, 48, 64, 128, 256]
    png_files: list[str] = []

    # Convert input file to PNG for each size
    for size in sizes:
        png_path = os.path.join(project_dir, f"resources/icons/app_icon_{size}.png")
        if convert_to_png(input_path, png_path, size):
            png_files.append(png_path)
            print(f"Created {png_path}")
        else:
            print(f"Failed to create {png_path}")
            return 1

    # Create ICO file
    create_ico_from_pngs(png_files, ico_path)
    print(f"Created {ico_path}")

    # Clean up temporary PNG files
    for png_file in png_files:
        os.remove(png_file)
        print(f"Removed temporary file {png_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
