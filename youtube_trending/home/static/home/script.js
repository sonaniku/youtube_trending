data_btn = document.getElementById("data_btn")
dashboard_btn = document.getElementById("dashboard_btn")

dashboard1 = document.getElementById("dashboard1")
dashboard2 = document.getElementById("dashboard2")

console.log(data_btn)
console.log(dashboard_btn)

data_btn.onclick = function() {
    dashboard1.style.display = "block"
    dashboard2.style.display = "none"

}

dashboard_btn.onclick = function() {
    dashboard1.style.display = "none"
    dashboard2.style.display = "block"

}