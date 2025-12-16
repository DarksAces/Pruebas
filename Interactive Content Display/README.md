# Interactive Content Display

Application for managing and displaying interactive content on screens, built with Electron.

## Features

- **Content Management**: Display interactive HTML/Web content.
- **Configurable**: Settings managed via `InteractiveContentDisplay.json`.
- **Inactivity Handling**: Automatically detects idle user state.
- **Session Restoration**: Remembers the last used configuration.
- **Window Management**: optimized for kiosk/display usage.

## Installation

1.  Ensure you have Node.js installed.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

### Development
Run the application in development mode:
```bash
npm start
```

### Build
Build the application for Windows:
```bash
npm run build:win
```

## Configuration

The application uses `InteractiveContentDisplay.json` for configuration.
- **Location**: `resources/InteractiveContentDisplay.json` (in production) or `config/` (in dev).
- **Key Settings**:
    - `logFilePath`: Path to store application logs.
    - Content sources and display settings.

## Project Structure

- `JavaScript/`: Core logic (Main process, Window Manager, Config Manager).
- `html/`: Renderer process and UI.
- `media_content/`: Assets for the display.