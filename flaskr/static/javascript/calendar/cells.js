document.querySelectorAll(".cells").forEach(
    day => {
        day.addEventListener("click", event => {
            console.log(event.currentTarget)
            event.currentTarget.classList
                .toggle("selected")
            var name = event.currentTarget.cellIndex
            var date = event.currentTarget.getAttribute("data-date")
            var time = event.currentTarget.getAttribute("data-time")
            console.log(name)
            console.log(date)
            console.log(time)
        })
    }
)