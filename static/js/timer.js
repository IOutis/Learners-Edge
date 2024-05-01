// // // Access the span elements
// // var firDate = document.getElementById('fir').textContent;
// // var fitTimeSlot = document.getElementById('fit').textContent;

// // // Parse the date
// // var eventDate = new Date(firDate);

// // // Parse the time slot
// // var timeParts = fitTimeSlot.split(':');
// // var hours = parseInt(timeParts[0], 10);
// // var minutes = parseInt(timeParts[1], 10);
// // var seconds = parseInt(timeParts[2], 10);

// // // Set the time on the eventDate object
// // eventDate.setHours(hours, minutes, seconds, 0);
// // var now = new Date();
// // var timeDifference = eventDate - now;

// // // Get the timer display element
// // var timerDisplay = document.getElementById('timerDisplay');

// // var countdown = setInterval(function() {
// //     var secondsLeft = Math.floor((timeDifference / 1000) % 60);
// //     var minutesLeft = Math.floor((timeDifference / 1000 / 60) % 60);
// //     var hoursLeft = Math.floor((timeDifference / (1000 * 60 * 60)) % 24);
// //     var daysLeft = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

// //     timeDifference -= 1000;

// //     // Update the timer display
// //     timerDisplay.innerHTML = daysLeft + "d " + hoursLeft + "h " + minutesLeft + "m " + secondsLeft + "s ";

// //     // If the countdown is finished, clear the interval
// //     if (timeDifference < 0) {
// //         clearInterval(countdown);
// //         timerDisplay.innerHTML = "Countdown finished!";
// //         alert("Countdown finished!");
// //     }
// // }, 1000);


// // function updateTimetable() {
// //     fetch('/get_timetable_data/')
// //         .then(response => response.json())
// //         .then(data => {
// //             const container = document.getElementById('timetable-container');
// //             container.innerHTML = ''; // Clear the container
// //             data.forEach(entry => {
// //                 // Create and append elements for each timetable entry
// //                 const entryElement = document.createElement('div');
// //                 entryElement.textContent = `${entry.fields.task_activity} - ${entry.fields.date} ${entry.fields.time_slot}`;
// //                 container.appendChild(entryElement);
// //             });
// //         })
// //         .catch(error => console.error('Error fetching timetable data:', error));
// // }

// // // Call updateTimetable when the page loads
// // document.addEventListener('DOMContentLoaded', updateTimetable);

// // // Optionally, call updateTimetable periodically to keep the timetable updated
// // setInterval(updateTimetable, 5000);








// document.addEventListener('DOMContentLoaded', function() {
//     // Get the scheduled time from the hidden input
//     var scheduledTimeInput = document.getElementById('scheduledTime');
//     console.log("Scheduled Time:", scheduledTimeInput.value); // Debugging line
//     var scheduledTime = scheduledTimeInput.value.split(':');
//     var scheduledHour = parseInt(scheduledTime[0], 10);
//     var scheduledMinute = parseInt(scheduledTime[1], 10);

//     // Function to check if the current time matches the scheduled time
//     function checkTime() {
//         var now = new Date();
//         var nowHour = now.getHours();
//         var nowMinute = now.getMinutes();

//         alert("Current Time:", nowHour + ":" + nowMinute); // Debugging line

//         if (nowHour === scheduledHour && nowMinute === scheduledMinute) {
//             // Play the sound
//             var alarmSound = document.getElementById('alarmSound');
//             alert("Playing sound..."); // Debugging line
//             alarmSound.play();
//         }
//     }

//     // Check the time every minute
//     setInterval(checkTime, 60);
// });



function playSound() {
    var alarmSound = document.getElementById('alarmSound'); 
    alarmSound.play();
}

function timer_run() {
    var scheduledTimeElement = document.getElementById('scheduledTime');
    var scheduledTime = scheduledTimeElement.textContent || scheduledTimeElement.innerText;
    var t2 = new Date();
    var sm = parseInt(scheduledTime.slice(2, 4));
    var sh = parseInt(scheduledTime.slice(0, 2));
    
    if (sh === t2.getHours() && sm === t2.getMinutes()) {
        playSound();
    }
}
playSound();// Check the time every minute
setInterval(playSound, 600); // Check the time every minute