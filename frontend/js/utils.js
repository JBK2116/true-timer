/*
This files stores util functions used throughout the frontend
 */

/**
 * Purpose: Gets the IANA String from the user's browser.
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

/** Purpose: Displays the notification modal using the provided message and for the provided duration
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

/** Purpose: Displays the notification modal using the provided message. 
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
 * Purpose: Initializes all necessary components of the frontend
 * @param {string} IANATimezone
 */
export function initializePage(IANATimezone) {
    // NOTIFICATION MODAL EVENT HANDLER
    let notificationModal = document.getElementById("notification-modal");
    let closeButton = notificationModal.querySelector(".modal__close");
    closeButton.addEventListener("click", function (event) {
        notificationModal.classList.remove("modal--show");
    })
    // CURRENT TIME DISPLAY
    let currentTimeDisplay = document.getElementById("current-time-display");
    function updateTime() {
        const now = new Date();
        currentTimeDisplay.textContent = createTimeString(now, IANATimezone);
    }
    updateTime();
    setInterval(updateTime, 1000);
}

/** Purpose: Creates the notification modal using the provided message.
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

/** Purpose: Creates a HH:MM:SS time string given the provided time and IANATimezone
 * @param {Date} time Current Time Object
 * @param {string} IANATimezone Timezone of current time
 */
export function createTimeString(time, IANATimezone) {
    return time.toLocaleTimeString("en-US", {
        timeZone: IANATimezone,
        hour12: false,   // 24-hour format
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}

/** Purpose: Creates a `stats__item` to display
 * @param {string} name Name of the stat item
 * @param {number|string} value Value of the stat item
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
}

