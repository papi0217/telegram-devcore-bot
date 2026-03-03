# DevCore Telegram Bot

DevCore is an adaptive engineering mentor Telegram bot designed to help users improve their software engineering skills across various domains. It provides personalized guidance, tracks progress, and offers interactive learning experiences.

## Features

-   **Adaptive Learning System**: Tracks user progress, identifies weak areas, and adjusts difficulty.
-   **Socratic Teaching Protocol**: Guides users with questions instead of direct answers.
-   **Spaced Repetition Engine**: Schedules review prompts for concepts learned.
-   **Live Code Execution Sandbox**: Safely executes Python and JavaScript code snippets.
-   **Precision Context Injection**: Personalizes OpenAI API calls with user-specific context.
-   **Anti-Passivity Enforcement**: Encourages active participation and engagement.
-   **Interview Simulation Mode**: Simulates technical interviews for various roles and levels.

## Installation

### Prerequisites

-   Python 3.x
-   Kali Linux (recommended environment)
-   Telegram account
-   OpenAI API Key or xAI API Key

### Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/papi0217/telegram-devcore-bot.git
    cd telegram-devcore-bot
    ```

2.  **Run the setup script:**

    This script will create a Python virtual environment, install all necessary dependencies, and initialize the SQLite database.

    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

3.  **Set environment variables:**

    Obtain your Telegram Bot Token from BotFather on Telegram and your OpenAI API Key from the OpenAI platform (or xAI API Key from xAI).

    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    export OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # Or XAI_API_KEY
    export AI_PROVIDER="openai" # Set to 'xai' if using xAI
    ```

    It is recommended to add these lines to your `~/.bashrc` or `~/.profile` to set them persistently.

4.  **Run the bot:**

    ```bash
    chmod +x run.sh
    ./run.sh
    ```

    This script will keep the bot running in the background and restart it automatically if it crashes.

## Usage

Interact with the bot on Telegram using the following commands:

-   `/start`: Onboarding and skill assessment.
-   `/learn [topic]`: Start a lesson on a specified topic.
-   `/quiz [topic]`: Start a quiz on a specified topic.
-   `/debug [code]`: Analyze and debug submitted code snippet.
-   `/review [code]`: Code review with improvement suggestions.
-   `/design [system]`: System design walkthrough.
-   `/progress`: Show full learning progress report.
-   `/weakareas`: List topics needing improvement.
-   `/challenge`: Random coding challenge scaled to user level.
-   `/explain [concept]`: Explain at beginner/intermediate/advanced level.
-   `/due`: Show all concepts due for review today (spaced repetition).
-   `/run [code]`: Execute code in sandboxed environment and return result.
-   `/interview [role] [level]`: Simulate a full technical interview session.
-   `/help`: Full command list with descriptions.

## File Structure

```
/telegram-devcore-bot/
├── bot.py                  # Main bot entry point
├── config.py               # API keys, config variables
├── database.py             # SQLite schema + CRUD operations
├── scheduler.py            # APScheduler for spaced repetition reminders
├── handlers/
│   ├── commands.py         # All /command handlers
│   ├── quiz.py             # Quiz logic and grading
│   ├── adaptive.py         # Adaptive learning engine
│   ├── ai_engine.py        # OpenAI API integration layer
│   ├── code_runner.py      # Sandboxed code execution
│   └── interview.py        # Interview simulation engine
├── prompts/
│   └── system_prompt.py    # DevCore persona system prompt
├── memory/
│   └── context_builder.py  # Context window optimizer
├── requirements.txt        # All dependencies
├── run.sh                  # One-command persistent launcher
├── setup.sh                # Setup script for virtual environment and dependencies
└── README.md               # Setup and usage guide
```

## Error Handling & Security

-   Robust error handling with logging for API calls and user input.
-   API keys loaded from environment variables only.
-   User input sanitized before database writes.
-   Sandboxed code execution to prevent malicious operations.

## Persistence

-   The `run.sh` script ensures the bot restarts automatically upon crashes, maintaining continuous operation.

## Contributing

Contributions are welcome! Please refer to the project's guidelines for more information.

## License

This project is licensed under the MIT License.
