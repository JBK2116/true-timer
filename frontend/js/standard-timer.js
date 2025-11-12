/*
This file stores the utilities for handling standard-timers
 */

import * as utils from './utils.js';
import {showNotificationDynamic, showNotificationStatic} from './utils.js';

export class StandardTimer {
    constructor(timerID, userID, timezone, maxSeconds) {
        // attributes for identification calculations
        this.userID = userID; // cached in local storage
        this.timerID = timerID; // received from backend
        this.timezone = timezone; // received from user's browser

        // attributes for timer tracking (all synced from backend)
        this.startTime = null; // created from Date.now()
        this.endTime = null; // calculated from startTime + maxSeconds
        this.maxSeconds = maxSeconds; // max seconds for timer

        // attributes for tracking timer state (backend is source of truth)
        this.elapsedSeconds = 0;
        this.pauseCount = 0;
        this.totalPausedMs = 0;
        this.lastPauseTime = null;
        this.isPaused = false;

        // dom elements
        this.timerTitle = document.getElementById("work-timer-title"); // default text: Work Session
        this.timerDisplay = document.getElementById("work-timer-display"); // default text: 00:00:00
        this.remainingTimeDisplay = document.getElementById("remaining-time-overlay"); // default text: 00:00:00
        this.startButton = document.getElementById("start-button"); // default state: visible + disabled
        this.pauseButton = document.getElementById("toggle-pause-button"); // default state: visible + disabled + "pause"
        this.endButton = document.getElementById("end-button"); // default state: visible + disabled
        this.resetButton = document.getElementById("reset-button"); // default state: hidden + disabled

        // interval tracking
        this.timerIntervalID = null;
    }

    /**
     * Sets the timer up to be started
     */
    async setTimer() {
        // 1. showcase user that we are ready to begin
        this.timerDisplay.textContent = "Ready To Begin";
        // 2. initialize the start button
        this.startButton.disabled = false;
        // 3. remove previous event handler on this btn
        const newBtn = this.startButton.cloneNode(true);
        this.startButton.replaceWith(newBtn);
        this.startButton = newBtn;
        // 4. notify backend of starting timer
        this.startButton.addEventListener("click", async () => {
            try {
                const response = await fetch(`${utils.ENDPOINTS.STANDARD_TIMER.START}/${this.timerID}`, {
                    method: "POST", headers: {"Content-Type": "application/json", "X-User-ID": this.userID},
                });
                const data = await response.json();
                if (response.ok) {
                    // sync timer state from backend
                    this.maxSeconds = data.minutes * 60;
                    this.elapsedSeconds = data.elapsed_seconds || 0;
                    this.totalPausedMs = (data.total_paused_seconds || 0) * 1000; // convert to ms
                    this.lastPauseTime = data.last_pause_time ? new Date(data.last_pause_time) : null;
                    this.startTime = new Date(data.start_time);
                    this.startTimeString = data.start_time_string;
                    this.estimatedEndTimeString = data.estimated_end_time_string;
                    this.pauseCount = data.total_pause_count || 0;
                    this.isPaused = data.is_paused || false;
                    await this.startTimer();
                } else {
                    showNotificationDynamic(data.message || "Failed to start timer", 5000);
                }
            } catch (error) {
                console.error("Error starting timer:", error);
                showNotificationDynamic("Network error - failed to start timer", 5000);
            }
        });

        // 5. setup reset button
        const newResetBtn = this.resetButton.cloneNode(true);
        this.resetButton.replaceWith(newResetBtn);
        this.resetButton = newResetBtn;
        this.resetButton.addEventListener("click", () => {
            this.reset();
        });
    }

    /**
     * Starts the timer session and sets all required statistics starting values
     */
    async startTimer() {
        // 1. disable and hide start button
        this.startButton.disabled = true;
        this.startButton.style.display = "none";

        // 2. enable reset button
        this.resetButton.disabled = false;
        this.resetButton.style.display = "flex";

        // 3. disable preset cards to prevent state mismanagement
        utils.disablePresetCards();

        // 4. initialize the toggle-pause button and remove any previous event handlers on it
        const newBtn = this.pauseButton.cloneNode(true);
        this.pauseButton.replaceWith(newBtn);
        this.pauseButton = newBtn;
        this.pauseButton.disabled = false;
        this.pauseButton.addEventListener("click", async () => {
            await this.togglePause();
        });

        // 5. initialize the statistics
        document.getElementById("start-time-label").textContent = this.startTimeString;
        document.getElementById("end-time-label").textContent = this.estimatedEndTimeString;
        this.pauseCountLabel = utils.createStatItem("Pause Count", this.pauseCount, "pause-count-label");

        // 6. start the visual timer display
        this.timerTitle.textContent = "Timer In Progress";
        await this.update();
        this.timerIntervalID = setInterval(() => this.update(), 1000);
    }

    /**
     * Handles pausing and resuming the timer
     */
    async togglePause() {
        try {
            if (this.isPaused) {
                // RESUME THE TIMER
                // 1. notify backend of resuming
                const response = await fetch(`${utils.ENDPOINTS.STANDARD_TIMER.RESUME}/${this.timerID}`, {
                    method: "POST", headers: {"Content-Type": "application/json", "X-User-ID": this.userID},
                });
                const data = await response.json();

                if (!response.ok) {
                    showNotificationStatic(data.message || "Failed to resume timer");
                    return;
                }

                // 2. sync state from backend response
                this.totalPausedMs = (data.total_paused_seconds || 0) * 1000;
                this.lastPauseTime = null; // reset it
                this.isPaused = false;

                // 3. update UI
                this.pauseButton.textContent = "Pause";
                await this.update();
                this.timerIntervalID = setInterval(() => this.update(), 1000);

            } else {
                // PAUSE THE TIMER
                // 1. notify backend of pause
                const response = await fetch(`${utils.ENDPOINTS.STANDARD_TIMER.PAUSE}/${this.timerID}`, {
                    method: "POST", headers: {"Content-Type": "application/json", "X-User-ID": this.userID},
                });
                const data = await response.json();

                if (!response.ok) {
                    showNotificationStatic(data.message || "Failed to pause timer");
                    return;
                }

                // 2. sync state from backend response
                this.lastPauseTime = new Date(data.last_pause_time);
                this.pauseCount = data.total_pause_count;
                this.isPaused = true;

                // 3. update UI
                this.pauseCountLabel.textContent = this.pauseCount;
                this.pauseButton.textContent = "Resume";

                // 4. stop the interval
                if (this.timerIntervalID) {
                    clearInterval(this.timerIntervalID);
                    this.timerIntervalID = null;
                }
            }
        } catch (error) {
            console.error("Error toggling pause:", error);
            showNotificationStatic("Network error - failed to toggle pause");
        }
    }

    /**
     * Ends the timer session
     */
    async end() {
        try {
            // 1. notify backend of timer completion
            const response = await fetch(`${utils.ENDPOINTS.STANDARD_TIMER.END}/${this.timerID}`, {
                method: "POST", headers: {"Content-Type": "application/json", "X-User-ID": this.userID},
            });

            if (!response.ok) {
                const data = await response.json();
                showNotificationStatic(data.message || "Failed to end timer");
            }
        } catch (error) {
            console.error("Error ending timer:", error);
            // Continue with UI updates even if backend call fails
        }

        // 2. clear out any remaining interval IDs
        if (this.timerIntervalID) {
            clearInterval(this.timerIntervalID);
            this.timerIntervalID = null;
        }

        // 3. update UI
        this.timerTitle.textContent = "Session Complete";
        this.pauseButton.disabled = true;
        this.endButton.disabled = true;
        this.resetButton.style.display = "flex";
    }

    /**
     * Increments the timer appropriately every second
     *
     * Updates the timer display and remaining time display
     */
    async update() {
        const now = new Date();
        this.elapsedSeconds = Math.floor((now - this.startTime - this.totalPausedMs) / 1000);
        this.timerDisplay.textContent = utils.formatDuration(this.elapsedSeconds);
        this.remainingTimeDisplay.textContent = utils.formatRemainingTime(this.elapsedSeconds, this.maxSeconds);

        // check if timer has completed
        if (this.elapsedSeconds >= this.maxSeconds) {
            await this.end();
        }
    }

    /**
     * Resets the page according to the timer display
     */
    reset() {
        // 1. clear interval
        if (this.timerIntervalID) {
            clearInterval(this.timerIntervalID);
            this.timerIntervalID = null;
        }

        // 2. reset main display
        this.timerTitle.textContent = "Work Session";
        this.timerDisplay.textContent = "00:00:00";

        // 3. reset start button
        this.startButton.style.display = "flex";
        this.startButton.disabled = true;

        // 4. reset pause button
        this.pauseButton.disabled = true;
        this.pauseButton.textContent = "Pause";

        // 5. reset end button
        this.endButton.disabled = true;

        // 6. reset "reset" button
        this.resetButton.style.display = "none";
        this.resetButton.disabled = true;

        // 7. reset main stats
        const startTimeLabel = document.getElementById("start-time-label");
        const endTimeLabel = document.getElementById("end-time-label");
        if (startTimeLabel) startTimeLabel.textContent = "--:--:--";
        if (endTimeLabel) endTimeLabel.textContent = "--:--:--";
        this.remainingTimeDisplay.textContent = "00:00:00";

        // 8. remove dynamically added stats
        if (this.pauseCountLabel) this.pauseCountLabel.remove();

        // 9. enable preset card selections
        utils.enablePresetCards();
    }
}