/*
Frontend entry point for this application
 */
import * as utils from './utils.js';
import {StandardTimer} from "./standard-timer.js";

const URLS = utils.ENDPOINTS

async function main() {
    // ENSURE USER HAS VALID UUID
    const userTimezone = utils.getUserIANAString();
    const hasValidID  = await checkUUID();
    if (!hasValidID) {
        const idCreated   = await createUUID(userTimezone);
        if (!idCreated) {
            utils.showNotificationStatic("Oops! There was a problem setting things up. Try reloading the page.")
            return;
        }
    }
    const uuid = localStorage.getItem("user_uuid");
    // USER HAS VALID UUID BY THIS POINT
    utils.setPage(userTimezone);
    utils.showNotificationDynamic("All set! Let's start your first timer.", 3000)
}

document.addEventListener('DOMContentLoaded', main);

/**
 * Checks for a cached UUID string in the User's browsers
 * If there is a cached UUID, sends a GET request to ensure it's valid
 *
 * @returns true if UUID is valid, false otherwise
 */
async function checkUUID() {
    // check browser cache
    const value = localStorage.getItem("uuid");
    if (!value) return false; 
    // ensure UUID is valid
    try {
        const response = await fetch(`${URLS.TEST.UUID}${value}`);
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
    const payload = {"timezone": timezone};
    try {
        const response = await fetch(`${URLS.UUID}`, {
            method: "POST", body: JSON.stringify(payload),
        })
        if (!response.ok) return false;
        const result = await response.json();
        if (!result.id) return false;
        localStorage.setItem("user_uuid", result.id)
        return true;
    } catch (error) {
        console.log(error);
        return false;
    }
}