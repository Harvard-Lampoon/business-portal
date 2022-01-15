const ctx = document.getElementById('deal-chart').getContext('2d');
console.log(data)
const labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
console.log(labels)
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Value (Cash + Trade)',
        data: data,
        borderColor: '#713adb',
        backgroundColor: '#703adb8e',
        tension: .2,
      }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: "bottom"
            },
    }
}

});