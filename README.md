Here's the Telegram Bot Command section you can add to your `README.md`:

## Bot Commands 🤖

### Admin Commands (for channel owners)
| Command | Description | Example |
|---------|-------------|---------|
| `/setcaption <template>` | Set custom caption template | `/setcaption {title} [{year}] - {quality}` |
| `/getcaption` | Show current caption template | `/getcaption` |
| `/stats` | Show bot statistics | `/stats` |
| `/export` | Export caption database | `/export` |
| `/restart` | Restart the bot (admin only) | `/restart` |

### User Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/variables` | List all available caption variables | `/variables` |
| `/preview` | Preview how caption will look | `/preview Movie.Name.2023.1080p.mp4` |
| `/help` | Show help message | `/help` |

### How to Use Commands
1. Add the bot to your channel as admin
2. Use commands in channel or private chat with bot
3. For template commands, use the available variables

Example of setting a custom template:
```bash
/setcaption 🎬 {title} ({year})
🌟 {quality} | {resolution} 
⏰ {duration} | 📁 {filesize}
{wish}! Enjoy your content!
```

### Automatic Functionality
- Automatically processes all new media in channel
- No command needed for auto-captioning
- Edits existing captions if template changes

Note: Admin commands require bot admin privileges in your channel.
