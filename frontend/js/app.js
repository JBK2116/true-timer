/*
Frontend entry point for this application
 */
import * as utils from './utils.js';

// ELEMENT DECLARATIONS

function main() {
    let timezone = utils.getUserIANAString();
    console.log(`Timezone: ${timezone}`);
    utils.initializePage(timezone);
    utils.showNotificationDynamic("Application ready for use", 3);
}

document.addEventListener('DOMContentLoaded', main);