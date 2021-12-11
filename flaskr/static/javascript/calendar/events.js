document.querySelectorAll(".events").forEach(event => {
        event.addEventListener("click", e => {
            console.log(e.currentTarget)

            event_id = e.currentTarget.innerHTML.trim()
            event_date = e.currentTarget.id.split("-")

            event_day = event_date[1]
            event_month = event_date[2]
            event_year = event_date[3]
            event_hour = Number(event_date[4])
            event_hour = event_hour < 10 ? "0" + event_hour + ":00" : event_hour + ":00"

            event_date = new Date(event_year + "/" + event_month + "/" + event_day)
            document.querySelector(".modal-body #event-name ").value = event_id
            document.querySelector(".modal-body #event-start-date ").valueAsDate = event_date
            document.querySelector(".modal-body #event-end-date ").valueAsDate = event_date
            document.querySelector(".modal-body #event-start-time ").value = event_hour
            document.querySelector(".modal-body #event-end-time ").value = event_hour
        })
    }
)