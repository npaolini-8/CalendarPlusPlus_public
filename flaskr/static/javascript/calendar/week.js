document.querySelectorAll("#days").forEach(
    day => {
        day.addEventListener("click", event => {
            console.log(event.currentTarget)
            event.currentTarget.classList.toggle("bg-info")
        })
    }
)