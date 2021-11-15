//Heavily inspired by Code and Create https://www.youtube.com/watch?v=o1yMqPyYeAo&t=1135s

//Class which defines events that will be added to the calendar
class CalendarEvent {

    constructor(date, group, description) {
        this.setDate(date)
        this.setGroup(group);
        this.setDescription(description);
    }
   
    setDate(date) {
        let dateArray = date.split('/')
        dateArray[0] = dateArray[0] - 1;
        if(validDate(dateArray)) {
            this.date = dateArray;
        }
    }

    setGroup(group) {
        this.group = group;
    }

    setDescription(description) {
        this.description = description;
    }

    getDate(index) {
        return this.date[index];
    }

    getGroup() {
        return this.group;
    }

    getDescription() {
        return this.description;
    }

    validDate(date) {
        if(date.length != 3) {
            console.log("date did not have 3 parts")
            return false
        }
        if(date[0] < 0 || date[0] > 11) {
            console.log("month was less than 1 and greater than 12")
            return false
        }
        if(date[1] > 1 || date[1] < new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay()) {
            console.log(new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay() + " was not equal to the value entered")
            return false
        }
        console.log("no issue was found with the date")
        return true
    }
    
}


//constants used for rendering the calendar
const date = new Date();
const importButton = document.querySelector('.import');
const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];

//renders the calendar
const renderCalendar = (eventArray) => {
    
    date.setDate(1);

    const monthDays = document.querySelector('.days');

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();

    const nextDays = 7 - lastDayIndex - 1;

    //displays the information in the header
    document.querySelector('.date h1').innerHTML = months[date.getMonth()];

    document.querySelector('.year').innerHTML = date.getFullYear();

    document.querySelector('.date p').innerHTML = new Date().toDateString();

    let days = "";

    for(let x = firstDayIndex; x > 0; x--){
        days += `<div class = "prev-date">${prevLastDay - x + 1}</div>`
    }

    //builds and displays the days for the month
    for(let i = 1; i <= lastDay; i++){
        let dailyEvents = "";
        //true if its todays date
        if(i === new Date().getDate() && (date.getMonth() === new Date().getMonth()) && date.getFullYear() === new Date().getFullYear()) {
            //loops through the event array
            eventArray.forEach(function(event) {
                //true if the event matches todays date
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                        dailyEvents += event.getDescription() + "<br>";
                }
            })
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i} today">${i + " " + `<p>${dailyEvents}</p>`}</div>`;
            
        }else{
            //loops through the events array
            eventArray.forEach(function(event) {
                //true if the event date matches the current date of the for loop
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                    dailyEvents += event.getDescription() + "<br>";
                }
            })
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i}">${i + " " + `<p>${dailyEvents}</p>`}</div>`;
        }
    }

    for(let j = 1; j <= nextDays; j++){
        days += `<div class = "next-date">${j}</div>`;
    }
    monthDays.innerHTML = days;

}

//Array used to store the events which will display on the calendar
let eventArray = [];

//checks for a click on the next and previous month arrows
document.querySelector('.prev').addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar(eventArray);
});

document.querySelector('.next').addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar(eventArray);
});

//creates the calendar
renderCalendar(eventArray);


//popup when clicking on a day
const openModalButtons = document.querySelectorAll("[data-modal-target]");
const closeModalButtons = document.querySelectorAll("[data-close-button]")

//opens whenever a day is clicked on
openModalButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e = e || window.event;
        let target = e.target
        let text = target.classList;
        const modal = document.querySelector(button.dataset.modalTarget)
        document.getElementById("title").innerHTML = text[1] + " " + text[2] + ", " + text[0]

        //generates the text boxes and buttons on the popup for the specified day based on the events on that day
        let dailyEvents = ""
        let eventFound = false
        eventArray.forEach(function(event, index) {
            if((event.getDate(1) == text[2] || event.getDate(1) == "0" + text[2]) && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                eventFound = true
                //generates the textboxes and buttons for the specified event
                dailyEvents += `<div class="event-section">
                                    <b>Event</b>
                                    <p>Date</p>
                                    <input id="date${index}" type="text" value="${(event.getDate(0) + 1) + "/" + text[2] + "/" + event.getDate(2)}" />
                                    <p>Group Name</p>
                                    <input id="group${index}" type="text" value="${event.getGroup()}" />
                                    <p>Description</p>
                                    <input id="description${index}" type="text" value="${event.getDescription()}" />
                                    <button data-event-delete${index} id="delete-event${index}" onclick="deleteEvent(${index}, eventArray)">Delete Event</button>
                                </div>`
            }
        })
        if(eventFound) {
            dailyEvents += `<button data-event-save id="save-events">Save Events</button>`
        }
        //generates the add event textboxes and buttons
        dailyEvents += `<div class="event-section">
                            <b>Add Event</b>
                            <p>Date</p>
                            <input id="add-date" type="text" value="${(months.indexOf(text[1]) + 1) + "/" + text[2] + "/" + text[0]}"/>
                            <p>Group Name</p>
                            <input id="add-group" type="text"/>
                            <p>Description</p>
                            <input id="add-description" type="text"/>
                            <button data-event-add id="add-event">Add Event</button>
                        </div>`
        document.getElementById("modal-body").innerHTML = dailyEvents;

        //section that actually opens the modal
        if(text[0] != "next-date" && text[0] != "prev-date" && text[0] != "days") {
            console.log(text)
            openModal(modal)

            const createEventButton = document.querySelectorAll("[data-event-add]")
            const saveEventButton = document.querySelectorAll("[data-event-save]")

            createEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    const date = document.getElementById("add-date").value
                    console.log(date)
                    const group = document.getElementById("add-group").value
                    console.log(group)
                    const description = document.getElementById("add-description").value
                    console.log(description)
                    addNewEvent(date, group, description, eventArray)
                    renderCalendar(eventArray);
                    const modal = button.closest('.modal')
                    closeModal(modal)
                })
            })

            saveEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    eventArray.forEach(function(event, index) {
                        if((event.getDate(1) == text[2] || event.getDate(1) == "0" + text[2]) && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                            event.setDate(document.getElementById("date"+index).value)
                            event.setGroup(document.getElementById("group"+index).value)
                            event.setDescription(document.getElementById("description"+index).value)
                            renderCalendar(eventArray);
                            const modal = button.closest('.modal')
                            closeModal(modal)
                        }
                    })
                })
            })
        }
    }, false);
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
});

function openModal(modal) {
    if (modal == null) return;
    modal.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return;
    modal.classList.remove('active')  
}

function addNewEvent(date, group, description, array) {
    let event = new CalendarEvent(date, group, description);
    array.push(event);
}

function deleteEvent(index, array) {
    console.log(index)
    array.splice(index, 1)
    renderCalendar(eventArray);
    closeModal(document.getElementsByClassName("modal")[0])
}

function changeEvent(date, group, description, index, array) {
        array[index].setDate(date)
        array[index].setGroup(group)
        array[index].setDescription(description)
}



const createEventButton = document.querySelectorAll("[data-event-add]")
const deleteEventButton = document.querySelectorAll("[data-event-delete]")
const changeEventButton = document.querySelectorAll("[data-event-change]")

createEventButton.forEach(button => {
    button.addEventListener('click', () => {
        const date = document.getElementById("add-date").value
        const group = document.getElementById("add-group").value
        const description = document.getElementById("add-description").value
        addNewEvent(date, group, description, eventArray)
        renderCalendar(eventArray);
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})

deleteEventButton.forEach(button => {
    button.addEventListener('click', () => {
        let date = document.getElementById("find-date").value.split('/')
        date[0] = date[0]-1;
        const group = document.getElementById("find-group").value
        const description = document.getElementById("find-description").value
        let index = findEvent(date, group, description, eventArray)
        if(index != null) {
            deleteEvent(index, eventArray)
            renderCal
            const modal = button.closest('.modal')
            closeModal(modal)
        }
    })
})

changeEventButton.forEach(button => {
    button.addEventListener('click', () => {
        let findDate = document.getElementById("find-date").value.split('/')
        findDate[0] = findDate[0]-1;
        const findGroup = document.getElementById("find-group").value
        const findDescription = document.getElementById("find-description").value
        let index = findEvent(findDate, findGroup, findDescription, eventArray)
        if(index != null) {
            let changeDate = document.getElementById("change-date").value
            const changeGroup = document.getElementById("change-group").value
            const changeDescription = document.getElementById("change-description").value
            changeEvent(changeDate, changeGroup, changeDescription, index, eventArray);
            renderCalendar(eventArray);
            const modal = button.closest('.modal')
            closeModal(modal)
        }
    })
})

// It accepts a dictionary an iterates through its elements
function handleResponse(obj) {  
    // Counting the number of events in the JSON object
    let numEvents = 0
    for (let key of Object.keys(obj)) {
        for (let number of Object.keys(obj[key])){
            numEvents++
        }
        if (numEvents != 0) { break }
    }
    // For each event in the JSON object create a new event and
    // append it to the event array.
    for(let i = 0; i < numEvents; i++){
        let eventAssignment = obj["Assignments"][i]
        let eventDate = obj["Date"][i]
        addNewEvent(eventDate, "No group", eventAssignment, eventArray)
    }
    renderCalendar(eventArray);
}

function handleError(errorMessage) {
    // Show dismissible error message
    $('.container').prepend("<div id='error_message' class='alert alert-danger alert-dismissible fade show' role='alert'> <strong>Error</strong> - "+ errorMessage +"<button type='button' class='close' data-dismiss='alert' aria-label='Close'> <span aria-hidden='true'>&times;</span> </button> </div>")
}

$('#file_form').change(function(e){
    var form_data = new FormData();
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    form_data.append('file', $('#file_input')[0].files[0]);    
    
    $.ajax({
        type:'POST',
        url:'/read_docx',
        headers: {'X-CSRFToken': token},
        processData: false,
        contentType: false,
        datatype: 'json',
        async: false,
        cache: false,
        data : form_data,
        success: function(data){
            handleResponse(data)
        },
        error:function(data){
            handleError(data.statusText);
        } 
    });
    e.preventDefault();
});