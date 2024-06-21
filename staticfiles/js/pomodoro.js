// Function to toggle the timer between starting/pausing and showing/hiding controls
function toggleTimer() {
    if (timerInterval) {
        stopTimer();
        document.getElementById("startButton").style.display = "block";
        document.getElementById("pauseButton").style.display = "none";
    } else {
        startTimer();
        document.getElementById("startButton").style.display = "none";
        document.getElementById("pauseButton").style.display = "block";
    }
    saveTimerState();
}

// Function to stop the sound (if any)
function stopSound() {
    alarmSound.pause();
}

// Variables to manage the timer state
var timerInterval = null;
var timeLeft = 1500; // 25 minutes in seconds
var isStudyTime = true;

// Function to start the timer
function startTimer() {
    timerInterval = setInterval(updateTimer, 1000);
    saveTimerState();
}

// Function to stop the timer
function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    saveTimerState();
}

// Function to reset the timer
function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = 1500;
    document.getElementById("startButton").style.display = "block";
    document.getElementById("pauseButton").style.display = "none";
    updateDisplay();
    saveTimerState();
}

// Function to update the timer display
function updateTimer() {
    if (timeLeft > 0) {
        timeLeft--;
        updateDisplay();
    } else {
        clearInterval(timerInterval);
        timerInterval = null;
        if (isStudyTime) {
            timeLeft = 300; // 5 minutes break time
            isStudyTime = false;
            showNotification("Time for a break!");
        } else {
            timeLeft = 1500; // 25 minutes study time
            isStudyTime = true;
            alert("Break's over Time to study!");
        }
        saveTimerState();
        updateDisplay();
        startTimer(); // Start the timer immediately after updating the state
    }
}

// Function to update the display text
function updateDisplay() {
    var minutes = Math.floor(timeLeft / 60);
    var seconds = timeLeft % 60;
    document.getElementById("timer").innerText = padZero(minutes) + ":" + padZero(seconds);
    saveTimerState();
}

// Function to pad zeros for single-digit numbers
function padZero(number) {
    return (number < 10)? "0" + number : number;
}

// Function to show notifications
function showNotification(string1) {
    let title = "JavaScript Jeep";
    let icon = 'https://homepages.cae.wisc.edu/~ece533/images/airplane.png';
    let body = string1 + "\nClick here to stop audio";
    var notification = new Notification('Timer Ended', { body, icon });

    notification.onclose = function() {
        stopSound();
    };

    notification.onclick = function() {
        notification.close();
        stopSound();
        window.parent.focus();
    };
}

// Function to save the timer state to localStorage
function saveTimerState() {
    localStorage.setItem('timerState', JSON.stringify({ timeLeft: timeLeft, isStudyTime: isStudyTime }));
}

// Function to load the timer state from localStorage
function loadTimerState() {
    const savedState = localStorage.getItem('timerState');
    if (savedState) {
        const state = JSON.parse(savedState);
        timeLeft = state.timeLeft;
        isStudyTime = state.isStudyTime;
        toggleTimer(); // Resume the timer based on the saved state
        updateDisplay();
    }
}

// Load the timer state when the page loads
window.onload = function() {
    loadTimerState();
};
