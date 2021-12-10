document.querySelectorAll(".cells").forEach(
    day => {
        day.addEventListener("click", event => {
            console.log(event.currentTarget);
            event.currentTarget.classList
                .toggle("selected")
            var name = null
            if(event.currentTarget.hasChildNodes()){
                var cell = event.currentTarget.childNodes[0]
                console.log(cell)
                name = cell.innerHTML
            }
            else{
                name = event.currentTarget.innerHTML
            }

            var date = event.currentTarget.getAttribute("data-date")
            var time = event.currentTarget.getAttribute("data-time")
            console.log(name)
            console.log(date)
            console.log(time)
        })
    }
)