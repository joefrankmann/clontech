function plot_result_graph(teststrip_number) {
  "use strict";
  var chart_element = $(`#teststrip_${teststrip_number}_chart`);
  var teststrip_data = chart_element.data('graph');
  var profile_data = teststrip_data.profile.map((currentValue, index) => [index, currentValue]);
  var baseline_data = teststrip_data.baseline.map((currentValue, index) => [index, currentValue]);

  var graph_data = [
    {
      data: profile_data,
      lines: {show: true},
      points: {show: false},
      color: 'green',
      label: "Profile",
    }, {
      data: baseline_data,
      lines: {show: true},
      points: {show: false},
      color: 'red',
      label: "Baseline",
    }
  ];

  console.log(teststrip_data.c_peak_position)
  console.log(teststrip_data.t_peak_position)
  var markings = [
    {
      color: 'blue',
      lineWidth: 2,
      xaxis: {
        from: teststrip_data.c_peak_position,
        to: teststrip_data.c_peak_position,
      },
    },
    {
      color: 'blue',
      lineWidth: 2,
      xaxis: {
        from: teststrip_data.t_peak_position,
        to: teststrip_data.t_peak_position,
      },
    },
  ];

  var graph_options = {
    grid: {
      hoverable: true,
      clickable: true,
      mouseActiveRadius: 30,
      borderWidth: 0.5,
      markings: markings,
    },
    yaxis: {min: 0, max: 255},
  };

  var do_plot = () => $.plot(chart_element, graph_data, graph_options);
  var chart = do_plot();

  var profile_min = Math.min.apply(null, teststrip_data.profile);

  function peak_label(peak_type) {
    let offset = chart.pointOffset({x: teststrip_data[`${peak_type}_peak_position`], y: profile_min + 5});
    let peak_label = $('<div>',
      {style: `position:absolute;left:${offset.left+4}px;top:${offset.top-24}px;color:#666;font-size:smaller`})
      .text(`${peak_type.toUpperCase()} peak position`);
    return peak_label;
  }

  chart_element.append(peak_label('c'));
  chart_element.append(peak_label('t'));

  var x_axis_label = $('<div>', {class: 'axisLabel xaxisLabel'}).text("Profile");
  var y_axis_label = $('<div>', {class: 'axisLabel yaxisLabel'}).text("Intensity");
  chart_element.append(x_axis_label);
  chart_element.append(y_axis_label);

  chart_element.on('plothover', on_chart_plothover);

  $(window).resize(do_plot);
}

// global because this is state for all charts
var chart_tooltip = {
  tooltip: null, // the actual element cached to avoid lookups
};

function on_chart_plothover(event, pos, item) {
  "use strict";
  if (!item) {
    if (chart_tooltip.tooltip !== null) {
      chart_tooltip.tooltip.remove();
      chart_tooltip.tooltip = null;
    }
    return;
  }

  var profile = item.series.data[item.dataIndex][0];
  var intensity = item.series.data[item.dataIndex][1];

  var pageX = item.pageX;
  if (item.pageX > ($(document).width() - 180)) pageX -= 200;

  var tooltip_div = (label, value) => {
    return $('<div>', {class: 'tooltip-label'}).text(`${label}: `).
      append($('<span>', {class: 'tooltip-value'}).text(value))
  };

  var new_tooltip = (chart_tooltip.tooltip === null);
  if (new_tooltip) {
    chart_tooltip.tooltip = $('<div>', {id: 'tooltip'});
  }
  chart_tooltip.tooltip.
    empty().
    css({top: item.pageY + 5, left: pageX + 20}).append([
      tooltip_div("Intensity", intensity),
      tooltip_div("Profile", profile)]);
  if (new_tooltip) {
    chart_tooltip.tooltip.
      appendTo('body').
      fadeIn(200);
  }
}

$(document).ready(() => {
  plot_result_graph(1);
  $('a[data-toggle="tab"]').on('shown.bs.tab', (e) => {
    var target_number = Number($(e.target).attr("href").substr(-1));
    plot_result_graph(target_number);
  });
});
