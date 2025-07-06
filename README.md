# Telegram Auto Caption Bot 🤖

Automatically adds formatted captions to files in your Telegram channel using metadata extracted from filenames and file properties.

## Features ✨

- Supports all media types (videos, audio, documents)
- Extracts metadata from filenames
- Customizable caption templates
- PostgreSQL database integration
- Time-based greetings
- Deployable to Render.com

## Variables Available 📝

| Variable       | Description                          | Example                |
|----------------|--------------------------------------|------------------------|
| `{filename}`   | Original filename                   | `Movie.Name.2023.mp4` |
| `{filesize}`   | Human-readable file size            | `1.45 GB`             |
| `{caption}`    | Existing file caption               |                        |
| `{language}`   | Language from filename              | `ENG`                 |
| `{year}`       | Year from filename                  | `2023`                |
| `{quality}`    | Quality from filename               | `1080p`               |
| `{season}`     | Season number                       | `S02`                 |
| `{episode}`    | Episode number                      | `E05`                 |
| `{duration}`   | Video duration                      | `1:45:23`             |
| `{height}`     | Video height in pixels              | `1080`                |
| `{width}`      | Video width in pixels               | `1920`                |
| `{ext}`        | File extension                      | `MP4`                 |
| `{resolution}` | Video resolution                    | `1920x1080`           |
| `{mime_type}`  | File MIME type                      | `video/mp4`           |
| `{title}`      | Audio title                         | `Song Name`           |
| `{artist}`     | Audio artist                        | `Artist Name`         |
| `{wish}`       | Time-based greeting                 | `Good Evening`        |

## Deployment 🚀

### Prerequisites

- Python 3.9+
- Telegram API credentials
- Render.com account
- PostgreSQL database

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/auto-caption-bot.git
cd auto-caption-bot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python bot.py
