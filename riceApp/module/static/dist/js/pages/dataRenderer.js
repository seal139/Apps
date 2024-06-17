function formatNum(num, place) {
    return num.toFixed(place).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",").replace(/(\.\d{2})\d+$/, "$1");
}

var chartOptions = {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
        display: true,
        labels: {
        fontColor: '#efefef'
    }
    },
    scales: {
        xAxes: [{
            ticks: {
            fontColor: '#efefef',
            stepSize: 3
            },
            gridLines: {
                display: false,
            },
        }],
        yAxes: [{
            ticks: {
                fontColor: '#efefef'
            },
            gridLines: {
                display: true,
                color: '#efefef',
                drawBorder: false
            }
        }]
    }
}

function updateStockTable(data) {
    if(data.data == null){
        return;
    }

    $('#stock-table').DataTable().destroy();                
    $('#stock-table').DataTable( {
        data: data.data.historical,
        pageLength: 5,
        dom: 'frtip',
        columns: [
            { data: 'id', visible: false },
            { data: 'year', type: 'num' },
            { data: 'month', type: 'num' },
            { data: 'avgStock', type: 'num' }
        ],
        order: [[0, 'desc']],
        columnDefs: [
            {
                targets: 3,
                render: function(data, type, row) {
                    return formatNum(data, 2);
                }
            }
        ],
    } );
}

function updatePopulationConsumptionTable(data){
    if(data.data == null){
        return;
    }

    $('#population-consumption-table').DataTable().destroy();
    $('#population-consumption-table').DataTable( {
        data: data.data.historical,
        pageLength: 5,
        dom: 'frtip',
        columns: [
            { data: 'id', visible: false },
            { data: 'year', type: 'num' },
            { data: 'population', type: 'num' },
            { data: 'consumptionRate', type: 'num' }
        ],
        order: [[0, 'desc']],
        columnDefs: [
            {
                targets: 2,
                render: function(data, type, row) {
                    return formatNum(data, 0);
                }
            },
            {
                targets: 3,
                render: function(data, type, row) {
                    return formatNum(data, 2);
                }
            }
        ],
    } );
}

function refresh() {
    var request1 = $.ajax({
        url: '../api/fetch-stock/',
        type: 'GET',
        dataType: 'json'
    });

    var request2 = $.ajax({
        url: '../api/fetch-consumption/',
        type: 'GET',
        dataType: 'json'
    });

    $.when(request1, request2).then(function(response1, response2) {
        var stock                  = response1[0];
        var consumption_population = response2[0];

        $.ajax({
            success: function() {                        
                updatePopulationGraph(consumption_population);
            }
        });

        $.ajax({
            success: function() {
                updateConsumptionGraph(consumption_population);                        
            }
        });

        $.ajax({
            success: function() {                        
                updatePopulationConsumptionTable(consumption_population);
            }
        });
        
        $.ajax({
            success: function() {
                updateStockGraph(stock);                        
            }
        }); 

        $.ajax({
            success: function() {                        
                updateStockTable(stock);
            }
        });    

        if(stock.data == null){
            return;
        }

        if(consumption_population.data == null){
            return;
        }

        var historicalData = consumption_population.data.historical;
        var stockData      = stock.data.historical;

        var population1  = historicalData[historicalData.length - 1].population;
        var population2  = consumption_population.data.prediction[0].population;
        var consumption  = consumption_population.data.prediction[0].consumptionRate;

        var growthRate      = formatNum((population2 - population1) / population1 * 100, 2);
        var consumptionRate = formatNum((consumption / population2) * 1000, 2);
        var dailyNeed       = formatNum(consumption / 365, 2) ;
        var stockLeft       = formatNum(stockData[stockData.length - 1].avgStock / (consumption / 365), 0);

        var forecast  = consumption_population.data.prediction
        var stockData = stock.data.prediction;

        var consumptionFactor1 = (forecast[0].consumptionRate) / 12;
        var consumptionFactor2 = (forecast[1].consumptionRate) / 12;

        var populationFactor1 = (forecast[0].population - historicalData[historicalData.length - 1].population) / 12;        
        var populationFactor2 = (forecast[1].population - forecast[0].population) / 12

        const populationMap   = new Map();
        const vpopulationMap  = new Map();
        const vconsumptionMap = new Map();

        populationMap.set(forecast[0].year, historicalData[historicalData.length - 1].population);
        populationMap.set(forecast[1].year, forecast[0].population);

        vpopulationMap.set(forecast[0].year, populationFactor1);
        vpopulationMap.set(forecast[1].year, populationFactor2);

        vconsumptionMap.set(forecast[0].year, consumptionFactor1);
        vconsumptionMap.set(forecast[1].year, consumptionFactor2);
        
        const compisiteData = [];
        stockData.forEach(stockItem => {
            population  = populationMap.get(stockItem.year);

            populationFactor  = vpopulationMap.get(stockItem.year);
            consumptionFactor = vconsumptionMap.get(stockItem.year);

            const newRow = {
                id: stockItem.id,
                year: stockItem.year,
                month: stockItem.month,
                stock: stockItem.avgStock,
                population: population + (populationFactor * stockItem.month),
                consumption: consumptionFactor * stockItem.month
            };
            compisiteData.push(newRow);
        });

        $('#daily-needs-value').html(dailyNeed + '<sup style="font-size: 20px">tons</sup>')
        $('#growth-value').html(growthRate + '<sup style="font-size: 20px">%</sup>')
        $('#consumption-value').html(consumptionRate + '<sup style="font-size: 20px">kg</sup>')
        $('#stock-value').html(stockLeft + '<sup style="font-size: 20px">days</sup>')
    
        $('#daily-needs-caption').html(
            'Current annual consumption rate is predicted at ' + formatNum(consumption, 2) + ' tons.'+
            ' Estimated daily rice needs is around ' + dailyNeed + ' tons or ' + formatNum(consumption / 12, 2) + ' tons per month.<br/>' +
            'This value can be used as a minimum threshold for rice stock.'
        );
        
        $('#growth-caption').html(
            'Compared to previous year, current year population growth is predicted at around ' + growthRate + '% or about ' + 
            formatNum(population2, 0) + ' in total. ' +
            'This value can significantly influence annual consumption and daily rice needs.'
        );

        $('#consumption-caption').html(
            'Consumption per individual per year is around ' + consumptionRate + ' kg by dividing annual rice needs by total population'
        );

        $('#stock-caption').html(
            'Last month\'s stock is ' + formatNum(stockData[stockData.length - 1].avgStock, 2) + 
            ' tons. If left without any stock in, it will be sufficient for around ' + 
            stockLeft + ' days before runs out (referring to daily needs).'
        );

        $('#forecast-table').DataTable().destroy();                
        $('#forecast-table').DataTable( {
            layout: {
                topStart: {
                    buttons: ['csv']
                }
            },
            dom: 'frtip',
            bInfo : false,
            bPaginate : false,
            bLengthChange : false,
            data: compisiteData,
            pageLength: 25,
            columns: [
                { data: 'id', type: 'num', visible: false },
                { data: 'year', type: 'num' },
                { data: 'month', type: 'num' },                    
                { data: 'population', type: 'num' },
                { data: 'consumption', type: 'num' },
                { data: 'stock', type: 'num' }
            ],
            order: [[0, 'desc']],
            columnDefs: [
                {
                    targets: 3,
                    render: function(data, type, row) {
                        return formatNum(data, 0);
                    }
                },
                {
                    targets: 4,
                    render: function(data, type, row) {
                        return formatNum(data, 2);
                    }
                },
                {
                    targets: 5,
                    render: function(data, type, row) {
                        return formatNum(data, 2);
                    }
                }
            ],
        });
    });
}

function updatePopulationGraph(data){
    if(data.data == null){
        return;
    }

    $('#population-parent-div').html(
        '<h4 class="card-title">'+
        '   <b>Population - in millions</b>'+
        '</h4> '+
        '<canvas class="chart" id="population-chart" style="min-height: 250px; height: 250px; max-height: 250px; max-width: 100%;"></canvas>'
    )

    var chartCanvas = $('#population-chart').get(0).getContext('2d')

    const historicalYears = data.data.historical.map(item => item.year).slice(-10);
    const predictionYears = data.data.prediction.map(item => item.year);

    const historicalPopulation = data.data.historical.map(item => (item.population / 1000000).toFixed(2)).slice(-10);
    const predictionPopulation = new Array(historicalPopulation.length - 1)
                                .fill(null)
                                .concat(historicalPopulation[historicalPopulation.length - 1])
                                .concat(data.data.prediction.map(item => (item.population / 1000000).toFixed(2)));

    var chartData = {
        labels: [...historicalYears, ...predictionYears],
        datasets: [
            {
                label: 'Histrorical',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: historicalPopulation
            },
            {
                borderDash: [3, 3],
                label: 'Prediction',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: predictionPopulation,
            }
        ]
    };

    var graphChart = new Chart(chartCanvas, {
        type: 'line',
        data: chartData,
        options: chartOptions
    });
}

function updateConsumptionGraph(data) {
    if(data.data == null){
        return;
    }

    $('#consumption-parent-div').html(
        '<h4 class="card-title">'+
        '    <b>Consumption Rate - in thousand tons</b>'+
        '</h4>'+  
        '<canvas class="chart" id="consumption-chart" style="min-height: 250px; height: 250px; max-height: 250px; max-width: 100%;"></canvas>'
    )

    var chartCanvas = $('#consumption-chart').get(0).getContext('2d')

    const historicalYears = data.data.historical.map(item => item.year).slice(-10);
    const predictionYears = data.data.prediction.map(item => item.year);

    const historicalConsumption = data.data.historical.map(item => (item.consumptionRate / 1000).toFixed(2)).slice(-10);
    const predictionConsumption = new Array(historicalConsumption.length - 1)
                                .fill(null)
                                .concat(historicalConsumption[historicalConsumption.length - 1])
                                .concat(data.data.prediction.map(item => (item.consumptionRate / 1000).toFixed(2)));

    var chartData = {
        labels: [...historicalYears, ...predictionYears],
        datasets: [
            {
                label: 'Historical',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: historicalConsumption
            },
            {
                borderDash: [3, 3],
                label: 'Prediction',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: predictionConsumption
            }
        ]
    };

    var graphChart = new Chart(chartCanvas, { // lgtm[js/unused-local-variable]
        type: 'line',
        data: chartData,
        options: chartOptions
    });
}

function updateStockGraph(data) {
    if(data.data == null){
        return;
    }

    $('#stock-parent-div').html(
        '<h4 class="card-title">'+
        '    <b>Average Stock - in thousand tons</b>'+
        '</h4>'+  
        '<canvas class="chart" id="stock-chart" style="min-height: 250px; height: 250px; max-height: 250px; max-width: 100%;"></canvas>'
    )

    
    var chartCanvas = $('#stock-chart').get(0).getContext('2d')

    const historicalYears = data.data.historical.map(item => item.year * 100 + item.month).slice(-18);
    const predictionYears = data.data.prediction.map(item => item.year * 100 + item.month);

    const historicalStock = data.data.historical.map(item => (item.avgStock / 1000).toFixed(2)).slice(-18);
    const predictionStock = new Array(historicalStock.length - 1)
                                .fill(null)
                                .concat(historicalStock[historicalStock.length - 1])
                                .concat(data.data.prediction.map(item => (item.avgStock / 1000).toFixed(2)));

    var chartData = {
        labels: [...historicalYears, ...predictionYears],
        datasets: [
            {
                label: 'Historical',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: historicalStock
            },
            {
                borderDash: [3, 3],
                label: 'Prediction',
                fill: true,
                backgroundColor: 'rgba(0, 0, 0, .25)',
                borderWidth: 3,
                lineTension: 0,
                spanGaps: true,
                borderColor: '#efefef',
                pointRadius: 3,
                pointHoverRadius: 7,
                pointColor: '#efefef',
                pointBackgroundColor: '#efefef',
                data: predictionStock
            }
        ]
    };

    var graphChart = new Chart(chartCanvas, {
        type: 'line',
        data: chartData,
        options: chartOptions
    });
}    

$(function () {
    
    refresh();

    $('input[type="file"]').on('change',function(e){
        var fileName = e.target.files[0].name;
        $('.custom-file-label[for="'+ $(this).attr("id") +'"]').text(fileName);
    });

    $('.datatables').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
    });

    $('form').submit(function(e) {
        e.preventDefault();

        var form = this;
        var formData = new FormData(form);
        $.ajax({
            url: form.action,
            method: 'post',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
                
                $(document).Toasts('create', {
                    class: 'bg-info',
                    title: 'Processing',
                    subtitle: '',
                    body: 'Please wait while server processing your data',
                    autohide: true,
                    delay: 6000 
                });
                $('.modal').modal('hide');
            },
            success: function(data) {
                refresh();

                $(document).Toasts('create', {
                    class: 'bg-success',
                    title: 'Complete',
                    subtitle: '',
                    body: 'Data uploaded. Model updated.',
                    autohide: true,
                    delay: 6000 
                });
            }
        });
    });
});
