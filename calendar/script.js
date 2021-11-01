//Heavily inspired by Code and Create https://www.youtube.com/watch?v=o1yMqPyYeAo&t=1135s
class CalendarEvent {

    constructor(date, group, description) {
        this.setDate(date)
        this.setGroup(group);
        this.setDescription(description);
    }
   
    setDate(date) {
        let dateArray = date.split('/')
        dateArray[0] = dateArray[0] - 1;
        this.date = dateArray;
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
    
}

const date = new Date();
const importButton = document.querySelector('.import');
const renderCalendar = (eventArray) => {
    
    date.setDate(1);

    const monthDays = document.querySelector('.days');

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();

    const nextDays = 7 - lastDayIndex - 1;

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

    //displays the information in the header
    document.querySelector('.date h1').innerHTML = months[date.getMonth()];

    document.querySelector('.year').innerHTML = date.getFullYear();

    document.querySelector('.date p').innerHTML = new Date().toDateString();

    let days = "";

    for(let x = firstDayIndex; x > 0; x--){
        days += `<div class = "prev-date">${prevLastDay - x + 1}</div>`
    }

    //displays the days
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
            days += `<div class = "today">${i + " " + `<p>${dailyEvents}</p>`}</div>`;
            
        }else{
            //loops through the events array
            eventArray.forEach(function(event) {
                //true if the event date matches the current date of the for loop
                if(event.getDate(1) == i && (event.getDate(0) == date.getMonth() && event.getDate(2) == date.getFullYear())) {
                    dailyEvents += event.getDescription() + "<br>";
                }
            })
            days += `<div>${i + " " + `<p>${dailyEvents}</p>`}</div>`;
        }
    }

    for(let j = 1; j <= nextDays; j++){
        days += `<div class = "next-date">${j}</div>`;
    }
    monthDays.innerHTML = days;

}

let event1 = new CalendarEvent("10/27/2021", "group", "a nice description1");


let eventArray = [event1];

document.querySelector('.prev').addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar(eventArray);
});

document.querySelector('.next').addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar(eventArray);
});

document.querySelector('.import').addEventListener('click', () => {
});

renderCalendar(eventArray);


//popup when clicking on a day
const openModalButtons = document.querySelectorAll("[data-modal-target]");
const closeModalButtons = document.querySelectorAll("[data-close-button]")

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
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

function findEvent(date, group, description, array) {
    let index
    array.forEach(function(item, i) {
        console.log(item.getDate(0)==date[0])
        console.log(item.getDate(1)==date[1] && item.getDate(2)==date[2])
        console.log(item.getGroup()==group && item.getDescription()==description)
        console.log((item.getDate(1)==date[1] && item.getDate(2)==date[2]) && (item.getGroup()==group && item.getDescription()==description))
        console.log(item.getDate(0)==date[0] && ((item.getDate(1)==date[1] && item.getDate(2)==date[2]) && (item.getGroup()==group && item.getDescription()==description)))
        console.log("date0 " + item.getDate(0) + ":" + date[0] + " date1 " + item.getDate(1) + ":" + date[1] + " date2 " + item.getDate(2) + ":" + date[2] + " description " + item.getDescription() + ":" + description + " group " + item.getGroup() + " " + group)
        if(item.getDate(0)==date[0] && ((item.getDate(1)==date[1] && item.getDate(2)==date[2]) && (item.getGroup()==group && item.getDescription()==description))) {
            index = i;
        }
    })
    return index;
}

function deleteEvent(index, array) {
    array.splice(index)
}

const createEventButton = document.querySelectorAll("[data-event-add]")
const deleteEventButton = document.querySelectorAll("[data-event-delete]")
const changeEventButton = document.querySelectorAll("[data-event-change]")

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

deleteEventButton.forEach(button => {
    button.addEventListener('click', () => {
        let date = document.getElementById("find-date").value.split('/')
        date[0] = date[0]-1;
        console.log("delete: " + date)
        const group = document.getElementById("find-group").value
        console.log("delete: "+ group)
        const description = document.getElementById("find-description").value
        console.log("delte: "+description)
        let index = findEvent(date, group, description, eventArray)
        console.log(index)
        if(index != null) {
            deleteEvent(index, eventArray)
            renderCalendar(eventArray);
            const modal = button.closest('.modal')
            closeModal(modal)
        }
    })
})

changeEventButton.forEach(button => {
    button.addEventListener('click', () => {
        const date = document.getElementById("add-date").value
        console.log(date)
        const group = document.getElementById("add-group").value
        console.log(group)
        const description = document.getElementById("add-description").value
        console.log(description)
    })
})
