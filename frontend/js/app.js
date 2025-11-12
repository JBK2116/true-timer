/*
Frontend entry point for this application
 */
import * as utils from "./utils.js";

const URLS = utils.ENDPOINTS;

let timer = null;

async function main() {
    // ensure user has a valid uuid
    const userTimezone = utils.getUserIANAString();
    const hasValidID = await checkUUID();
    if (!hasValidID) {
        const idCreated = await createUUID(userTimezone);
        if (!idCreated) {
            utils.showNotificationStatic("Oops! There was a problem setting things up. Try reloading the page.",);
            return;
        }
    }
    const user_uuid = localStorage.getItem("user_uuid");
    // user has a valid uuid by this point
    utils.setPage(userTimezone);
    utils.showNotificationDynamic("All set! Let's start your first timer.", 3);
    // TODO: Set up the event handling for card timers, start with the standard timer.
    await setUpStandardTimerCard();

}

document.addEventListener("DOMContentLoaded", main);

/**
 * Checks for a cached UUID string in the User's browsers
 * If there is a cached UUID, sends a GET request to ensure it belongs to a user and is valid
 *
 * @returns true if successful, false otherwise
 */
async function checkUUID() {
    // ensure UUID is valid
    // check browser cache
    const value = localStorage.getItem("user_uuid");
    if (!value) return false;
    try {
        const response = await fetch(`${URLS.USER}/${value}`);
        return response.ok;
    } catch (error) {
        console.log(error);
        return false;
    }
}

/**
 * Sends a POST request for a UUID string from the backend.
 * Timezone must be included to receive a UUID
 *
 * Caches the result in the user's browser
 * @returns true if successful, else false
 */
async function createUUID(timezone) {
    const payload = {timezone: timezone};
    try {
        const response = await fetch(`${URLS.USER}`, {
            method: "POST", headers: {
                "Content-Type": "application/json",
            }, body: JSON.stringify(payload),
        });
        if (!response.ok) return false;
        const result = await response.json();
        if (!result.user_id) return false;
        localStorage.setItem("user_uuid", result.user_id);
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
}

/**
 * Sets up the `standard-timer` card to handle submissions
 *
 * Calls `StandardTimerSubmit` to handle the full timer lifecycle
 * @returns {Promise<void>}
 */
async function setUpStandardTimerCard() {
    let card = document.getElementById("preset-standard");
    let submitModal = document.getElementById("standard-timer-modal");
    let closeSubmitModalBtn = document.getElementById("close-standard-modal");
    card.addEventListener("click", () => {
        // Show standard timer submit form
        submitModal.classList.remove("modal--hidden");
        submitModal.classList.add("modal--show");
    });
    // set up close button for submit form
    closeSubmitModalBtn.addEventListener("click", () => {
        submitModal.classList.remove("modal--show");
        submitModal.classList.add("modal--hidden");
    });
    // call the standard timer submit function to handle timer life cycle
    await standardTimerSubmit();
}

async function standardTimerSubmit() {
    document.getElementById("standard-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        // manually handle form submission
        const hours = parseInt(document.getElementById("timer-hours").value);
        const minutes = parseInt(document.getElementById("timer-minutes").value);
        let payload = {"minutes": minutes, "hours": hours};
        const response = await fetch(`${URLS.STANDARD_TIMER.ROOT}`, {
            method: "POST", headers: {
                'Content-Type': 'application/json', 'X-User-ID': localStorage.getItem("user_uuid"),
            }, body: JSON.stringify(payload),
        });
        // convert response data to JSON
        const data = await response.json();
        // handle error response
        if (!response.ok) {
            if (data.message) {
                utils.showNotificationStatic(data.message);
            } else {
                utils.showNotificationStatic("An error occurred whilst creating your timer. Please reload the page and try again")
            }
        }
        // TODO: Finish this function
        console.log(data); // works properly
        // handle successful response
        // timer = new StandardTimer()
    });
}
