document.querySelectorAll(".cells").forEach(cell => {
        cell.addEventListener("click", event => {
            console.log(event.currentTarget)
            const current_page = document.location.pathname.split("/")[2]

            if (current_page == 'month') {
                window.location = "http://127.0.0.1:5000/calendar/day/"
            }

            // if event_div is not empty, parse the events and display them

            cell_date = cell.id.split("-")

            cell_day = cell_date[1]
            cell_month = cell_date[2]
            cell_year = cell_date[3]
            cell_hour = Number(cell_date[4])
            cell_hour = cell_hour < 10 ? "0" + cell_hour + ":00" : cell_hour + ":00"

            cell_date = new Date(cell_year + "/" + cell_month + "/" + cell_day)
            document.querySelector(".modal-body #event-name ").value = ""
            document.querySelector(".modal-body #event-start-time ").value = cell_hour
            document.querySelector(".modal-body #event-end-time ").value = cell_hour
            document.querySelector(".modal-body #event-start-date ").valueAsDate = cell_date
            document.querySelector(".modal-body #event-end-date ").valueAsDate = cell_date
        })
    }
)