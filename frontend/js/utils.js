/*
This files stores util functions used throughout the frontend
 */

/**
 * Gets the IANA String from the user's browser.
 * @example - If the user is in Toronto, IANA String = America/Toronto
 *
 * @returns {string} - User's `IANA String` if successful, else default to `UTC`
 */
export function getUserIANAString() {
    try {
        return Intl.DateTimeFormat().resolvedOptions().timeZone;
    } catch (err) {
        console.log(`Error retrieving user timezone. Defaulting to: UTC`);
        console.log(`Error: ${err}`);
    }
}

/** Creates the notification modal using the provided message.
 * @param {string} message Message to set in the modal
 */
function createNotification(message) {
    let notificationModal = document.getElementById("notification-modal");
    let messageBody = document.getElementById("notification-message");
    if (!notificationModal || !messageBody) {
        return null;
    }
    messageBody.textContent = message;
    return notificationModal;
}

/** Displays the notification modal using the provided message and for the provided duration
 * @param {string} message Message to display
 * @param {number} duration Duration to display modal (Seconds)
 */
export function showNotificationDynamic(message, duration) {
    let notificationModal = createNotification(message);
    if (!notificationModal) {
        console.log("No notification modal found");
        return;
    }
    notificationModal.classList.add("modal--show");
    setTimeout(() => {
        notificationModal.classList.remove("modal--show");
    }, duration * 1000)
}

/** Displays the notification modal using the provided message.
 * Notification modal remains displayed until close button is clicked on it.
 * @param {string} message Message to display
 */
export function showNotificationStatic(message) {
    let notificationModal = createNotification(message);
    if (!notificationModal) {
        console.log("No notification modal found");
        return;
    }
    notificationModal.classList.add("modal--show");
}

/**
 * Initializes all necessary components of the frontend
 * @param {string} IANATimezone
 */
export function setPage(IANATimezone) {
    // NOTIFICATION MODAL EVENT HANDLER
    let notificationModal = document.getElementById("notification-modal");
    let closeButton = notificationModal.querySelector(".modal__close");
    closeButton.addEventListener("click", function (event) {
        notificationModal.classList.remove("modal--show");
    })
    // CURRENT TIME DISPLAY
    let currentTimeDisplay = document.getElementById("current-time-display");
    function updatePageTime() {
        const now = new Date();
        currentTimeDisplay.textContent = formatClockTime(now, IANATimezone);
    }
    updatePageTime();
    setInterval(updatePageTime, 1000);
}

/** Creates the event handlers for the timer buttons
 * @param {StandardTimer} timer Timer object for the session
 */
export function setTimerButtons(timer) {
    // Start Button
    let startBtn = document.getElementById("start-button");
    startBtn.addEventListener("click", () => timer.startTimer())
    
    // Toggle Pause Button
    let togglePauseBtn = document.getElementById("toggle-pause-button");
    togglePauseBtn.disabled = false;
    togglePauseBtn.addEventListener("click", () => timer.togglePause());
    // End Button
    let endBtn = document.getElementById("end-button");
    endBtn.disabled = false;
    endBtn.addEventListener("click", () => timer.end());
    // Reset Button
    let resetBtn = document.getElementById("reset-button");
    resetBtn.addEventListener("click", () => timer.reset());
}

/**
 * Formats a Date object as HH:MM:SS in 24-hour format
 * @param {Date} time - Date object to format
 * @param {string} IANATimezone - IANA timezone string (e.g., 'America/New_York')
 * @returns {string} Time string in HH:MM:SS format
 */
export function formatClockTime(time, IANATimezone) {
    return time.toLocaleTimeString("en-US", {
        timeZone: IANATimezone,
        hour12: false,   // 24-hour format
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}

/**
 * Formats seconds as HH:MM:SS duration
 * @param {number} seconds - Total seconds elapsed
 * @returns {string} Duration string in HH:MM:SS format
 */
export function formatDuration(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Calculates and formats remaining time as HH:MM:SS
 * @param {number} elapsedSeconds - Seconds already elapsed
 * @param {number} maxSeconds - Total duration in seconds
 * @returns {string} Remaining time in HH:MM:SS format (minimum 00:00:00)
 */
export function formatRemainingTime(elapsedSeconds, maxSeconds) {
    const remaining = Math.max(0, maxSeconds - elapsedSeconds);
    const hrs = Math.floor(remaining / 3600);
    const mins = Math.floor((remaining % 3600) / 60);
    const secs = remaining % 60;
    return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/** Creates a `stats__item` to display
 * @param {string} name Name of the stat item
 * @param {number|string} value Value of the stat item
 * @param {string} id - ID to assign to the stat item value
 * @returns span - DOM element
 */
export function createStatItem(name, value, id) {
    let parent = document.getElementById("timer-stats");
    let container = document.createElement("div");
    container.classList.add("stats__item");
    let statLabel = document.createElement("span");
    statLabel.classList.add("stats__label");
    statLabel.textContent = name;
    let statValue = document.createElement("span");
    statValue.classList.add("stats__value");
    statValue.id = id;
    statValue.textContent = value;
    container.append(statLabel, statValue);
    parent.appendChild(container);
    return statValue;
}

