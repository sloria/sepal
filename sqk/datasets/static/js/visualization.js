//////////////Visualization//////////////////////////
// Create a namespace for visualization
var Viz = {};
// The scatter plot requires 2 dimensions to be selected
// before points can be plotted.
// Selected dimensions are stored in the
// these two global vars:
var X_DIM, Y_DIM;
// When these are set, they have this form:
// {"minVal": < minimum value for this feature across all instances>, "maxVal": <same idea>, "name": <name of the feature>}
// When the user hasn't selected enough dimensions, the vars are reset to:
// {"minVal" : 0, "maxVal" : < number of instances >, "name": "dummy"}
// The index of the dimensions a user selects are stored in these
// Where the first dimension selection is the x-axis
// These are used to index into list of attribute names to set up X_DIM & Y_DIM
var X_DIM_INDEX, Y_DIM_INDEX;

// Global constants
var LABEL_PROP_NAME = "label";
var CHART_WIDTH = 475;
var CHART_HEIGHT = 450;
var PT_RADIUS = 4;
var X_TICKS = 8;
var Y_TICKS = 8;
var PADDING = CHART_WIDTH / 6;
var selectedDimensions = [];
Viz.data = {};
var svg;

// Calculates the min & max values for each feature across all instances
// @param - the instances to be visualized
// @return - Object of the form:
//    {
//      "domainMin": 0
//      "domainMax": instances.length
//        "features" : [
//          "name": < feature name >,
//          "minVal" : < min value for feature >,
//          "maxVal" : < max value for feature >
//        ]
//    }

function getMinAndMaxRangeForFeatures(instances) {
  var returnObj = {
    "domainMin": 0,
    "domainMax": instances.length,
    features: []
  };
  // First get property names
  var propNames = [];
  for(var key in instances[0]) {
    if(key !== LABEL_PROP_NAME && instances[0].hasOwnProperty(key)) {
      propNames.push(key);
    }
  }
  // Now go through each instance and find the max and min values for each feature
  for(var j = 0; j < propNames.length; j++) {
    var prop = propNames[j];
    var min = Number.MAX_VALUE;
    var max = Number.MIN_VALUE;
    for(var i = 0; i < instances.length; i++) {
      var inst = instances[i];
      var floatVal = parseFloat(inst[prop]);
      min = (floatVal < min) ? floatVal : min;
      max = (floatVal > max) ? floatVal : max;
    }
    // the min and max values for this feature have been found
    returnObj.features.push({
      "name": prop,
      "minVal": min,
      "maxVal": max
    });
  }
  return returnObj;
}

// Draws a new scatter plot based on supplied list of data
// @param data - Object of the form:
//   {
//     "instances" : [
//       {
//         "feature_0" : "val_0",
//         ...
//         "feature_N" : "val_N",
//         "label" : "label_val"
//       }
//     ],
//     "labels" : [
//       "label_0",
//       ...
//       "label_N"
//     ]
//   }
// @return - Nothing.
Viz.scatterPlot = function() {
  // This gets the min & max values for each feature across all instances
  var domainRangeObj = getMinAndMaxRangeForFeatures(Viz.data.instances);

  X_DIM = (X_DIM_INDEX) ? domainRangeObj.features[parseInt(X_DIM_INDEX)] : {
    "minVal": 0,
    "maxVal": Viz.data.instances.length - 1,
    "name": "dummy"
  };
  Y_DIM = (Y_DIM_INDEX) ? domainRangeObj.features[parseInt(Y_DIM_INDEX)] : {
    "minVal": 0,
    "maxVal": Viz.data.instances.length - 1,
    "name": "dummy"
  };

  // set up scales
  var xScale = d3.scale.linear().domain([X_DIM.minVal, X_DIM.maxVal]).range([PADDING, CHART_WIDTH - PADDING]);
  var yScale = d3.scale.linear().domain([Y_DIM.minVal, Y_DIM.maxVal]).range([CHART_HEIGHT - PADDING, PADDING]);
  var categoryScale = d3.scale.ordinal().domain(Viz.data.labels).range(d3.scale.category10().range());

  // set up axes
  var xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(X_TICKS);

  var yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(Y_TICKS);

  // set up legend
  var legendXScale = d3.scale.linear().domain([0, Viz.data.labels.length - 1]).range([PADDING, (CHART_WIDTH / 1.3) - PADDING]);

  svg.selectAll("rect.legend-rect").data(Viz.data.labels).enter().append("rect").attr("class", "legend-rect").attr("x", function(d, i) {
    return legendXScale(i);
  }).attr("y", function(d, i) {
    return PADDING / 3;
  }).attr("width", 10).attr("height", 10).style("fill", function(d, i) {
    return categoryScale(Viz.data.labels[i]);
  });

  svg.selectAll("text.legend").data(Viz.data.labels).enter().append("text").attr("class", "legend").attr("x", function(d, i) {
    return legendXScale(i) + 15;
  }).attr("y", function(d, i) {
    return(PADDING / 3) + 10;
  }).text(function(d, i) {
    return Viz.data.labels[i];
  }).style("font-family", "Helvetica Neue, Helvetica, Arial, sans-serif").style("font-size", "11px");

  // Set up x-axis tick marks
  svg.selectAll("g.axis").remove();
  svg.append("g").attr("class", "x axis").attr("id", "x-axis").attr("transform", "translate(0," + (CHART_HEIGHT - PADDING) + ")").transition().duration(250).call(xAxis);

  // Set up y-axis tick marks
  svg.append("g").attr("class", "y axis").attr("id", "y-axis").attr("transform", "translate(" + PADDING + ", 0)").transition().duration(250).call(yAxis);

  // Label the x-axis
  svg.select("text.x-label").remove();
  svg.append("text").attr("class", "x-label").attr("text-anchor", "end").attr("x", CHART_WIDTH - PADDING).attr("y", CHART_HEIGHT - (PADDING - 35)).style("fill", "#000000").text(function() {
    if(X_DIM_INDEX) {
      return X_DIM.name;
    } else {
      return "Select X";
    }
  });

  // Label the y-axis
  svg.select("text.y-label").remove();
  svg.append("text").attr("class", "y-label").attr("text-anchor", "end").attr("y", (PADDING - 60)).attr("dx", (PADDING * -1.1)).attr("dy", ".75em").attr("transform", "rotate(-90)").style("fill", "#000000").text(function() {
    if(Y_DIM_INDEX) {
      return Y_DIM.name;
    } else {
      return "Select Y";
    }
  });

  // Call the main update method
  updatePlotPoints(svg, Viz.data, xScale, yScale, xAxis, yAxis, categoryScale);
  updateLegend(svg, Viz.data, legendXScale, categoryScale);
}

// Main method which controls the points on the plot as selections
// are made on the data table

function updatePlotPoints(svg, data, xScale, yScale, xAxis, yAxis, categoryScale) {
  var plotPoints = svg.selectAll("circle").data(data.instances);
  // Update the plot points
  plotPoints.transition().duration(1000).delay(200).attr("cx", function(d, i) {
    var scaleInput = (X_DIM.name !== "dummy") ? d[X_DIM.name] : i;
    return xScale(scaleInput);
  }).transition().duration(1000).delay(200).attr("cy", function(d, i) {
    var scaleInput = (Y_DIM.name !== "dummy") ? d[Y_DIM.name] : 0;
    return yScale(scaleInput);
  }).attr("r", PT_RADIUS).style("fill", function(d) {
    return categoryScale(d.label);
  });

  // Handle new data points
  plotPoints.enter().append("circle").attr("cx", function(d, i) {
    var scaleInput = (X_DIM.name !== "dummy") ? d[X_DIM.name] : i;
    return xScale(scaleInput);
  }).attr("cy", function(d, i) {
    return CHART_HEIGHT * Math.random();
  }).transition().duration(2000).delay(200).attr("cy", function(d, i) {
    var scaleInput = (Y_DIM.name !== "dummy") ? d[Y_DIM.name] : 0;
    return yScale(scaleInput);
  }).attr("r", PT_RADIUS).style("fill", function(d) {
    return categoryScale(d.label);
  });

  // If there's less data now, remove those plots points
  plotPoints.exit().remove();

  // Update X axis
  svg.select('#x-axis').transition().duration(1000).delay(200).call(xAxis);

  svg.select('#y-axis').transition().duration(1000).delay(200).call(yAxis);
}



function updateLegend(svg, data, legendXScale, categoryScale) {
  // Update legend
  var legendText = svg.selectAll("text.legend").data(data.labels);
  legendText.transition().duration(500).delay(0).attr("x", function(d, i) {
    return legendXScale(i) + 15;
  }).attr("y", function(d, i) {
    return(PADDING / 3) + 10;
  }).text(function(d, i) {
    return data.labels[i];
  });
  legendText.exit().remove();

  var legendRectangles = svg.selectAll("rect.legend-rect").data(data.labels);
  legendRectangles.transition().duration(500).delay(0).attr("x", function(d, i) {
    return legendXScale(i);
  }).attr("y", function(d, i) {
    return PADDING / 3;
  });
  legendRectangles.exit().remove();
}


// A user has selected a dimension checkbox on the data table
// This updates the global variable which keeps track of what's
// been checked and passes that to the viz

function addToSelectedDimensions(dimension) {
  selectedDimensions.push(dimension);
  if(selectedDimensions.length > 2) {
    // TODO: send asynchronous request for PCA-ified data
    // Right now, it's going to slice out the first element
    var index = selectedDimensions.splice(0, 1);
    $('li.feature-select.multicheck[value=' + index[0] + ']').removeClass('checked');
    $('li.feature-select.multicheck[value=' + index[0] + ']').find("span").removeClass("icon-ok");
  }
  X_DIM_INDEX = selectedDimensions[0];
  Y_DIM_INDEX = selectedDimensions[1];
  Viz.scatterPlot();
}

// A user has de-selected a dimension checkbox on the data table
// This updates the global variable which keeps track of what's
// been checked and passes that to the viz

function removeFromSelectedDimensions(dimension) {
  var removeIndex = selectedDimensions.indexOf(dimension);
  selectedDimensions.splice(removeIndex, 1);
  if(selectedDimensions.length < 2) {
    // There's no longer 2 dimensions selected, 
    // reset the x & y dimensino pointers to be null
    X_DIM_INDEX = null;
    Y_DIM_INDEX = null;
  } else {
    // TODO: this code is replicated, re-think this
    X_DIM_INDEX = selectedDimensions[0];
    Y_DIM_INDEX = selectedDimensions[1];
  }
  Viz.scatterPlot();
}

Viz.reloadData = function() {
  $.ajax({
    url: Dataset.updateVisualizationUrl,
    type: "POST",
    data: {
      "pk": Dataset.id
    },
    dataType: 'json',
    success: function(data) {
      Viz.data = data;
      Viz.scatterPlot();
      return true;
    },
    crossDomain: false,
    cache: false
  });
};

$(document).ready(function() {
  $.ajax({
    url: Dataset.updateVisualizationUrl,
    type: "GET",
    data: {
      "pk": Dataset.id
    },
    dataType: 'json',
    success: function(data) {
      // If AJAX request is successful
      // Load the data
      Viz.data = data;
      // create the svg element
      svg = d3.select("div#chart").append("svg").attr("width", CHART_WIDTH).attr("height", CHART_HEIGHT);
      // Draw the points and axes even though no dimensions
      // have been selected yet
      Viz.scatterPlot();
    },
    crossDomain: false,
    cache: false
  });

  // Update selected dimensions when a feature is selected
  $('li.feature-select.multicheck').on('click', function() {
    var self = this;
    var val = $(self).val(); // The index value of the selected dimension
    if($(self).hasClass('checked')) {
      addToSelectedDimensions(val);
    } else {
      removeFromSelectedDimensions(val);
    }
  });
});