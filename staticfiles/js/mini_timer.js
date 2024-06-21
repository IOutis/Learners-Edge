
function toggleTimer() {
    if (timerInterval) {
        stopTimer();
        document.getElementById("startButton").style.display="block";
        document.getElementById("pauseButton").style.display = "none";
    } else {
        startTimer();
        document.getElementById("startButton").style.display="none";
        document.getElementById("pauseButton").style.display = "block";
    }
}


var timerInterval=null;
var timeLeft = 1500; // 25 minutes in seconds
var isStudyTime = true;

function startTimer() {
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null; 
}

function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = 1500;
    // document.getElementById("startButton").style.display="block";
    // document.getElementById("pauseButton").style.display = "none";
    toggleTimer();
    updateDisplay();
}

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
            alert("Break's over! Time to study!");
        }
        updateDisplay();
    }
}

function updateDisplay() {
    var minutes = Math.floor(timeLeft / 60);
    var seconds = timeLeft % 60;
    document.getElementById("timer").innerText = padZero(minutes) + ":" + padZero(seconds);
}

function padZero(number) {
    return (number < 10) ? "0" + number : number;
}

function showNotification(string1) {
    let title = "JavaScript Jeep";
    let icon = 'https://homepages.cae.wisc.edu/~ece533/images/airplane.png';
    let body = string1+"\nClick here to stop audio";
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

// New toggleTimer function

