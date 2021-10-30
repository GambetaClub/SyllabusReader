class CalendarEvent {
    date = null;
    group = "";
    description = "";

   constructor(date, group, description) {
       this.date = date;
       this.group = group;
       this.description = description;
   }

   //methods
   setDate(date) {
       this.date = date;
   }

   setGroup(group) {
       this.group = group;
   }

   setDescription(description) {
       this.description = description;
   }

   getDate() {
       return this.date;
   }

   getGroup() {
       return this.group;
   }

   getDescription() {
       return this.description;
   }
}
let eventArray = [new CalendarEvent(13, "class", "test")];