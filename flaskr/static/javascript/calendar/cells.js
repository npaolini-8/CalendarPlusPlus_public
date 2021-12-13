document.querySelectorAll(".cells").forEach(cell => {
        cell.addEventListener("click", (e) => {
            console.log(e.currentTarget)
            const cell_id = e.currentTarget.id
            const event_div = e.currentTarget.querySelector(".events")
            const current_page = document.location.pathname.split("/")[2]

            if(current_page == "month"){
                window.location.href = "http://127.0.0.1:5000/calendar/day/" //TODO fix routing to proper day
            }

            // if event_div is not empty, parse the events and display them
            if(event_div != null|undefined) {
                myModal = new bootstrap.Modal(document.getElementById("event-dialog-modal"))
                document.getElementById("event-dialog-update").onclick = () => {
                    the_event = event_div.id.split(",")         
                    event_id = the_event[0]
                    start_year = the_event[1]
                    start_month = the_event[2]
                    start_day = the_event[3]
                    start_hour = the_event[4]
                    start_min = the_event[5]
                    end_year = the_event[6]
                    end_month = the_event[7]
                    end_day = the_event[8]
                    end_hour = the_event[9]
                    end_min = the_event[10]
                    event_desc = the_event[11]//all event values populated
                    event_loc = the_event[12]
                    
                    start_min = Number(start_min)
                    start_min = start_min < 10 ? start_min + "0" : String(start_min)

                    start_hour = Number(start_hour) 
                    start_time = start_hour < 10 ? "0" + start_hour + ":" + start_min : start_hour + ":" + start_min

                    end_hour = Number(end_hour)
                    end_time = end_hour < 10 ? "0" + end_hour + ":" + end_min : end_hour + ":" + end_min


                    document.querySelector(".modal-body #event-start-time ").value = start_time
                    document.querySelector(".modal-body #event-end-time ").value = end_time

                    start_date = new Date(start_year + "/" + start_month + "/" + start_day)
                    end_date = new Date(end_year + "/" + end_month + "/" + end_day)
                    document.querySelector(".modal-body #event-name ").value = event_id
                    document.querySelector(".modal-body #event-start-date ").valueAsDate = start_date
                    document.querySelector(".modal-body #event-end-date ").valueAsDate = end_date
                    document.querySelector(".modal-body #event-description").value = event_desc
                    document.querySelector(".modal-body #event-location").value = event_loc

                    document.querySelector(".modal-footer #old-title ").value = event_id
                    document.querySelector(".modal-footer #old-start-time ").value = start_time
                    document.querySelector(".modal-footer #old-end-time ").value = end_time
                    document.querySelector(".modal-footer #old-start-date ").valueAsDate = start_date
                    document.querySelector(".modal-footer #old-end-date ").valueAsDate = end_date

                    document.getElementById("event-save").hidden = true
                    document.getElementById("event-update").hidden = false
                    document.getElementById("event-delete").hidden = false
                    document.getElementById("event-recurrence").hidden = true
                    document.getElementById("event-recurrence-label").hidden = true

                    document.getElementById("old-title").hidden = true
                    document.getElementById("old-start-time").hidden = true
                    document.getElementById("old-end-time").hidden = true
                    document.getElementById("old-start-date").hidden = true
                    document.getElementById("old-end-date").hidden = true
               }

               document.getElementById("event-dialog-add").onclick = () => {
                    reset(cell_id)
               }
            }
            else{
                myModal = new bootstrap.Modal(document.getElementById("event-modal"))
                reset(cell_id)


            }
            myModal.show()
        })
    }
)

function reset(cell_id) {
    cell_date = cell_id.split("-")
    cell_day = cell_date[1]
    cell_month = cell_date[2]
    cell_year = cell_date[3]
    cell_date = new Date(cell_year + "/" + cell_month + "/" + cell_day)

    document.querySelector(".modal-body #event-name ").value = ""
    document.querySelector(".modal-body #event-start-date ").valueAsDate = cell_date
    document.querySelector(".modal-body #event-end-date ").valueAsDate = cell_date
    document.querySelector(".modal-body #event-start-time ").value = "00:00"
    document.querySelector(".modal-body #event-end-time ").value = "00:00"
    document.querySelector(".modal-body #event-description").value = ""
    document.querySelector(".modal-body #event-location").value = ""
    document.getElementById("event-save").hidden = false
    document.getElementById("event-update").hidden = true
    document.getElementById("event-delete").hidden = true
    document.getElementById("event-recurrence").hidden = false
    document.getElementById("event-recurrence-label").hidden = false

    document.getElementById("old-title").hidden = true
    document.getElementById("old-start-time").hidden = true
    document.getElementById("old-end-time").hidden = true
    document.getElementById("old-start-date").hidden = true
    document.getElementById("old-end-date").hidden = true
}
