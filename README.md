# Habitica AutoInviter

Habitica Autoinviter is a Python program that automates inviting users to your Habitica group based on specified criteria. It periodically checks for users looking for a party and invites those who meet the minimum level requirement.

## Features

- Automatically invite users to your Habitica group based on their level.
- Configurable minimum level requirement and delay between invite sessions.
- Logs information about the users invited and the highest level user found.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Student-FastDev/Habitica-AutoInviter
    cd habitica-autoinviter
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Create and edit the configuration file `config.json`. The program will create a default configuration file if it doesn't exist. Update it with your actual Habitica credentials and preferences.

    ```json
    {
        "userAPI": "your-user-api-key",
        "tokenAPI": "your-token-api-key",
        "groupId": "your-group-id",
        "delay": 60,
        "min_level": 10
    }
    ```

    - `userAPI`: Your Habitica user API key.
    - `tokenAPI`: Your Habitica token API key.
    - `groupId`: The ID of your Habitica group.
    - `delay`: Delay in seconds between invite sessions.
    - `min_level`: Minimum level required for users to be invited.

## Usage

Run the Habitica AutoInviter script:

```bash
python invite_bot.py
