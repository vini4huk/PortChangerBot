# PortChangerBot

A Telegram bot designed for dynamic management of Apache ports. This bot empowers authorized users to modify the Apache port and review the port change history through simple Telegram commands.

## Features

-   **Secure Apache Port Management:** Facilitates secure modification of Apache ports directly via Telegram.
-   **History Logging:** Maintains a detailed log of all port changes.
-   **Authentication:** Implements authentication via chat IDs to restrict access to authorized users.
-   **Robust Error Handling:** Incorporates error handling to ensure safe and reliable operations.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/vini4huk/PortChangerBot.git](https://github.com/vini4huk/PortChangerBot.git)
    cd PortChangerBot
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**

    Create a `.env` file in the project directory with the following content:

    ```plaintext
    BOT_TOKEN=your_telegram_bot_token
    AUTHORIZED_CHATS=123456789,987654321 # Comma-separated chat IDs
    ```

    Replace `your_telegram_bot_token` with your actual Telegram bot token and `123456789,987654321` with the comma-separated list of authorized chat IDs.

4.  **Run the Bot:**

    ```bash
    python main.py
    ```

## Setting Up as a Linux Service (systemd)

To run the bot as a background service using `systemd`, follow these steps:

1.  **Create a systemd Service File:**

    ```bash
    sudo nano /etc/systemd/system/portchangerbot.service
    ```

2.  **Add Service Configuration:**

    Add the following content to the `portchangerbot.service` file:

    ```ini
    [Unit]
    Description=Apache Port Changer Telegram Bot
    After=network.target

    [Service]
    User=your_username
    WorkingDirectory=/path/to/PortChangerBot
    ExecStart=/usr/bin/python3 /path/to/PortChangerBot/main.py
    Restart=always
    EnvironmentFile=/path/to/PortChangerBot/.env

    [Install]
    WantedBy=multi-user.target
    ```

    Replace `your_username` with your system username and `/path/to/PortChangerBot` with the actual path to your project directory.

3.  **Reload systemd and Enable the Service:**

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable portchangerbot
    sudo systemctl start portchangerbot
    ```

4.  **Check Service Status:**

    ```bash
    sudo systemctl status portchangerbot
    ```

## Usage

-   `/start`: Starts the bot and displays available options.
-   `Change Port`: Generates a new Apache port.
-   `Port History`: Displays the history of port changes.

## License

This project is licensed under the [MIT License](LICENSE).
