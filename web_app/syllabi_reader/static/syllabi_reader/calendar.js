//Heavily inspired by Code and Create https://www.youtube.com/watch?v=o1yMqPyYeAo&t=1135s

//Things to do:
    //export to ics
    //handle invalid inputs from the user when creating events
        //Currently only checks if the day is equal to or less than 31 so it lets some invalid dates on months with less than 31 days.
        //I challenge you to try and break it!
    //Make sure the code properly handles each syllabus

    //Anything else...

//Class which defines events that will be added to the calendar
class CalendarEvent {

    constructor(date, description) {
        this.setDate(date)
        this.setDescription(description)
    }
   
    setDate(date) {
        let dateArray = date.split('/')
        dateArray[0] = dateArray[0] - 1;
        //this is a quick fix for error handling. Doesn't work if there is a month that has less than 31 days**********
        if((dateArray[0] < 12 && dateArray[1] <= 31) && (dateArray[2] != undefined)) {
            this.date = dateArray;
        } else {
            displayErrorMsg("Date invalid, try mm/dd/yyyy")
        }
    }

    setDescription(description) {
        this.description = description
    }

    getDate(index) {
        if(index < this.date.length) {
            return this.date[index]
        }
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
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i} today date">${i + " " + `<p>${dailyEvents}</p>`}</div>`
            
        }else{
            //loops through the events array
            eventArray.forEach(function(event) {
                //true if the event date matches the current date of the for loop
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                    dailyEvents += event.getDescription() + "<br>"
                }
            })
            days += `<div class = "${date.getFullYear()} ${months[date.getMonth()]} ${i} date">${i + " " + `<p>${dailyEvents}</p>`}</div>`
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
        e = e || window.event
        let target = e.target.closest('.date')
        console.log(target)
        let text = target.classList
        const modal = document.querySelector(button.dataset.modalTarget)
        document.getElementById("title").innerHTML = text[1] + " " + text[2] + ", " + text[0]

        //generates the text boxes and buttons on the popup for the specified day based on the events on that day
        let dailyEvents = ""
        let eventFound = false
        eventArray.forEach(function(event, index) {
            if((event.getDate(1) == text[2] || event.getDate(1) == "0" + text[2]) && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                eventFound = true
                dailyEvents += `<div class="event-section">
                                    <b>Event</b>
                                    <label class="omrs-input-underlined">
				                        <input required id="date${index}" value="${(event.getDate(0) + 1) + "/" + text[2] + "/" + event.getDate(2)}">
				                        <span class="omrs-input-label">Date</span>
					                    <span class="omrs-input-helper">mm/dd/yyyy</span>
				                    </label>
                                    <label class="omrs-input-underlined">
				                        <input required id="description${index}" value="${event.getDescription()}">
				                        <span class="omrs-input-label">Description</span>
				                    </label>
                                    <button data-event-delete${index} id="delete-event${index}" onclick="deleteEvent(${index}, eventArray)">Delete Event</button>
                                </div>`
            }
        })
        if(eventFound) {
            dailyEvents += `<button data-event-save id="save-events">Save Events</button>`
        }
        dailyEvents += `<div class="event-section">
                            <b>Add Event</b>
                            <label class="omrs-input-underlined">
				                <input required id="add-date" value="${(months.indexOf(text[1]) + 1) + "/" + text[2] + "/" + text[0]}">
				                <span class="omrs-input-label">Date</span>
                                <span class="omrs-input-helper">mm/dd/yyyy</span>
				            </label>
                            <label class="omrs-input-underlined">
				                <input required id="add-description">
				                <span class="omrs-input-label">Description</span>
				            </label>
                            <button data-event-add id="add-event">Add Event</button>
                        </div>`


        document.getElementById("event-modal-body").innerHTML = dailyEvents

        //section that actually opens the modal
        if(text[0] != "next-date" && text[0] != "prev-date" && text[0] != "days") {
            openModal(modal)

            const createEventButton = document.querySelectorAll("[data-event-add]")
            const saveEventButton = document.querySelectorAll("[data-event-save]")

            createEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    const date = document.getElementById("add-date").value
                    const description = document.getElementById("add-description").value
                    addNewEvent(date, description, eventArray)
                    const modal = button.closest('.event-modal')
                    closeModal(modal)
                })
            })

            saveEventButton.forEach(button => {
                button.addEventListener('click', () => {
                    eventArray.forEach(function(event, index) {
                        if((event.getDate(1) == text[2] || event.getDate(1) == "0" + text[2]) && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                            const date = document.getElementById("date"+index).value
                            const description = document.getElementById("description"+index).value
                            changeEvent(date, description, index, eventArray)
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

function addNewEvent(date, description, array) {
    if(date != "" && description != "") {
        //this is a quick fix for error handling. Doesn't work if there is a month that has less than 31 days**********
        let dateArray = date.split('/')
        dateArray[0] = dateArray[0] - 1;
        if((dateArray[0] < 12 && dateArray[1] <= 31) && (dateArray[2] != undefined)) {
            let event = new CalendarEvent(date, description)
            array.push(event)
        } else {
            displayErrorMsg("Date invalid, try mm/dd/yyyy")
        }
        
        
    } else {
        displayErrorMsg("date and description must all be filled.")
    }
    renderCalendar(eventArray)
}

function deleteEvent(index, array) {
    array.splice(index, 1)
    renderCalendar(eventArray)
    closeModal(document.getElementsByClassName("event-modal")[0])
}

function changeEvent(date, description, index, array) {
    if(date != "" && description != "") {
        array[index].setDate(date)
        array[index].setDescription(description)
    } else {
        displayErrorMsg("date and description must all be filled.")   
    }
    renderCalendar(eventArray)
}


function handleResponse(obj) {  
    // It accepts a dictionary an iterates through its elements

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
        addNewEvent(eventDate, eventAssignment, eventArray)
    }
    renderCalendar(eventArray)
    $('.container').ready(function() {
        $('.container').prepend("<div class='alert alert-success alert-dismissible fade show' role='alert'> <strong>Success</strong> - Syllabus successfully uploaded.<button type='button' class='close' data-dismiss='alert' aria-label='Close'> <span aria-hidden='true'>&times;</span> </button></div>")
        $(".alert").first().hide().slideDown(500).delay(4000).slideUp(500, function () {
           $(this).remove(); 
        });
    });
    
}

function displayErrorMsg(errorMessage) {
    // Show dismissible error message
    $('.container').ready(function() {
        $('.container').prepend("<div id='error_message' class='alert alert-danger alert-dismissible fade show' role='alert'> <strong>Error</strong> - "+ errorMessage +"<button type='button' class='close' data-dismiss='alert' aria-label='Close'> <span aria-hidden='true'>&times;</span> </button></div>")
        $(".alert").first().hide().slideDown(500).delay(4000).slideUp(500, function () {
           $(this).remove(); 
        });
    });
}

$('#file_form').change(function(e){
    // When the input changes, it posts the file uploaded
    // and handles the response.

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
            displayErrorMsg(data.statusText)
        } 
    })
    e.preventDefault()
})

function promptDownload(res, filename){
    // Gets a response with a file and prompts it download
    var downloadLink = document.createElement("a");
    var blob = new Blob(["\ufeff", res]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

function handleDownload(route, filename){
    if (eventArray.length == 0) {
        displayErrorMsg("You cannot export an empty calendar.")
        return
    }

    // Token necessary to make posts requests in Django
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    
    // Transforming the array of events to a string
    // in order to send it in the request
    events = JSON.stringify(eventArray)
    
    // Ajax request to the backend
    $.ajax({
        type:'POST',
        url: route,
        headers: {'X-CSRFToken': token}, // Appending the token to the ajax request
        datatype: 'json',
        data : {
            'events': events // Appending the events to the request
        },
    })
    .done(function(res) {   
        promptDownload(res, filename)
    })
}


function saveInCsv(){
    handleDownload("/save_csv", "calendar.csv")
}



function saveInIcs(){
    handleDownload("/save_ics", "calendar.ics")
}