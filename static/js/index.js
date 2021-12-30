const ctx = document.getElementById('deal-chart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [{
        label: 'Total $ Value',
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
            }
    }
}

});