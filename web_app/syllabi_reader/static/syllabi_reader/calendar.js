//Heavily inspired by Code and Create https://www.youtube.com/watch?v=o1yMqPyYeAo&t=1135s



//Things to do:
    //export to ics
        //be able to select which groups to export to ics
        //*be able to select to export to csv (optional)
    //change the file location on the description to the group when importing
    //handle invalid inputs from the user when creating events
        //currently locks if the user types values into both description and group into add event. Then they remove remove a / and click add event
        //Currently only checks if the day is equal to or less than 31 so it lets some invalid dates on months with less than 31 days.
        //I challenge you to try and break it!
    //header dips into the weeks bar
    //Prevent a bunch of error messages from piling up on the screen
    //Try to clean up files that are not being used and tidy up the code the best we can.
    //Make sure the code properly handles each sylabus
    //Make it easily accesable (trying to get it on the web) (we may be able to get an exception to this)

    //Anything else...



//Class which defines events that will be added to the calendar
class CalendarEvent {

    constructor(date, group, description) {
        this.setDate(date)
        this.setGroup(group)
        this.setDescription(description)
    }
   
    setDate(date) {
        let dateArray = date.split('/')
        dateArray[0] = dateArray[0] - 1;
        //this is a quick fix for error handling. Doesn't work if there is a month that has less than 31 days**********
        if((dateArray[0] < 12 && dateArray[1] <= 31) && (dateArray[2] != undefined)) {
            console.log("sucess!?!")
            this.date = dateArray;
        } else {
            handleError("Date invalid, try mm/dd/yyyy")
        }
    }

    setGroup(group) {
        this.group = group 
    }

    setDescription(description) {
        this.description = description
    }

    getDate(index) {
        console.log("date length: " + this.date.length)
        if(index < this.date.length) {
            return this.date[index]
        }
    }

    getGroup() {
        return this.group
    }

    getDescription() {
        return this.description
    }
    
}


//constants used for rendering the calendar
const date = new Date()
const importButton = document.querySelector('.import')
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
]

//renders the calendar
const renderCalendar = (eventArray) => {
    
    date.setDate(1)

    const monthDays = document.querySelector('.days')

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate()

    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate()

    const firstDayIndex = date.getDay()

    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay()

    const nextDays = 7 - lastDayIndex - 1

    //displays the information in the header
    document.querySelector('.date h1').innerHTML = months[date.getMonth()]

    document.querySelector('.year').innerHTML = date.getFullYear()

    document.querySelector('.date p').innerHTML = new Date().toDateString()

    let days = ""

    for(let x = firstDayIndex; x > 0; x--){
        days += `<div class = "prev-date">${prevLastDay - x + 1}</div>`
    }

    //builds and displays the days for the month
    for(let i = 1; i <= lastDay; i++){
        let dailyEvents = ""
        //true if its todays date
        if(i === new Date().getDate() && (date.getMonth() === new Date().getMonth()) && date.getFullYear() === new Date().getFullYear()) {
            //loops through the event array
            eventArray.forEach(function(event) {
                //true if the event matches todays date
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                        dailyEvents += event.getDescription() + "<br>"
                }
            })
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i} today">${i + " " + `<p>${dailyEvents}</p>`}</div>`
            
        }else{
            //loops through the events array
            eventArray.forEach(function(event) {
                //true if the event date matches the current date of the for loop
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                    dailyEvents += event.getDescription() + "<br>"
                }
            })
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i}">${i + " " + `<p>${dailyEvents}</p>`}</div>`
        }
    }

    for(let j = 1; j <= nextDays; j++){
        days += `<div class = "next-date">${j}</div>`
    }
    monthDays.innerHTML = days

}

//Array used to store the events which will display on the calendar
let eventArray = []

//checks for a click on the next and previous month arrows
document.querySelector('.prev').addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1)
    renderCalendar(eventArray)
})

document.querySelector('.next').addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1)
    renderCalendar(eventArray)
})

//creates the calendar
renderCalendar(eventArray)


//popup when clicking on a day
const openModalButtons = document.querySelectorAll("[data-modal-target]")
const closeModalButtons = document.querySelectorAll("[data-close-button]")

//opens whenever a day is clicked on
openModalButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        console.log("day clicked")
        e = e || window.event
        let target = e.target
        let text = target.classList
        const modal = document.querySelector(button.dataset.modalTarget)
        document.getElementById("title").innerHTML = text[1] + " " + text[2] + ", " + text[0]
        console.log("Getting title: " + text[1] + " " + text[2] + ", " + text[0])

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
        document.getElementById("event-modal-body").innerHTML = dailyEvents
        console.log("text 1: " + text[1])
        console.log("getting date for text box: " + (months.indexOf(text[1]) + 1) + "/" + text[2] + "/" + text[0])

        //section that actually opens the modal
        if(text[0] != "next-date" && text[0] != "prev-date" && text[0] != "days") {
            console.log(text)
            openModal(modal)

            const createEventButton = document.querySelectorAll("[data-event-add]")
            const saveEventButton = document.querySelectorAll("[data-event-save]")

            createEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    const date = document.getElementById("add-date").value
                    const group = document.getElementById("add-group").value
                    const description = document.getElementById("add-description").value
                    addNewEvent(date, group, description, eventArray)
                    const modal = button.closest('.event-modal')
                    closeModal(modal)
                })
            })

            saveEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    eventArray.forEach(function(event, index) {
                        if((event.getDate(1) == text[2] || event.getDate(1) == "0" + text[2]) && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                            const date = document.getElementById("date"+index).value
                            const group = document.getElementById("group"+index).value
                            const description = document.getElementById("description"+index).value
                            changeEvent(date, group, description, index, eventArray)
                            const modal = button.closest('.event-modal')
                            closeModal(modal)
                        }
                    })
                })
            })
        }
    }, false)
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.event-modal')
        closeModal(modal)
    })
})

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')  
}

function addNewEvent(date, group, description, array) {
    if((date != "" && group != "") && description != "") {
        let event = new CalendarEvent(date, group, description)
        array.push(event)
    } else {
        handleError("date, group, and description must all be filled.")
    }
    renderCalendar(eventArray)
}

function deleteEvent(index, array) {
    array.splice(index, 1)
    renderCalendar(eventArray)
    closeModal(document.getElementsByClassName("event-modal")[0])
}

function changeEvent(date, group, description, index, array) {
    if((date != "" && group != "") && description != "") {
        array[index].setDate(date)
        array[index].setGroup(group)
        array[index].setDescription(description)
    } else {
        handleError("date, group, and description must all be filled.")   
    }
    renderCalendar(eventArray)
}

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
        addNewEvent(eventDate, "group", eventAssignment, eventArray)
    }
    renderCalendar(eventArray)
    $('.container').prepend("<div class='alert alert-success alert-dismissible fade show' role='alert'> <strong>Success</strong> - Syllabus successfully uploaded.<button type='button' class='close' data-dismiss='alert' aria-label='Close'> <span aria-hidden='true'>&times;</span> </button></div>")
}

function handleError(errorMessage) {
    // Show dismissible error message
    $('.container').prepend("<div id='error_message' class='alert alert-danger alert-dismissible fade show' role='alert'> <strong>Error</strong> - "+ errorMessage +"<button type='button' class='close' data-dismiss='alert' aria-label='Close'> <span aria-hidden='true'>&times;</span> </button></div>")
}

$('#file_form').change(function(e){
    var form_data = new FormData()
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    form_data.append('file', $('#file_input')[0].files[0])    
    
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
            handleError(data.statusText)
        } 
    })
    e.preventDefault()
})


function saveCalendar(){
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    events = JSON.stringify(eventArray)
    
    $.ajax({
        type:'POST',
        url:'/save_calendar',
        headers: {'X-CSRFToken': token},
        datatype: 'json',
        data : {
            'events': events
        },
    })
    .done(function(msg) {
        alert("Data saved " + msg)
    })
}