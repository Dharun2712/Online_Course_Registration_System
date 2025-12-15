"""
Generate placeholder course images with course titles
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create course_images directory if it doesn't exist
os.makedirs('static/course_images', exist_ok=True)

# Course configurations with colors matching the images you showed
courses = [
    {
        'filename': 'datamining.jpg',
        'title': 'DATA\nMINING',
        'bg_color': '#6B4EE6',
        'text_color': '#FFFFFF'
    },
    {
        'filename': 'ooad.jpg',
        'title': 'OBJECT ORIENTED\nPROGRAMMING',
        'bg_color': '#00C4B4',
        'text_color': '#FFFFFF'
    },
    {
        'filename': 'data-structure.jpg',
        'title': 'Data Structures\n& Algorithms',
        'bg_color': '#6B8CFF',
        'text_color': '#FFFFFF'
    },
    {
        'filename': 'data-analysis-with-pandas.jpg',
        'title': 'Learn\nData Analysis\nwith Pandas',
        'bg_color': '#1E2A47',
        'text_color': '#FFFFFF'
    },
    {
        'filename': 'web-development-with-flask.jpg',
        'title': 'Flask Web\nDevelopment',
        'bg_color': '#000000',
        'text_color': '#00D9FF'
    },
    {
        'filename': 'test-course-advanced-javascript.jpg',
        'title': 'Master\nJavaScript',
        'bg_color': '#F9F5E3',
        'text_color': '#1a1a1a'
    },
    {
        'filename': 'introduction-to-python.jpg',
        'title': 'INTRODUCTION\nTO PYTHON',
        'bg_color': '#4AC4D4',
        'text_color': '#FFFFFF'
    }
]

for course in courses:
    # Create image
    img = Image.new('RGB', (600, 320), color=course['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Get text size and position
    text = course['title']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((600 - text_width) // 2, (320 - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill=course['text_color'], font=font)
    
    # Save image
    filepath = os.path.join('static', 'course_images', course['filename'])
    img.save(filepath, 'JPEG', quality=95)
    print(f"Created: {filepath}")

print("\nAll course images created successfully!")
