var row_links = document.getElementsByClassName("table-link")
for(let i = 0; i < row_links.length; i++){
  row_links[i].addEventListener("click", (e)=>{
    window.location.href = row_links[i].getAttribute("link")
  })
}