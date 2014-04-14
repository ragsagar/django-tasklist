// main js file for report template
// function for activate knob
$('.dial').knob();

var json_response = $.getJSON('/tasks/report/task_by_status/json', function(response) {
	// geting the data form backend
	creat_pie_chart(response.task_by_status);
	creat_rectangular_pie_chart(response.task_by_module);
})


function labelFormatter(label, series) {
	// function for format the labels
	return "<div style='font-size:8pt; text-align:center; padding:2px; color:white;'>" + label + "<br/>" + Math.round(series.percent) + "%</div>";
}

function creat_pie_chart(data) {
	// function to ceate tilted pie chart.
	$.plot('.status_chart', data, {
	    series: {
	        pie: {
	            show: true,
	            radius: 1,
	            tilt: 0.5,
	            label: {
	                show: true,
	                radius: 1,
	                formatter: labelFormatter,
	                background: {
	                    opacity: 0.8
	                }
	            },
	            combine: {
	                color: '#999',
	                threshold: 0.1
	            }
	        }
	    },
	    legend: {
	        show: false
	    }
	});
}
function creat_rectangular_pie_chart(data) {
	$.plot('.module_chart', data, {
	    series: {
	        pie: {
	            show: true,
	            radius: 500,
	            label: {
	                show: true,
	                formatter: labelFormatter,
	                threshold: .05
	            }
	        }
	    },
	    legend: {
	        show: true
	    }
	});
}
