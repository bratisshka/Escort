$(function () {
    eval($('#code').text());
    // prettyPrint();
});

$(document).ready(function () {
    $.ajax({
        url: '/ocs/statistic_donat',
        type: 'get',
        success: function (data) {
            Morris.Donut({
                element: 'donat',
                data: data,
                backgroundColor: '#eeeeee',
                colors: [
                    '#e57373', //провалено
                    '#fff176', //ожидает подтверждения
                    '#4fc3f7', //выполняется
                    '#81c784' //выполнено
                ],
                formatter: function (x) {
                    return x + "%"
                }
            }).on('click', function (i, row) {
                console.log(i, row);
            });
        }
    })

    $.ajax({
        url: '/ocs/statistic_bar',
        type: 'get',
        success: function (data) {
            Morris.Bar({
                element: 'bar',
                data: data,
                xkey: 'x',
                ykeys: ['y'],
                labels: ['задач'],
                barColors: function (row, series, type) {
                    if (type === 'bar') {
                        var red = Math.ceil(255 * row.y / this.ymax);
                        return 'rgb(' + red + ',0,0)';
                    }
                    else {
                        return '#000';
                    }
                },
                xLabelMargin: 10
            });
        }
    })
});

// Morris.Bar({
//     element: 'bar',
//     data: [
//         {x: '2011 Q1', y: 0},
//         {x: '2011 Q2', y: 1},
//         {x: '2011 Q3', y: 2},
//         {x: '2011 Q4', y: 3},
//         {x: '2012 Q1', y: 4},
//         {x: '2012 Q2', y: 5},
//         {x: '2012 Q3', y: 6},
//         {x: '2012 Q4', y: 7},
//         {x: '2013 Q1', y: 8}
//     ],
//     xkey: 'x',
//     ykeys: ['y'],
//     labels: ['Y'],
//     barColors: function (row, series, type) {
//         if (type === 'bar') {
//             var red = Math.ceil(255 * row.y / this.ymax);
//             return 'rgb(' + red + ',0,0)';
//         }
//         else {
//             return '#000';
//         }
//     }
// });