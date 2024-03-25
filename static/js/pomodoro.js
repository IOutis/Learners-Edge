var alarmSound = document.getElementById('alarmSound');
function playSound() {
    // document.write("Playing sound..."); // Debugging log
    alarmSound.play();
    // alarmSound.play().then(() => {
    //     document.write("Sound played successfully.");
    // }).catch(error => {
    //     document.write("Error playing sound:", error);
    // });
}
function stopSound(){
    alarmSound.pause();
}

var timerInterval;
        var timeLeft = 1500; // 25 minutes in seconds
        var isStudyTime = true;

        function startTimer() {
            timerInterval = setInterval(updateTimer, 1000);
        }

        function stopTimer() {
            clearInterval(timerInterval);
        }

        function resetTimer() {
            clearInterval(timerInterval);
            timeLeft = 1500;
            updateDisplay();
        }

        function updateTimer() {
            if (timeLeft > 0) {
                timeLeft--;
                updateDisplay();
            } else {
                clearInterval(timerInterval);
                if (isStudyTime) {

                   
                    timeLeft = 300; // 5 minutes break time
                    isStudyTime = false;
                    // alert("Time for a break!");
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
        
            // Play the sound when the notification is shown
            playSound();
        
            // Stop the sound when the notification is closed
            notification.onclose = function() {
                stopSound();
            };
        
            // Optionally, you can also stop the sound when the notification is clicked
            notification.onclick = function() {
                notification.close();
                stopSound();
                window.parent.focus();
            };
        }
        