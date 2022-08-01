function showRecurrenceCount()
{   
    if (document.getElementById("event-recurrence").value === "None")
    {
        document.getElementById("event-recurrence-count").hidden = true
        document.getElementById("event-recurrence-count-label").hidden = true
    }
    else
    {
        document.getElementById("event-recurrence-count").hidden = false
        document.getElementById("event-recurrence-count-label").hidden = false
    }
    
}