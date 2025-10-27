// static/core/js/dashboard.js
const ctx = document.getElementById('scoreChart').getContext('2d');
const scoreChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: ['Week 1', 'Week 2', 'Week 3'],
    datasets: [{
        label: 'Average Score',
        data: [75, 80, 90],
        borderColor: '#2e86de',
        fill: false,
        tension: 0.1
    }]
    },
    options: {
    responsive: true,
    plugins: {
        title: {
        display: true,
        text: 'Your Performance Over Time'
        }
    }
    }
});
