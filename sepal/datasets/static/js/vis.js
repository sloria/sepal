// Generated by CoffeeScript 1.4.0

/*
Visualization
*/


(function() {
  var CHART_HEIGHT, CHART_WIDTH, ID_PROP_NAME, LABEL_PROP_NAME, PT_RADIUS, TOOLTIP_SIZE, X_AXIS_LABEL_OFFSET, X_DIM, X_DIM_INDEX, X_TICKS, Y_AXIS_LABEL_OFFSET, Y_DIM, Y_DIM_INDEX, Y_TICKS, addToSelectedDimensions, color, drawScatterplot, getMinAndMaxRangeForFeatures, height, margin, prevChartHeight, prevChartWidth, removeFromSelectedDimensions, selectedDimensions, svg, width, xAxis, xScale, yAxis, yScale;

  window.Viz = {};

  Viz.dataset = {};

  X_DIM = {};

  Y_DIM = {};

  X_DIM_INDEX = null;

  Y_DIM_INDEX = null;

  /* Constants
  */


  LABEL_PROP_NAME = "label";

  ID_PROP_NAME = 'pk';

  CHART_WIDTH = 475;

  CHART_HEIGHT = 450;

  PT_RADIUS = 4;

  X_AXIS_LABEL_OFFSET = 35;

  Y_AXIS_LABEL_OFFSET = -60;

  X_TICKS = 5;

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

  svg = d3.select("div#chart").append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

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
      return drawScatterplot();
    });
    return $('li.feature-select').on('click', function() {
      var $this, featureIndex;
      $this = $(this);
      featureIndex = $this.val();
      if ($this.hasClass('checked')) {
        return addToSelectedDimensions(featureIndex);
      } else {
        return removeFromSelectedDimensions(featureIndex);
      }
    });
  });

  prevChartWidth = 0;

  prevChartHeight = 0;

  drawScatterplot = function() {
    /*
        The main method that draws the scatterPlot and handles updates (enters, transitions,
        exits, etc.). This is called when first loading the plot as well as when there
        are any changes.
    */

    var click, domainRangeObj, dots, legend, mouseover, tooltip;
    domainRangeObj = getMinAndMaxRangeForFeatures(Viz.dataset.instances);
    X_DIM = X_DIM_INDEX !== null ? domainRangeObj.features[parseInt(X_DIM_INDEX)] : {
      "minVal": 0,
      "maxVal": Viz.dataset.instances.length - 1,
      "name": "dummy"
    };
    Y_DIM = Y_DIM_INDEX !== null ? domainRangeObj.features[parseInt(Y_DIM_INDEX)] : {
      "minVal": 0,
      "maxVal": Viz.dataset.instances.length - 1,
      "name": "dummy"
    };
    tooltip = d3.select("body").data(Viz.dataset.instances).append("div").style("position", "absolute").style("z-index", "10").style("visibility", "hidden").attr("class", "nvtooltip");
    xScale.domain([X_DIM.minVal, X_DIM.maxVal]);
    yScale.domain([Y_DIM.minVal, Y_DIM.maxVal]);
    color.domain(Viz.dataset.labels);
    dots = svg.selectAll(".dot").data(Viz.dataset.instances, function(d) {
      return d['pk'];
    });
    dots.enter().append("circle").attr('class', 'dot').attr('data-id', function(d) {
      return d['pk'];
    }).attr('r', PT_RADIUS).on("mouseover", function(d, i) {
      return mouseover(d, i);
    }).on("mousemove", function() {
      return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
    }).on("mouseout", function() {
      return tooltip.style("visibility", "hidden");
    }).on("click", function(d, i) {
      return click(d, i);
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
    dots.transition().duration(1000).attr("cx", function(d, i) {
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
    dots.exit().transition().duration(1000).attr("r", 0).remove();
    svg.selectAll(".legend").remove();
    legend = svg.selectAll(".legend").data(color.domain()).enter().append('g').attr('class', "legend").attr("transform", function(d, i) {
      return "translate(0, " + (i * 20) + ")";
    });
    legend.append("rect").attr('x', width - 18).attr('width', 10).attr('height', 10).style('fill', color);
    legend.append("text").attr("x", width - 24).attr('y', 5).attr('dy', 5).style('text-anchor', 'end').text(function(d) {
      return d;
    });
    svg.select('.x.axis').transition().duration(1000).call(xAxis);
    svg.select('.y.axis').transition().duration(1000).call(yAxis);
    svg.select('.x.axis .label').transition().duration(1000).text(function() {
      if (X_DIM_INDEX !== null) {
        return X_DIM.name;
      } else {
        return "Select X";
      }
    });
    svg.select('.y.axis .label').transition().duration(1000).text(function() {
      if (Y_DIM_INDEX !== null) {
        return Y_DIM.name;
      } else {
        return "Select Y";
      }
    });
    mouseover = function(d, i) {
      /*
              On mouseover, show tooltip (coordinates) and scroll to thed
              datapoints corresponding table row using the oScroller API.
      */

      var content, format, inst, instId, instRow, instRowNumber;
      inst = d3.select(d)[0][0];
      instId = d['pk'];
      instRow = $("tr[data-id=" + instId + "]");
      instRowNumber = parseInt($("tr[data-id=" + instId + "] .index").text());
      format = d3.format(".2f");
      content = "<p class=\"coordinates\"><span class=\"value\">" + ("[" + (format(inst.x)) + ", " + (format(inst.y)) + "]") + "</span></p>";
      content += "<p>" + inst.label;
      if (!isNaN(instRowNumber)) {
        content += " (Row " + instRowNumber + ")";
      }
      content += "</p>";
      tooltip.style('visibility', "visible").html(function() {
        return content;
      });
      $('tr.selected').removeClass('selected');
      return setTimeout(function() {
        oTable.fnSettings().oScroller.fnScrollToRow(instRowNumber);
        return instRow.toggleClass("selected");
      }, 750);
    };
    return click = function(d, i) {
      /* On click, select the instance's table row using the oTable API.
      */

      var inst, instId, instRow;
      inst = d3.select(d)[0][0];
      instId = d['pk'];
      instRow = $("tr[data-id=" + instId + "]")[1];
      console.log(instRow);
      return oTT.fnSelect(instRow);
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

    var floatVal, inst, max, min, prop, propNames, returnObj, _i, _j, _len, _len1;
    returnObj = {
      "domainMin": 0,
      "domainMax": instances.length,
      features: []
    };
    propNames = (function() {
      var _results;
      _results = [];
      for (prop in instances[0]) {
        if ((prop !== LABEL_PROP_NAME && prop !== ID_PROP_NAME && prop !== 'x' && prop !== 'y') && prop in instances[0]) {
          _results.push(prop);
        }
      }
      return _results;
    })();
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
        This updates the global varable which keeps track of what's
        been checked and passes that to the viz
    */

    var index;
    selectedDimensions.push(dimension);
    if (selectedDimensions.length > 2) {
      index = selectedDimensions.splice(0, 1);
      $("li.feature-select.multicheck[value=" + index[0] + "]").removeClass('checked').find("span").removeClass("icon-ok");
    }
    X_DIM_INDEX = selectedDimensions[0], Y_DIM_INDEX = selectedDimensions[1];
    return drawScatterplot();
  };

  removeFromSelectedDimensions = function(dimension) {
    /*
        A user has de-selected a dimension checkbox on the data table
        This updates the global variable (selectedDimension) which keeps track of what's
        been checked and passes that to the viz
    */

    var removeIndex;
    removeIndex = selectedDimensions.indexOf(dimension);
    selectedDimensions.splice(removeIndex, 1);
    if (selectedDimensions.length < 2) {
      X_DIM_INDEX = null;
      Y_DIM_INDEX = null;
    } else {
      X_DIM_INDEX = selectedDimensions[0], Y_DIM_INDEX = selectedDimensions[1];
    }
    return drawScatterplot();
  };

}).call(this);
