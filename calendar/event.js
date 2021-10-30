let event = {
    date:20213001,
    group:"group name",
    description:"description",

    //methods
    setDate : function(date) {
        this.date = date;
    },

    setGroup : function(group) {
        this.group = group;
    },

    setDescription : function(description) {
        this.description = description;
    },

    getDate : function() {
        return this.date;
    },

    getGroup : function() {
        return this.group;
    },

    getDescription : function() {
        return this.description;
    },
}