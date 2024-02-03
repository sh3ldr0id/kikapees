let isFuture = document.querySelector("#future")

isFuture.addEventListener("change", clicked)

function clicked() {

    console.log(isFuture.checked)
    document.querySelector("#due").addAttribute("disabled")
}