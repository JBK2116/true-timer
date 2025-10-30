/*
This file stores the utilities for handling standard-timers
 */
import * as utils from './utils.js';

export class StandardTimer {
    constructor(startTime, endTime, maxSeconds, timezone) {
        this.timezone = timezone;
        this.startTime = startTime;
        this.endTime = endTime;
        this.maxSeconds = maxSeconds;
        this.elapsedSeconds = 0;
        this.pauseCount = 0;
        this.lastPauseTime = null;
        this.isPaused = false;
    }

    initializeWorkTimer() {
        let timerDisplay = document.getElementById("work-timer-display");
        const updateWorkTimer = () => {
            const now = new Date();
            timerDisplay.textContent = utils.createTimeString(now, this.timezone);
            this.elapsedSeconds += 1;
            if (this.elapsedSeconds === this.maxSeconds) {
                this.terminateWorkTimer();
            }
        }
        this.intervalID = setInterval(updateWorkTimer, 1000);
        this.initializeTimerStats();
    }

    pauseWorkTimer() {
        if (this.isPaused === true) {
            return "Timer is already paused!";
        }
        this.lastPauseTime = new Date();
        this.isPaused = true;
        if (this.intervalID !== undefined) {
            clearInterval(this.intervalID);
            this.intervalID = null;
        }
        return "Timer paused..."
    }

    resumeWorkTimer() {
        if (this.isPaused === false) {
            return "Timer is already running!";
        }
        let timerDisplay = document.getElementById("work-timer-display");
        if (this.intervalID !== undefined) {
            clearInterval(this.intervalID);
            this.intervalID = null;
        }
        const resumeWorkTimer = () => {
            const now = new Date();
            timerDisplay.textContent = utils.createTimeString(now, this.timezone);
            this.elapsedSeconds += 1;
            if (this.elapsedSeconds === this.maxSeconds) {
                this.terminateWorkTimer();
            }
        }
        this.intervalID = setInterval(resumeWorkTimer, 1000);
        return "Timer resumed..."

    }

    terminateWorkTimer() {
        if (this.intervalID !== undefined) {
            clearInterval(this.intervalID);
        }
        let timerTitle = document.getElementById("work-timer-title");
        timerTitle.textContent = "Time's UP";
        this.endTime = new Date();
    }
    
    initializeTimerStats() {
        let startTime = document.getElementById("start-time-label");
        let endTime = document.getElementById("end-time-label");
        startTime.textContent = utils.createTimeString(this.startTime, this.timezone);
        endTime.textContent = utils.createTimeString(this.endTime, this.timezone);
        utils.createStatItem("Pause Count", this.pauseCount, "pause-count-label");
        this.pauseCountStatID = "pause-count-label";
    }
}