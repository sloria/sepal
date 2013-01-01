// Generated by CoffeeScript 1.4.0

/*
Visualization
*/


(function() {
  var CHART_HEIGHT, CHART_WIDTH, ID_PROP_NAME, LABEL_PROP_NAME, PT_RADIUS, TOOLTIP_SIZE, X_AXIS_LABEL_OFFSET, X_DIM, X_DIM_INDEX, X_TICKS, Y_AXIS_LABEL_OFFSET, Y_DIM, Y_DIM_INDEX, Y_TICKS, addToSelectedDimensions, color, drawScatterplot, getMinAndMaxRangeForFeatures, height, margin, removeFromSelectedDimensions, selectedDimensions, svg, width, xAxis, xScale, yAxis, yScale;

  window.Viz = {};

  Viz.dataset = {};

  X_DIM = {};

  Y_DIM = {};

  X_DIM_INDEX = false;

  Y_DIM_INDEX = false;

  /* Constants
  */


  LABEL_PROP_NAME = "label";

  ID_PROP_NAME = 'pk';

  CHART_WIDTH = 475;

  CHART_HEIGHT = 450;

  PT_RADIUS = 4;

  X_AXIS_LABEL_OFFSET = 35;

  Y_AXIS_LABEL_OFFSET = -50;

  X_TICKS = 8;

  Y_TICKS = 8;

  TOOLTIP_SIZE = "12px";

  selectedDimensions = [];

  margin = {
    top: 30,
    right: 50,
    bottom: 60,
    left: 70
  };

  width = CHART_WIDTH - margin.left - margin.right;

  height = CHART_HEIGHT - margin.top - margin.bottom;

  svg = d3.select("div#chart").append("svg").attr("width", width + margin.left + margin.right).attr("height", width + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

  xScale = d3.scale.linear().rangeRound([0, width - 50]);

  yScale = d3.scale.linear().rangeRound([height, 0]);

  color = d3.scale.category10();

  xAxis = d3.svg.axis().scale(xScale).orient('bottom').ticks(X_TICKS);

  yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(Y_TICKS);

  svg.append("g").attr("class", "x axis").attr("transform", "translate(0, " + height + " )").call(xAxis).append("text").attr("class", "label").attr('x', width).attr('y', X_AXIS_LABEL_OFFSET).style("text-anchor", "end").text(function() {
    return "Select X";
  });

  svg.append("g").attr("class", "y axis").call(yAxis).append("text").attr('class', 'label').attr("transform", "rotate(-90)").attr('y', Y_AXIS_LABEL_OFFSET).attr('dy', ".71em").style("text-anchor", "end").text(function() {
    return "Select Y";
  });

  jQuery(function() {
    /*
        When the document is ready, send an AJAX request for the data
    */
    d3.json(Dataset.updateVisualizationUrl, function(data) {
      Viz.dataset = data;
      addToSelectedDimensions(Math.round(Math.random() * Object.keys(Viz.dataset.instances[0]).length - 4));
      return addToSelectedDimensions(Math.round(Math.random() * Object.keys(Viz.dataset.instances[0]).length - 4));
    });
    return $('li.feature-select.multicheck').on('click', function() {
      var self, val;
      self = this;
      val = $(self).val();
      if ($(self).hasClass('checked')) {
        return addToSelectedDimensions(val);
      } else {
        return removeFromSelectedDimensions(val);
      }
    });
  });

  drawScatterplot = function() {
    /*
        The main method that draws the scatterPlot and handles updates (enters, transitions,
        exits, etc.). This is called when first loading the plot as well as when there
        are any changes.
    */

    var domainRangeObj, dots, legend, mouseover, tooltip, transition1;
    domainRangeObj = getMinAndMaxRangeForFeatures(Viz.dataset.instances);
    X_DIM = X_DIM_INDEX ? domainRangeObj.features[parseInt(X_DIM_INDEX)] : {
      "minVal": 0,
      "maxVal": Viz.dataset.instances.length - 1,
      "name": "dummy"
    };
    Y_DIM = Y_DIM_INDEX ? domainRangeObj.features[parseInt(Y_DIM_INDEX)] : {
      "minVal": 0,
      "maxVal": Viz.dataset.instances.length - 1,
      "name": "dummy"
    };
    tooltip = d3.select("body").data(Viz.dataset.instances).append("div").style("position", "absolute").style("z-index", "10").style("visibility", "hidden").text(function(d, i) {
      var format, x, xLabel, y, yLabel;
      format = d3.format(".2f");
      x = X_DIM.name !== "dummy" ? format(d[X_DIM.name]) : i;
      xLabel = X_DIM.name !== "dummy" ? X_DIM.name : "None";
      y = Y_DIM.name !== "dummy" ? format(d[Y_DIM.name]) : 0;
      yLabel = Y_DIM.name !== "dummy" ? Y_DIM.name : "None";
      return "" + xLabel + ": " + x + ",\r\n " + yLabel + ": " + y;
    }).attr("class", "d3-tooltip");
    xScale.domain([X_DIM.minVal, X_DIM.maxVal]);
    yScale.domain([Y_DIM.minVal, Y_DIM.maxVal]);
    color.domain(Viz.dataset.labels);
    dots = svg.selectAll(".dot").data(Viz.dataset.instances);
    dots.enter().append("circle").attr('class', 'dot').attr('data-id', function(d) {
      return d['pk'];
    }).attr('r', PT_RADIUS).on("mouseover", function(d, i) {
      return mouseover(d, i);
    }).on("mousemove", function() {
      return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
    }).on("mouseout", function() {
      clearTimeout(myTimeout);
      return tooltip.style("visibility", "hidden");
    }).attr("cx", function(d, i) {
      var scaleInput;
      scaleInput = X_DIM.name !== "dummy" ? d[X_DIM.name] : i;
      d['x'] = scaleInput;
      return xScale(scaleInput);
    }).attr("cy", function(d, i) {
      return height * Math.random();
    }).transition().duration(2000).delay(200).attr("cy", function(d, i) {
      var scaleInput;
      scaleInput = Y_DIM.name !== "dummy" ? d[Y_DIM.name] : 0;
      d['y'] = xScale(scaleInput);
      return yScale(scaleInput);
    }).style("fill", function(d) {
      return color(d.label);
    });
    dots.exit().remove();
    svg.selectAll(".legend").remove();
    legend = svg.selectAll(".legend").data(color.domain()).enter().append('g').attr('class', "legend").attr("transform", function(d, i) {
      return "translate(0, " + (i * 20) + ")";
    });
    legend.append("rect").attr('x', width - 18).attr('width', 10).attr('height', 10).style('fill', color);
    legend.append("text").attr("x", width - 24).attr('y', 5).attr('dy', 5).style('text-anchor', 'end').text(function(d) {
      return d;
    });
    transition1 = svg.transition().duration(1000);
    transition1.select('.x.axis').call(xAxis);
    transition1.select('.y.axis').call(yAxis);
    transition1.select('.x.axis .label').text(function() {
      if (X_DIM_INDEX) {
        return X_DIM.name;
      } else {
        return "Select X";
      }
    });
    transition1.select('.y.axis .label').text(function() {
      if (Y_DIM_INDEX) {
        return Y_DIM.name;
      } else {
        return "Select Y";
      }
    });
    transition1.selectAll('.dot').attr("cx", function(d, i) {
      var scaleInput;
      scaleInput = X_DIM.name !== "dummy" ? d[X_DIM.name] : i;
      d['x'] = scaleInput;
      return xScale(scaleInput);
    }).attr("cy", function(d, i) {
      var scaleInput;
      scaleInput = Y_DIM.name !== "dummy" ? d[Y_DIM.name] : 0;
      d['y'] = scaleInput;
      return yScale(scaleInput);
    }).style("fill", function(d) {
      return color(d.label);
    });
    return mouseover = function(d, i) {
      /*
              On mouseover, show tooltip (coordinates) and scroll to thed
              datapoints corresponding table row using the oScroller API.
      */

      var content, format, inst, instId, instRow;
      inst = d3.select(d)[0][0];
      instId = d['pk'];
      instRow = $("tr[data-id=" + instId + "]");
      window.instRowNumber = parseInt($("tr[data-id=" + instId + "] .index").text());
      format = d3.format(".2f");
      content = "" + inst.label + ": (" + (format(inst.x)) + ", " + (format(inst.y)) + ")";
      if (!isNaN(instRowNumber)) {
        content += " Row " + instRowNumber;
      }
      tooltip.style("visibility", "visible").text(function(d, i) {
        return content;
      }).style("font-size", TOOLTIP_SIZE);
      $('tr.selected').removeClass('selected');
      return setTimeout(function() {
        oTable.fnSettings().oScroller.fnScrollToRow(instRowNumber);
        return instRow.toggleClass("selected");
      }, 750);
    };
  };

  Viz.reloadData = function() {
    /*
        Global method for updating the plot when data is added, changed, or removed.
        Sends an AJAX request for the new data then
    */
    return d3.json(Dataset.updateVisualizationUrl, function(data) {
      Viz.dataset = data;
      return drawScatterplot();
    });
  };

  getMinAndMaxRangeForFeatures = function(instances) {
    /*
        Calculates the min & max values for each feature across all instances
    
        @param - the instances to be visualized
        @return - Object of the form:
           {
             "domainMin": 0
             "domainMax": instances.length
               "features" : [
                 "name": < feature name >,
                 "minVal" : < min value for feature >,
                 "maxVal" : < max value for feature >
               ]
           }
    */

    var floatVal, inst, max, min, prop, propNames, returnObj, value, _i, _j, _len, _len1, _ref;
    returnObj = {
      "domainMin": 0,
      "domainMax": instances.length,
      features: []
    };
    propNames = [];
    _ref = instances[0];
    for (prop in _ref) {
      value = _ref[prop];
      if ((prop !== LABEL_PROP_NAME && prop !== ID_PROP_NAME && prop !== 'x' && prop !== 'y') && instances[0].hasOwnProperty(prop)) {
        propNames.push(prop);
      }
    }
    for (_i = 0, _len = propNames.length; _i < _len; _i++) {
      prop = propNames[_i];
      min = Number.MAX_VALUE;
      max = Number.MIN_VALUE;
      for (_j = 0, _len1 = instances.length; _j < _len1; _j++) {
        inst = instances[_j];
        floatVal = parseFloat(inst[prop]);
        min = floatVal < min ? floatVal : min;
        max = floatVal > max ? floatVal : max;
      }
      returnObj.features.push({
        "name": prop,
        "minVal": min,
        "maxVal": max
      });
    }
    return returnObj;
  };

  addToSelectedDimensions = function(dimension) {
    /*
        A user has selected a dimension checkbox on the data table
        This updates the global able which keeps track of what's
        been checked and passes that to the viz
    */

    var index;
    selectedDimensions.push(dimension);
    if (selectedDimensions.length > 2) {
      index = selectedDimensions.splice(0, 1);
      $("li.feature-select.multicheck[value=" + index[0] + "]").removeClass('checked');
      $("li.feature-select.multicheck[value=" + index[0] + "]").find("span").removeClass("icon-ok");
    }
    X_DIM_INDEX = selectedDimensions[0];
    Y_DIM_INDEX = selectedDimensions[1];
    return drawScatterplot();
  };

  removeFromSelectedDimensions = function(dimension) {
    /*
        A user has de-selected a dimension checkbox on the data table
        This updates the global variable (selectedDimesnsion) which keeps track of what's
        been checked and passes that to the viz
    */

    var removeIndex;
    removeIndex = selectedDimensions.indexOf(dimension);
    selectedDimensions.splice(removeIndex, 1);
    if (selectedDimensions.length < 2) {
      X_DIM_INDEX = null;
      Y_DIM_INDEX = null;
    } else {
      X_DIM_INDEX = selectedDimensions[0];
      Y_DIM_INDEX = selectedDimensions[1];
    }
    return drawScatterplot();
  };

}).call(this);
