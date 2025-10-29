# Frontend Structure

This `README.md` documents the structure and organization of the application's frontend.

## TL;DR

A **timer web application** designed for efficient lock-in periods, supporting multiple timer modes for focused productivity.

## Description

The frontend is organized into directories by file type to keep everything **modular, reusable, and easy to navigate** as the project scales.

### Core Components

1. **`index.html`** — The single entry point of this *SPA* (Single Page Application).

    * Located in the root directory.
    * Should remain lightweight and reference all required JS/CSS assets.

2. **`css/`** — Contains all stylesheet files.

    * Initially includes `style.css`.
    * May expand as the UI grows.

3. **`js/`** — Contains all JavaScript files, structured with an **object-oriented approach**.

    * Each file encapsulates logic for a specific timer or core functionality.

---

### JS Folder

#### Required Files

1. **`app.js`** — Entry point for the frontend.

    * Manages app flow (errors, notifications, state).
    * Imports and uses modules from other JS files.

2. **`standard-timer.js`** — Implements the `standardTimer` object.

3. **`pomodoro-timer.js`** — Implements the `pomodoroTimer` object.

4. **`fiftyTwoSeventeen-timer.js`** — Implements the `fiftyTwoSeventeenTimer` object.

    * Handles all logic for 52/17 interval cycles.

5. **`deep-session-timer.js`** — Implements the `deepSessionTimer` object.

6. **`utils.js`** — Contains shared utility functions used throughout the frontend.