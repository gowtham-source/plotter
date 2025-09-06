# Telegram Plotting Bot

A Telegram bot that executes Python plotting code and returns the generated images. The bot is designed to be deployed on a server using Docker.

## Features

- Execute Python code with matplotlib to generate plots
- Automatically use Times New Roman font for all plots
- Secure sandbox environment for code execution
- Support for multiple plots in a single code snippet
- Error handling with user-friendly messages

## Prerequisites

- **Docker Desktop** installed on your system ([Download here](https://www.docker.com/products/docker-desktop/))
- A Telegram Bot Token (obtained from BotFather)
- Git (for cloning the repository)

**Note**: If you don't have Docker installed, you can also run the bot directly with Python (see Alternative Setup section below).

## Setup and Deployment

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send `/newbot`
3. Follow the instructions to create a new bot
4. Once created, BotFather will provide you with a token. Save this token for later use.

### 2. Clone the Repository

```bash
git clone <repository-url>
cd plotter
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory with the following content:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

Replace `your_telegram_bot_token_here` with the token you received from BotFather.

### 4. Build and Run with Docker

#### Build the Docker Image

```bash
docker build -t telegram-plotting-bot .
```

#### Run the Docker Container

```bash
docker run -d --name plotting-bot --env-file .env telegram-plotting-bot
```

### 5. Verify the Bot is Running

Check the container logs to ensure the bot started correctly:

```bash
docker logs plotting-bot
```

You should see output indicating that the bot is running and connected to the Telegram API.

### 6. Test the Bot

Open Telegram and search for your bot by the username you provided during setup. Start a chat and send the `/start` command to verify it's working.

## Usage

Send Python code that creates matplotlib plots to the bot. The code should be enclosed in triple backticks (\`\`\`) and include `plt.show()` to display the plots.

Example:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Wave')
plt.show()
```

The bot will execute the code and send back the generated plot as an image.

### Testing the Plotting Functionality

A test script is included to verify that the plotting functionality works correctly. This script creates three different types of plots using the Times New Roman font:

1. A radar chart comparing different models
2. A grouped bar plot showing metric values
3. A bubble chart visualizing relationships between metrics

To run the test script:

```bash
python test_plot.py
```

This will generate three PNG files in the current directory that you can examine to verify the plotting functionality.

## Alternative Setup (Without Docker)

If you prefer to run the bot directly with Python instead of using Docker:

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd plotter
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file with your bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

5. **Run the bot**:
   ```bash
   python bot.py
   ```

**Note**: When running without Docker, the bot will use system fonts. Times New Roman may not be available, so the bot will fall back to available serif fonts.

## Server Maintenance

### Updating the Bot

To update the bot with new code:

```bash
# Pull the latest code
git pull

# Rebuild the Docker image
docker build -t telegram-plotting-bot .

# Stop and remove the old container
docker stop plotting-bot
docker rm plotting-bot

# Run a new container with the updated image
docker run -d --name plotting-bot --env-file .env telegram-plotting-bot
```

### Viewing Logs

To view the bot's logs:

```bash
docker logs plotting-bot
```

For continuous log monitoring:

```bash
docker logs -f plotting-bot
```

### Restarting the Bot

If you need to restart the bot:

```bash
docker restart plotting-bot
```

## Security Considerations

- The bot runs user code in a restricted sandbox environment
- Only specific modules are allowed to be imported
- Dangerous functions and operations are blocked
- File system access is limited to temporary directories

## Troubleshooting

### Docker Installation Issues
If you get "docker command not found" error:
- Install Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running
- Restart your terminal after installation
- On Windows, you may need to enable WSL2

### Font Issues
If plots are not using Times New Roman font:
- **With Docker**: The bot uses Liberation Serif as a fallback, which provides similar appearance
- **Without Docker**: The bot will use system fonts; install Times New Roman on your system if needed
- Check the logs for font configuration messages
- The bot will automatically fall back to available serif fonts

### Bot Not Responding
If the bot is not responding:
- **With Docker**: Check container logs with `docker logs plotting-bot`
- **Without Docker**: Check the terminal output for error messages
- Verify that the bot token is correct in your `.env` file
- Ensure your system has internet access
- Try restarting the bot

## License

This project is licensed under the MIT License - see the LICENSE file for details.