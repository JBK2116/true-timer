/*
This file stores the utilities for handling standard-timers
 */
import * as utils from './utils.js';

export class StandardTimer {
    constructor(startTime, endTime, maxSeconds, timezone) {
        // values for time calculations
        this.timezone = timezone;
        this.startTime = startTime;
        this.endTime = endTime;
        this.maxSeconds = maxSeconds;
        this.elapsedSeconds = 0;
        this.pauseCount = 0;
        this.totalPausedMs = 0;
        this.lastPauseTime = null;
        this.isPaused = false;
        // dom elements
        this.timerDisplay = document.getElementById("work-timer-display");
        this.startButton = document.getElementById("start-button");
        this.pauseButton = document.getElementById("toggle-pause-button");
        this.endButton = document.getElementById("end-button");
    }

    /**
     * Sets the timer up to be started
     */
    setTimer() {
        this.timerDisplay.textContent = "Ready To Begin";
        this.setTimerStats();
    }
    
    /**
     * Starts the timer session and sets all required statistics starting values
     */
    startTimer() {
        this.startButton.style.display = "none";
        this.update(this.timerDisplay);
        this.intervalID = setInterval(() => this.update(this.timerDisplay), 1000);
    }

    /**
     * Handles pausing and resuming the timer
     */
    togglePause() {
        if (this.isPaused) {
            // resume the timer
            this.totalPausedMs += new Date() - this.lastPauseTime;
            this.endTime = new Date(this.startTime.getTime() + (this.maxSeconds * 1000) + this.totalPausedMs);
            this.isPaused = false;
            this.pauseButton.textContent = "Pause";
            this.update(this.timerDisplay);
            this.intervalID = setInterval(() => this.update(this.timerDisplay), 1000);
        } else {
            // pause the timer
            this.lastPauseTime = new Date();
            this.pauseCount++;
            this.isPaused = true;
            this.pauseCountLabel.textContent = this.pauseCount;
            this.pauseButton.textContent = "Resume";
            if (this.intervalID) {
                clearInterval(this.intervalID);
                this.intervalID = null;
            }
        }
    }

    /**
     * Ends the timer session
     */
    end() {
        // clear out any remaining interval IDs
        if (this.intervalID !== undefined) {
            clearInterval(this.intervalID);
        }
        // alert user
        let timerTitle = document.getElementById("work-timer-title");
        timerTitle.textContent = "Time's UP";
        this.endTime = new Date();
        // disable buttons
        this.pauseButton.disabled = true;
        this.endButton.disabled = true;
    }

    /**
     * Increments the timer appropriately every second
     *
     * Updates the timer display and remaining time display
     */
    update() {
        const now = new Date();
        this.elapsedSeconds = Math.floor(((now - this.startTime - this.totalPausedMs)) / 1000);
        this.timerDisplay.textContent = utils.formatDuration(this.elapsedSeconds);
        this.remainingTimeLabel.textContent = utils.formatRemainingTime(this.elapsedSeconds, this.maxSeconds);
        if (this.elapsedSeconds >= this.maxSeconds) {
            this.end();
        }
    }

    /**
     * Sets all starting timer statistic labels for the session.
     *
     * Saves the DOM elements as attributes for the object
     */
    setTimerStats() {
        // start-time & pause-time label
        this.startTimeLabel = document.getElementById("start-time-label");
        this.endTimeLabel = document.getElementById("end-time-label");
        this.startTimeLabel.textContent = utils.formatClockTime(this.startTime, this.timezone)
        this.endTimeLabel.textContent = utils.formatClockTime(this.endTime, this.timezone);
        // pause count
        this.pauseCountLabel = utils.createStatItem("Pause Count", this.pauseCount, "pause-count-label");
        // remaining time
        this.remainingTimeLabel = utils.createStatItem("Remaining Time", utils.formatRemainingTime(this.elapsedSeconds,this.maxSeconds), "remaining-time-label");
    }
}