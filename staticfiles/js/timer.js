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
}

var miniTimerInterval = null;
var miniTimeLeft = 1500; // 25 minutes in seconds
var miniIsStudyTime = true;

function startMiniTimer() {
    miniTimerInterval = setInterval(updateMiniTimer, 1000);
}

function stopMiniTimer() {
    clearInterval(miniTimerInterval);
    miniTimerInterval = null;
}

function resetMiniTimer() {
    clearInterval(miniTimerInterval);
    miniTimeLeft = 1500;
    toggleMiniTimer();
    updateMiniTimerDisplay();
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
        updateMiniTimerDisplay();
    }
}

function updateMiniTimerDisplay() {
    var minutes = Math.floor(miniTimeLeft / 60);
    var seconds = miniTimeLeft % 60;
    document.getElementById("miniTimerDisplay").innerText = padZero(minutes) + ":" + padZero(seconds);
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
