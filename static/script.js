document.addEventListener("DOMContentLoaded", function () {

    const utcElements = document.querySelectorAll(".utc-time");


    // Auto-dismiss flash messages
    const flash = document.querySelector(".flash-success");
    if (flash) {
        setTimeout(() => {
            flash.style.display = "none";
        }, 4000);
    }

    // Chart rendering logic
    const canvas = document.getElementById('budgetChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');

        // Parse data from canvas attributes
        const labelsJSON = canvas.getAttribute('data-labels');
        const valuesJSON = canvas.getAttribute('data-values');

        const labels = JSON.parse(labelsJSON);
        const values = JSON.parse(valuesJSON);

        const data = {
            labels: labels,
            datasets: [{
                label: 'Budget Overview',
                data: values,
                backgroundColor: ['#00cc99', '#ff6666'],
                hoverOffset: 4
            }]
        };

        const config = {
            type: 'pie',
            data: data,
        };

        new Chart(ctx, config);
    }
    $(".hamburger").click(function () {
        $("#nav-links").toggleClass("show-nav");
    });
    $(document).click(function (event) {
        if (!$(event.target).closest(".hamburger, #nav-links").length) {
            $("#nav-links").removeClass("show-nav");
        }
    });
});
