document.querySelectorAll(".cells").forEach(day => {
        day.addEventListener("click", event => {
            console.log(event.currentTarget)
            const event_div = event.currentTarget.querySelector(".events")
            const current_page = document.location.pathname.split("/")[2]

            // if event_div is not empty, parse the events and display them
            if(event_div != null|undefined) {
                var myModal = new bootstrap.Modal(document.getElementById("event-dialog-modal"))
                myModal.show()

               if(document.getElementById("event-dialog-update").clicked ==true)
                event_id = event_div.innerHTML.trim()
                event_date = event_div.id.split("-")
                console.log(event_date)
                event_day = event_date[1]
                event_month = event_date[2]
                event_year = event_date[3]

                if(current_page != "month") {
                    event_hour = Number(event_date[3]) % 12
                    event_hour = event_hour < 10 ? "0" + event_hour + ":00" : event_hour + ":00"

                    document.querySelector(".modal-body #event-start-time ").value = event_hour
                    document.querySelector(".modal-body #event-end-time ").value = event_hour
                }

                event_date = new Date(event_year + "/" + event_month + "/" + event_day)
                document.querySelector(".modal-body #event-name ").value = event_id
                document.querySelector(".modal-body #event-start-date ").valueAsDate = event_date
                document.querySelector(".modal-body #event-end-date ").valueAsDate = event_date
                document.getElementById("event-save").hidden = true
                document.getElementById("event-update").hidden = false
            }
            else{
                document.querySelector(".modal-body #event-name ").value = ""
                document.querySelector(".modal-body #event-start-date ").valueAsDate = new Date()
                document.querySelector(".modal-body #event-end-date ").valueAsDate = new Date()
                document.querySelector(".modal-body #event-start-time ").value = "00:00"
                document.querySelector(".modal-body #event-end-time ").value = "00:00"
                document.getElementById("event-save").hidden = false
                document.getElementById("event-update").hidden = true
            }
        })
    }
)