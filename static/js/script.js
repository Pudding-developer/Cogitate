// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;




// Pomodoro
// variables
let workTitle = document.getElementById('work');
let breakTitle = document.getElementById('break');

let workTime = 25;
let breakTime = 5;

let seconds = "00";
let timerInterval;
let remainingMinutes = workTime;
let remainingSeconds = 0;
let timerPaused = false;

// display
window.onload = () => {
    document.getElementById('minutes').innerHTML = workTime;
    document.getElementById('seconds').innerHTML = seconds;

    workTitle.classList.add('active');
}

// start or resume timer
function start() {
    // change buttons
    document.getElementById('start').style.display = "none";
    document.getElementById('reset').style.display = "block";
    document.getElementById('pause').style.display = "block";

    // resume countdown if paused
    if (timerPaused) {
        timerInterval = setInterval(timerFunction, 1000);
    } else {
        // initialize timer if not paused
        timerInterval = setInterval(timerFunction, 1000); // 900= 1s
    }
    timerPaused = false;

    // Reset the timer if it was paused and reached 0
    if (remainingMinutes === 0 && remainingSeconds === 0) {
        reset();
    }
}

// pause timer
function pause() {
    // change buttons
    document.getElementById('start').style.display = "block";
    document.getElementById('reset').style.display = "block";
    document.getElementById('pause').style.display = "none";

    // stop countdown
    clearInterval(timerInterval);
    timerPaused = true;
}

// reset timer
function reset() {
    // reset variables
    clearInterval(timerInterval);
    timerPaused = false; // This line was missing
    remainingMinutes = workTime;
    remainingSeconds = 0;

    // change buttons
    document.getElementById('start').style.display = "block";
    document.getElementById('reset').style.display = "none";
    document.getElementById('pause').style.display = "none";

    // update display
    document.getElementById('minutes').innerHTML = remainingMinutes;
    document.getElementById('seconds').innerHTML = remainingSeconds < 10 ? "0" + remainingSeconds : remainingSeconds;

    // change the panel
    workTitle.classList.add('active');
    breakTitle.classList.remove('active');
}

// countdown function
function timerFunction() {
    // change the display
    document.getElementById('minutes').innerHTML = remainingMinutes;
    document.getElementById('seconds').innerHTML = remainingSeconds < 10 ? "0" + remainingSeconds : remainingSeconds;

    // decrement time
    remainingSeconds--;

    if (remainingSeconds < 0) {
        remainingMinutes--;

        if (remainingMinutes < 0) {
            // switch between work and break
            toggleTimerState();
        }
        remainingSeconds = 59;
    }
}

// toggle between work and break
function toggleTimerState() {
    if (workTitle.classList.contains('active')) {
        // start break
        remainingMinutes = breakTime - 1;
        workTitle.classList.remove('active');
        breakTitle.classList.add('active');
    } else {
        // continue work
        remainingMinutes = workTime - 1;
        breakTitle.classList.remove('active');
        workTitle.classList.add('active');
    }
}



//Calendar
$(document).ready(function () {
    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: '/all-events',
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true,
        eventColor: '#A4857A',
        eventRender: function (event, element) {
            if (event.complete) {
                // Cross out the event title
                element.css('text-decoration', 'line-through');
                // Change the background color to lightgray or any other color you prefer
                // element.css('background-color', 'lightgray');
            } else {
                // Reset styles if the event is not complete
                element.css('text-decoration', 'none');
                element.css('background-color', '#A4857A');
            }
        },
        select: function (start, end, allDay) {
            var title = prompt("Enter Event Title");
            if (title) {
                var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
                var end = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");
                var complete = false;  // Assuming newly added events are not completed by default
                $.ajax({
                    type: "GET",
                    url: '/add-event',
                    data: { 'title': title, 'start': start, 'end': end, 'complete': complete },
                    dataType: "json",
                    success: function (data) {
                        calendar.fullCalendar('refetchEvents');
                        alert("Added Successfully");
                    },
                    error: function (data) {
                        alert('There is a problem!!!');
                    }
                });
            }
        },

        eventResize: function (event) {
            var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
            var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
            var title = event.title;
            var id = event.id;
            $.ajax({
                type: "GET",
                url: '/update',
                data: { 'title': title, 'start': start, 'end': end, 'id': id },
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    alert('Event Update');
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        },

        eventDrop: function (event) {
            var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
            var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
            var title = event.title;
            var id = event.id;
            $.ajax({
                type: "GET",
                url: '/update',
                data: { 'title': title, 'start': start, 'end': end, 'id': id },
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    alert('Event Update');
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        },

        eventClick: function (event) {
            if (confirm("Are you sure you want to remove it?")) {
                var id = event.id;
                $.ajax({
                    type: "GET",
                    url: '/remove',
                    data: { 'id': id },
                    dataType: "json",
                    success: function (data) {
                        calendar.fullCalendar('refetchEvents');
                        alert('Event Removed');
                    },
                    error: function (data) {
                        alert('There is a problem!!!');
                    }
                });
            }
        },

    });
});



