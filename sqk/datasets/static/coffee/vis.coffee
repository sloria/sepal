###
Visualization
###

# Create a namespace for visualization
window.Viz = {}
# The scatter plot requires 2 dimensions to be selected
# before points can be plotted.
# Selected dimensions are stored in the
# these two global :
X_DIM = {}
Y_DIM = {}
# When these are set, they have this form:
# {"minVal": < minimum value for this feature across all instances>, "maxVal": <same idea>, "name": <name of the feature>}
# When the user hasn't selected enough dimensions, the  are reset to:
# {"minVal" : 0, "maxVal" : < number of instances >, "name": "dummy"}
# The index of the dimensions a user selects are stored in these
# Where the first dimension selection is the x-axis
# These are used to index into list of attribute names to set up X_DIM & Y_DIM
X_DIM_INDEX = false
Y_DIM_INDEX = false

# Global constants
LABEL_PROP_NAME = "label"
CHART_WIDTH = 475
CHART_HEIGHT = 450
PT_RADIUS = 4
X_TICKS = 8
Y_TICKS = 8
PADDING = CHART_WIDTH / 6
selectedDimensions = []
window.Viz.data = {}
svg = null


getMinAndMaxRangeForFeatures = (instances) ->
    ###
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
    ###
    returnObj = 
        "domainMin": 0,
        "domainMax": instances.length,
        features: []

    # First get property names
    propNames = []
    for prop, value of instances[0]
        if prop isnt LABEL_PROP_NAME and instances[0].hasOwnProperty(prop)
            propNames.push(prop)

    # Now go through each instance and find the max and min values for each feature
    for prop in propNames
        min = Number.MAX_VALUE
        max = Number.MIN_VALUE
        for inst in instances
            floatVal = parseFloat(inst[prop])
            min = if (floatVal < min) then floatVal else min
            max = if (floatVal > max) then floatVal else max
        # the min and max values for this feature have been found
        returnObj.features.push({
            "name": prop,
            "minVal": min,
            "maxVal": max
        })
    return returnObj

Viz.scatterPlot = () -> 
    ###
    Draws a new scatter plot based on supplied list of data
    @param data - Object of the form:
      {
        "instances" : [
          {
            "feature_0" : "val_0",
            ...
            "feature_N" : "val_N",
            "label" : "label_val"
          }
        ],
        "labels" : [
          "label_0",
          ...
          "label_N"
        ]
      }
    @return - Nothing.
    ###
  
    # This gets the min & max values for each feature across all instances
    domainRangeObj = getMinAndMaxRangeForFeatures(window.Viz.data.instances)

    X_DIM = if X_DIM_INDEX then domainRangeObj.features[parseInt(X_DIM_INDEX)] else {
        "minVal": 0,
        "maxVal": window.Viz.data.instances.length - 1,
        "name": "dummy"
    }
    console.log "X_DIM_INDEX:"
    console.log X_DIM_INDEX
    console.log "X_DIM:"
    console.log X_DIM


    Y_DIM = if Y_DIM_INDEX then domainRangeObj.features[parseInt(Y_DIM_INDEX)] else {
        "minVal": 0,
        "maxVal": window.Viz.data.instances.length - 1,
        "name": "dummy"
    }
    console.log "Y_DIM_INDEX:"
    console.log Y_DIM_INDEX
    console.log "Y_DIM:"
    console.log Y_DIM

    # set up scales
    xScale = d3.scale.linear()
                    .domain([X_DIM.minVal, X_DIM.maxVal])
                    .range([PADDING, CHART_WIDTH - PADDING])

    yScale = d3.scale.linear()
                    .domain([Y_DIM.minVal, Y_DIM.maxVal])
                    .range([CHART_HEIGHT - PADDING, PADDING])

    categoryScale = d3.scale.ordinal()
                    .domain(window.Viz.data.labels)
                    .range(d3.scale.category10().range())

    # set up axes
    xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(X_TICKS)

    yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(Y_TICKS)

    # Set up legend
    legendXScale = d3.scale.linear().domain([0, window.Viz.data.labels.length - 1]).range([PADDING, (CHART_WIDTH / 1.3) - PADDING])

    svg.selectAll("rect.legend-rect")
        .data(Viz.data.labels).enter()
        .append("rect")
        .attr("class", "legend-rect")
        .attr("x", (d, i) -> return legendXScale(i) )
        .attr("y", (d, i) -> return PADDING / 3)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", (d, i) -> return categoryScale(window.Viz.data.labels[i]) )

    svg.selectAll("text.legend")
        .data(Viz.data.labels)
        .enter()
        .append("text")
        .attr("class", "legend")
        .attr("x", (d, i) -> return legendXScale(i) + 15)
        .attr("y", (d, i) -> return(PADDING / 3) + 10)
        .text((d, i) -> return Viz.data.labels[i])
        .style("font-family", "Helvetica Neue, Helvetica, Arial, sans-serif")
        .style("font-size", "11px")

    # Set up x-axis tick marks
    svg.selectAll("g.axis")
        .remove()
    svg.append("g")
        .attr("class", "x axis")
        .attr("id", "x-axis")
        .attr("transform", "translate(0, #{ CHART_HEIGHT - PADDING } )")
        .transition().duration(250)
        .call(xAxis)

    # Set up y-axis tick marks
    svg.append("g")
        .attr("class", "y axis")
        .attr("id", "y-axis")
        .attr("transform", "translate( #{ PADDING }, 0)")
        .transition().duration(250)
        .call(yAxis)

    # Label the x-axis
    svg.select("text.x-label")
        .remove()
    svg.append("text")
        .attr("class", "x-label")
        .attr("text-anchor", "end")
        .attr("x", CHART_WIDTH - PADDING)
        .attr("y", CHART_HEIGHT - (PADDING - 35))
        .style("fill", "#000000")
        .text( () -> return if X_DIM_INDEX then X_DIM.name else "Select X" )

    # Label the y-axis
    svg.select("text.y-label")
        .remove()
    svg.append("text")
        .attr("class", "y-label")
        .attr("text-anchor", "end")
        .attr("y", (PADDING - 60))
        .attr("dx", (PADDING * -1.1))
        .attr("dy", ".75em")
        .attr("transform", "rotate(-90)")
        .style("fill", "#000000")
        .text( () -> return if Y_DIM_INDEX then Y_DIM.name else "Select Y" )

    # Call the main update method
    updatePlotPoints(svg, window.Viz.data, xScale, yScale, xAxis, yAxis, categoryScale)
    updateLegend(svg, window.Viz.data, legendXScale, categoryScale)

updatePlotPoints = (svg, data, xScale, yScale, xAxis, yAxis, categoryScale) ->
    ###
    Main method which controls the points on the plot as selections
    are made on the data table
    ###
    plotPoints = svg.selectAll("circle")
                    .data(data.instances)


    t0 = svg.transition().duration(1000).delay(250)
    t0.selectAll('circle')
        .attr("cx", (d, i) -> 
            console.log "X_DIM.name: #{d[X_DIM.name]}"
            scaleInput = if X_DIM.name isnt "dummy" then d[X_DIM.name] else i
            return xScale(scaleInput)
        )
        .attr("cy", (d, i) ->
            scaleInput = if Y_DIM.name isnt "dummy" then d[Y_DIM.name] else 0
            return yScale(scaleInput)
        )
        .attr("r", PT_RADIUS)
        .style("fill", (d) -> return categoryScale(d.label) )


    # Handle new data points
    plotPoints
        .enter()
        .append("circle")
        .attr("cx", (d, i) ->
            scaleInput = if X_DIM.name isnt "dummy" then d[X_DIM.name] else i
            return xScale(scaleInput)
        )
        .attr("cy", (d, i) -> return CHART_HEIGHT * Math.random() )
        .transition().duration(2000).delay(200)
        .attr("cy", (d, i) ->
            scaleInput = if Y_DIM.name isnt "dummy" then d[Y_DIM.name] else 0
            return yScale(scaleInput)
        )
        .attr("r", PT_RADIUS)
        .style("fill", (d) -> return categoryScale(d.label) )

    # If there's less data now, remove those plots points
    plotPoints.exit().remove()

    # Update axes
    svg.select('#x-axis')
        .transition().duration(1000).delay(200)
        .call(xAxis)

    svg.select('#y-axis')
        .transition().duration(1000).delay(200)
        .call(yAxis)

updateLegend = (svg, data, legendXScale, categoryScale) ->
    ###
    Updates the legend.
    ###
    legendText = svg.selectAll("text.legend").data(data.labels)
        
    legendText.transition().duration(500).delay(0)
        .attr("x", (d, i) -> return legendXScale(i) + 15 )
        .attr("y", (d, i) -> return (PADDING / 3) + 10 )
        .text( (d, i) -> return data.labels[i] )
        
    legendText.exit()
        .remove()

    legendRectangles = svg.selectAll("rect.legend-rect").data(data.labels)
        
    legendRectangles.transition().duration(500).delay(0)
        .attr("x", (d, i) -> return legendXScale(i) )
        .attr("y", (d, i) -> return PADDING / 3 )
        
    legendRectangles.exit()
        .remove()

addToSelectedDimensions = (dimension) ->
    ###
    A user has selected a dimension checkbox on the data table
    This updates the global able which keeps track of what's
    been checked and passes that to the viz
    ###
    selectedDimensions.push(dimension)
    if selectedDimensions.length > 2
        # TODO: send asynchronous request for PCA-ified data
        # Right now, it's going to slice out the first element
        index = selectedDimensions.splice(0, 1)
        # Uncheck the select button
        $("li.feature-select.multicheck[value=#{ index[0] }]").removeClass('checked')
        $("li.feature-select.multicheck[value=#{ index[0] }]").find("span").removeClass("icon-ok")
    X_DIM_INDEX = selectedDimensions[0]
    Y_DIM_INDEX = selectedDimensions[1]
    Viz.scatterPlot()

removeFromSelectedDimensions = (dimension) ->
    ###
    A user has de-selected a dimension checkbox on the data table
    This updates the global variable (selectedDimesnsion) which keeps track of what's
    been checked and passes that to the viz
    ###
    removeIndex = selectedDimensions.indexOf(dimension)
    selectedDimensions.splice(removeIndex, 1)
    if(selectedDimensions.length < 2) 
        # There's no longer 2 dimensions selected, 
        # reset the x & y dimensino pointers to be null
        X_DIM_INDEX = null
        Y_DIM_INDEX = null
    else
        # TODO: this code is replicated, re-think this
        X_DIM_INDEX = selectedDimensions[0]
        Y_DIM_INDEX = selectedDimensions[1]
    Viz.scatterPlot()


Viz.reloadData = () ->
    $.ajax({
    url: Dataset.updateVisualizationUrl,
    type: "POST",
    data: {"pk": Dataset.id},
    dataType: 'json',
    success: (data) ->
        Viz.data = data
        Viz.scatterPlot()
        return true
    ,
    crossDomain: false,
    cache: false
    })

jQuery ->
    $.ajax({
    url: Dataset.updateVisualizationUrl,
    type: "GET",
    data: {"pk": Dataset.id},
    dataType: 'json',
    success: (data) ->
        # If AJAX request is successful
        # Load the data
        window.Viz.data = data
        # create the svg element
        svg = d3.select("div#chart")
                .append("svg")
                .attr("width", CHART_WIDTH)
                .attr("height", CHART_HEIGHT)
        # Draw the points and axes even though no dimensions
        # have been selected yet
        Viz.scatterPlot()
    ,
    crossDomain: false,
    cache: false
    })

    # Update selected dimensions when a feature is selected
    $('li.feature-select.multicheck').on('click', () ->
        self = this
        val = $(self).val() # The index value of the selected dimension
        if $(self).hasClass('checked') 
            addToSelectedDimensions(val)
        else
            removeFromSelectedDimensions(val)
    )

