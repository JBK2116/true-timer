/**
 * QueueTimer Application
 * Handles user registration with timezone and displays notifications
 */

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8080/api';

// Modal timeout reference
let modalTimeout = null;

/**
 * Display a modal notification
 * @param {string} title - Modal title
 * @param {string} message - Modal message
 * @param {string} type - Modal type ('success' or 'error')
 * @param {number} duration - Duration in milliseconds (default: 4000)
 */
function showModal(title, message, type = 'success', duration = 4000) {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modal-content');
    const modalTitle = document.getElementById('modal-title');
    const modalMessage = document.getElementById('modal-message');

    // Clear existing timeout
    if (modalTimeout) {
        clearTimeout(modalTimeout);
    }

    // Set modal content
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    
    // Remove existing type classes and add new one
    modalContent.classList.remove('success', 'error');
    modalContent.classList.add(type);

    // Show modal
    modal.style.display = 'flex';

    // Auto-hide after specified duration
    modalTimeout = setTimeout(() => {
        hideModal();
    }, duration);
}

/**
 * Hide the modal notification
 */
function hideModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
    
    if (modalTimeout) {
        clearTimeout(modalTimeout);
        modalTimeout = null;
    }
}

/**
 * Register user with their timezone information
 * Sends POST request to /api/users with IANA timezone string
 */
async function registerUser() {
    try {
        // Get user's IANA timezone string
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        
        console.log('Registering user with timezone:', timezone);

        // Send POST request to register user
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ timezone })
        });

        // Handle successful registration (201 Created)
        if (response.status === 201) {
            showModal(
                'Success!', 
                'Application is ready to start tracking your assignments.', 
                'success'
            );
            return;
        }

        // Handle other status codes as errors
        const errorData = await response.json();
        const errorMessage = errorData.detail || 'An unexpected error occurred';
        
        showModal(
            'Registration Error', 
            errorMessage, 
            'error'
        );

    } catch (error) {
        console.error('Error registering user:', error);
        
        // Handle network errors or other exceptions
        showModal(
            'Connection Error', 
            'Unable to connect to the server. Please check your connection and try again.', 
            'error'
        );
    }
}

/**
 * Initialize application on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('QueueTimer application initialized');
    
    // Register user immediately on page load
    registerUser();

    // Add click event to modal to hide it manually
    document.getElementById('modal').addEventListener('click', function(e) {
        if (e.target === this) {
            hideModal();
        }
    });
});