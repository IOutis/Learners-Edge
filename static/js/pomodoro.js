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


// Function to save the mini timer state to localStorage

var miniTimerInterval = null;
var miniTimeLeft = 1500; // 25 minutes in seconds
var miniIsStudyTime = true;

function toggleMiniTimer() {
    if (miniTimerInterval) {
        stopMiniTimer();
        document.getElementById("startControlButton").style.display = "block";
        document.getElementById("pauseControlButton").style.display = "none";
    } else {
        startMiniTimer();
        document.getElementById("startControlButton").style.display = "none";
        document.getElementById("pauseControlButton").style.display = "block";
    }
    saveMiniTimerState(); // Save the state after toggling
}

function stopMiniTimer() {
    clearInterval(miniTimerInterval);
    miniTimerInterval = null;
    saveMiniTimerState(); // Save the state after stopping
}

function startMiniTimer() {
    miniTimerInterval = setInterval(updateMiniTimer, 1000);
    saveMiniTimerState(); // Save the state after starting
}

function resetMiniTimer() {
    clearInterval(miniTimerInterval);
    miniTimeLeft = 1500;
    document.getElementById("startControlButton").style.display = "block";
    document.getElementById("pauseControlButton").style.display = "none";
    updateMiniTimerDisplay();
    saveMiniTimerState(); // Save the state after resetting
}

function updateMiniTimer() {
    if (miniTimeLeft > 0) {
        miniTimeLeft--;
        updateMiniTimerDisplay();
    } else {
        clearInterval(miniTimerInterval);
        miniTimerInterval = null;
        if (miniIsStudyTime) {
            miniTimeLeft = 300; // 5 minutes break time
            miniIsStudyTime = false;
            showNotification("Time for a break!");
        } else {
            miniTimeLeft = 1500; // 25 minutes study time
            miniIsStudyTime = true;
            alert("Break's over Time to study!");
        }
        saveMiniTimerState(); // Save the state after updating
        updateMiniTimerDisplay();
        startMiniTimer(); // Start the timer immediately after updating the state
    }
}

function updateMiniTimerDisplay() {
    var minutes = Math.floor(miniTimeLeft / 60);
    var seconds = miniTimeLeft % 60;
    document.getElementById("miniTimerDisplay").innerText = padZero(minutes) + ":" + padZero(seconds);
    saveMiniTimerState(); // Save the state after updating the display
}

function padZero(number) {
    return (number < 10)? "0" + number : number;
}

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

// Function to save the mini timer state to localStorage
function saveMiniTimerState() {
    localStorage.setItem('miniTimerState', JSON.stringify({ timeLeft: miniTimeLeft, isStudyTime: miniIsStudyTime }));
}

// Function to load the mini timer state from localStorage
function loadMiniTimerState() {
    const savedState = localStorage.getItem('miniTimerState');
    if (savedState) {
        const state = JSON.parse(savedState);
        miniTimeLeft = state.timeLeft;
        miniIsStudyTime = state.isStudyTime;
        toggleMiniTimer(); // Resume the mini timer based on the saved state
        updateMiniTimerDisplay();
    }
}

// Load the mini timer state when the page loads
window.onload = function() {
    loadMiniTimerState();
    const miniTimerOpened = localStorage.getItem('miniTimerOpened');

    if (miniTimerOpened === 'true') {
        document.getElementById('miniTimerContainer').style.display = "block";
    }
};


function popdown(){
    clearInterval(miniTimerInterval);
    miniTimerInterval = null;
    document.getElementById('miniTimerContainer').style.display="none";
    localStorage.setItem('miniTimerOpened', 'false');
    resetMiniTimer();
    saveMiniTimerState();
  }


//draggable element
