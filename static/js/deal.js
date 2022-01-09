var radios  = document.getElementsByName("action");
var extra_inputs = document.getElementById("extra_data")
for(let i = 0; i < radios.length; i ++){
    radios[i].addEventListener("change", function(event){
        var endpoint = this.getAttribute("endpoint");
        fetch(endpoint, {
            method: "GET",
        })
        .then(response => response.json())
        .then(result => {
          console.log(result)
            extra_inputs.innerHTML = result.html
            if (result.action = "select"){
              var element = document.querySelector('#companies');
              var choices = new Choices(element);
            }
        })
    })
}

var product_select = document.getElementById("product-select")
var product_data = document.getElementById("product-data")
product_select.addEventListener("change", (e)=>{
    var endpoint = product_select.getAttribute("endpoint")
    fetch(endpoint+"?type="+product_select.value, {
        method: "GET",
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        product_data.innerHTML = result.html
    })
})

function request(status){
    if(status=="pending"){
        return confirm("A request has already been sent out. Are you sure you want to send another?")
    }
    return true
}