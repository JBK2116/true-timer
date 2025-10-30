/*
Frontend entry point for this application
 */
import * as utils from './utils.js';
import {StandardTimer} from "./standard-timer.js";

function main() {
    let timezone = utils.getUserIANAString();
    console.log(`Timezone: ${timezone}`);
    utils.initializePage(timezone);
    utils.showNotificationDynamic("Application ready for use", 3);
    let timer = new StandardTimer(new Date, new Date(Date.now() + 60 * 1000), 60, timezone);
    timer.initializeWorkTimer(timezone);
}

document.addEventListener('DOMContentLoaded', main);