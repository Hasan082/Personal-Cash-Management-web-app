document.addEventListener('DOMContentLoaded', function () {
  const data = window.dashboardData || {};

  const monthlyLabels = data.monthlyLabels || [];
  const monthlyIncome = data.monthlyIncome || [];
  const monthlyExpense = data.monthlyExpense || [];
  const topExpLabels = data.topExpLabels || [];
  const topExpValues = data.topExpValues || [];

  // Monthly chart
  try {
    const mcanvas = document.getElementById('monthlyChart');
    if (mcanvas && typeof Chart !== 'undefined') {
      const mctx = mcanvas.getContext('2d');
      new Chart(mctx, {
        type: 'bar',
        data: {
          labels: monthlyLabels,
          datasets: [
            { label: 'Income', data: monthlyIncome, backgroundColor: 'rgba(40,167,69,0.7)' },
            { label: 'Expense', data: monthlyExpense, backgroundColor: 'rgba(220,53,69,0.7)' }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: { y: { beginAtZero: true } }
        }
      });
    }
  } catch (e) {
    // fail silently but log for debugging
    console.error('Monthly chart init error', e);
  }

  // Top expenses donut
  try {
    const tcanvas = document.getElementById('topExpChart');
    if (tcanvas && typeof Chart !== 'undefined') {
      const tctx = tcanvas.getContext('2d');
      new Chart(tctx, {
        type: 'doughnut',
        data: { labels: topExpLabels, datasets: [{ data: topExpValues, backgroundColor: ['#007bff','#6610f2','#6f42c1','#20c997','#ffc107'] }] },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }
  } catch (e) {
    console.error('Top expenses chart init error', e);
  }
});
