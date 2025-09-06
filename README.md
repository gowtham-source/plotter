# Telegram Plotting Bot

A Telegram bot that executes Python plotting code and returns the generated images. The bot is designed to be deployed on a server using Docker.

## Features

- Execute Python code with matplotlib to generate plots
- Automatically use Times New Roman font for all plots
- Secure sandbox environment for code execution
- Support for multiple plots in a single code snippet
- Error handling with user-friendly messages

## Prerequisites

- Docker installed on your server
- A Telegram Bot Token (obtained from BotFather)

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

### Font Issues

If plots are not using Times New Roman font:

1. Check the Docker build logs for any font installation errors
2. Verify that the font path in the code matches the actual path in the container
3. You may need to modify the Dockerfile to use a different method for installing the font

### Bot Not Responding

If the bot is not responding:

1. Check the container logs for errors
2. Verify that the bot token is correct
3. Ensure the container has internet access
4. Restart the container

## License

This project is licensed under the MIT License - see the LICENSE file for details.