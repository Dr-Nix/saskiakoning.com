#!/usr/bin/env python3
"""
Script to identify images in the new website tree that are not referenced by the built site.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote

def find_images_in_directory(directory):
    """Find all image files in a directory tree."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico'}
    images = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                full_path = os.path.join(root, file)
                # Get relative path from the directory
                rel_path = os.path.relpath(full_path, directory)
                images.append(rel_path)
    
    return sorted(images)

def find_image_references_in_built_site(site_directory):
    """Find all image references in HTML and CSS files of the built site."""
    referenced_images = set()
    
    # File extensions to search in
    search_extensions = {'.html', '.css', '.js', '.xml'}
    
    for root, dirs, files in os.walk(site_directory):
        for file in files:
            if Path(file).suffix.lower() in search_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Find image references in various formats
                        patterns = [
                            r'src=["\']([^"\']*\.(?:jpg|jpeg|png|gif|webp|svg|ico))["\']',
                            r'href=["\']([^"\']*\.(?:jpg|jpeg|png|gif|webp|svg|ico))["\']',
                            r'url\(["\']?([^"\']*\.(?:jpg|jpeg|png|gif|webp|svg|ico))["\']?\)',
                            r'background[^:]*:[^;]*url\(["\']?([^"\']*\.(?:jpg|jpeg|png|gif|webp|svg|ico))["\']?\)',
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                # Clean up the path (remove leading slashes, resolve relative paths)
                                clean_path = match.lstrip('/')
                                if clean_path.startswith('assets/'):
                                    # URL decode and normalize the path
                                    normalized_path = normalize_path(clean_path)
                                    referenced_images.add(normalized_path)
                                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return referenced_images

def normalize_path(path):
    """Normalize path for comparison."""
    # URL decode the path to handle spaces and special characters
    decoded_path = unquote(path)
    # Remove any leading slashes and normalize separators
    return decoded_path.replace('\\', '/').lstrip('/')

def main():
    base_dir = Path(__file__).parent
    source_dir = base_dir / 'saskia_nieuw'
    built_site_dir = base_dir / 'saskia_nieuw' / '_site'
    
    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} does not exist")
        return
    
    if not built_site_dir.exists():
        print(f"Error: Built site directory {built_site_dir} does not exist")
        print("Make sure to build the site first with: cd saskia_nieuw && bundle exec jekyll build")
        return
    
    print("Finding all images in source directory...")
    all_images = find_images_in_directory(str(source_dir))
    
    print("Finding image references in built site...")
    referenced_images = find_image_references_in_built_site(str(built_site_dir))
    
    # Normalize paths for comparison
    all_images_normalized = {normalize_path(img): img for img in all_images}
    # referenced_images are already normalized when added
    referenced_images_normalized = referenced_images
    
    # Find unreferenced images
    unreferenced = []
    for normalized_path, original_path in all_images_normalized.items():
        if normalized_path not in referenced_images_normalized:
            # Skip certain directories that might not be directly referenced
            if not any(skip in original_path for skip in ['_site/', '.git/', '__pycache__/']):
                unreferenced.append(original_path)
    
    # Display results
    print(f"\n=== SUMMARY ===")
    print(f"Total images found: {len(all_images)}")
    print(f"Images referenced in built site: {len(referenced_images_normalized)}")
    print(f"Potentially unreferenced images: {len(unreferenced)}")
    
    if unreferenced:
        print(f"\n=== UNREFERENCED IMAGES ===")
        by_directory = defaultdict(list)
        for img in unreferenced:
            directory = os.path.dirname(img)
            by_directory[directory].append(os.path.basename(img))
        
        for directory in sorted(by_directory.keys()):
            print(f"\n{directory}/")
            for filename in sorted(by_directory[directory]):
                print(f"  - {filename}")
    else:
        print("\n✅ All images appear to be referenced!")
    
    # Show some sample referenced images for verification
    print(f"\n=== SAMPLE REFERENCED IMAGES (first 10) ===")
    for img in sorted(list(referenced_images_normalized))[:10]:
        print(f"  - {img}")

if __name__ == "__main__":
    main()