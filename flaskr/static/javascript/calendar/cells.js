document.querySelectorAll(".cells").forEach(
    day => {
        day.addEventListener("click", event => {
            console.log(event.currentTarget);
            event.currentTarget.classList
                .toggle("selected")

            var event_div = event.currentTarget.querySelector(".events")
            if(event_div != null|undefined){
                event_id = event_div.innerHTML
                event_date = (event_div.id).split("-")
                event_day = event_date[0].substring(4)
                event_month = event_date[1]
                event_year = event_date[2]
                event_hour = event_date[3]
            }
            else{
                event_id = event.currentTarget.getAttribute("id")
                event_date = event.currentTarget.getAttribute("id")
                event_time = event.currentTarget.getAttribute("id")
            }

            console.log(event_id)
            console.log(event_date)
        })
    }
)