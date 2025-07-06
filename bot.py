import os
import re
import math
import datetime
import psycopg2
from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Dict, Optional

# Configuration
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
DATABASE_URL = os.getenv("DATABASE_URL")
CAPTION_TEMPLATE = os.getenv("CAPTION_TEMPLATE", """
🎬 {title} ({year}) | {quality} {resolution}
🌍 {language} | ⏳ {duration} | 📁 {ext}
👤 {artist} | {wish}!
""")

# Database connection
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# Initialize the bot
app = Client("auto_caption_bot", 
             api_id=API_ID, 
             api_hash=API_HASH, 
             bot_token=BOT_TOKEN)

def get_wish() -> str:
    """Get time-based greeting"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12: return "Good Morning"
    if 12 <= hour < 17: return "Good Afternoon"
    if 17 <= hour < 21: return "Good Evening"
    return "Good Night"

def parse_filename(filename: str) -> Dict[str, str]:
    """Extract metadata from filename"""
    metadata = {
        'language': 'Unknown',
        'year': str(datetime.datetime.now().year),
        'quality': 'HD',
        'season': '01',
        'episode': '01',
        'ext': os.path.splitext(filename)[1][1:].upper(),
        'artist': 'Unknown',
        'title': os.path.splitext(filename)[0],
        'resolution': '1920x1080'
    }
    
    patterns = [
        (r'\[(\d{4})\]', 'year'),
        (r'(\d{3,4}p)', 'resolution'),
        (r'(S\d{2})', 'season'),
        (r'(E\d{2})', 'episode'),
        (r'(720p|1080p|2160p|4K|HD|SD)', 'quality'),
        (r'\[([A-Za-z]+)\]', 'language'),
        (r'-(.+?)-', 'artist'),
        (r'^(.+?)\s*[\[\(]', 'title')
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            metadata[key] = match.group(1)
    
    return metadata

def format_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    if size_bytes == 0: return "0B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f"{round(size_bytes / p, 2)} {units[i]}"

def get_video_metadata(file_path: str) -> Dict[str, str]:
    """Extract video metadata using ffprobe"""
    try:
        import ffmpeg
        probe = ffmpeg.probe(file_path)
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        return {
            'duration': str(datetime.timedelta(seconds=float(video_stream['duration'])) if video_stream else 'N/A',
            'height': str(video_stream.get('height', 'N/A')),
            'width': str(video_stream.get('width', 'N/A')),
            'resolution': f"{video_stream.get('width', 'N/A')}x{video_stream.get('height', 'N/A')}" if video_stream else 'N/A',
            'mime_type': probe['format'].get('format_name', 'N/A') if 'format' in probe else 'N/A'
        }
    except Exception as e:
        print(f"Metadata extraction error: {e}")
        return {}

def save_to_db(message_id: int, metadata: dict):
    """Save caption data to PostgreSQL"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO captions (message_id, filename, filesize, caption_data)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (message_id) DO UPDATE SET
            filename = EXCLUDED.filename,
            filesize = EXCLUDED.filesize,
            caption_data = EXCLUDED.caption_data
        """, (message_id, metadata.get('filename'), metadata.get('filesize'), str(metadata)))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn: conn.close()

@app.on_message(filters.chat(CHANNEL_ID) & (filters.video | filters.audio | filters.document))
async def auto_caption(client: Client, message: Message):
    """Process channel posts and add captions"""
    file_path = None
    try:
        if message.video or message.audio or message.document:
            file_path = await message.download()
            filename = os.path.basename(file_path)
            filesize = os.path.getsize(file_path)
            
            metadata = parse_filename(filename)
            metadata.update({
                'filename': filename,
                'filesize': format_size(filesize),
                'wish': get_wish(),
                'caption': message.caption or ''
            })
            
            if message.video:
                metadata.update({
                    'duration': str(datetime.timedelta(seconds=message.video.duration)),
                    'height': str(message.video.height),
                    'width': str(message.video.width),
                    'resolution': f"{message.video.width}x{message.video.height}",
                    'mime_type': message.video.mime_type
                })
                # Additional metadata from file
                metadata.update(get_video_metadata(file_path))
            
            # Apply caption template
            caption = CAPTION_TEMPLATE.format(**metadata)
            await message.edit_caption(caption)
            
            # Save to database
            save_to_db(message.id, metadata)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    # Create database table if not exists
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS captions (
                message_id BIGINT PRIMARY KEY,
                filename TEXT,
                filesize TEXT,
                caption_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Database setup error: {e}")
    finally:
        if conn: conn.close()
    
    print("Auto Caption Bot is running...")
    app.run()
