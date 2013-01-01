###
Visualization
###

# Create a namespace for visualization
window.Viz = {}
Viz.dataset = {}
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

### Constants ###
LABEL_PROP_NAME = "label" # The name of the instance object property that is the label key
ID_PROP_NAME = 'pk'  # The name of the instance object property that is the ID key
CHART_WIDTH = 475  
CHART_HEIGHT = 450
PT_RADIUS = 4  # The radius of each data point
X_AXIS_LABEL_OFFSET = 35 # More postive moves X-axis label lower
Y_AXIS_LABEL_OFFSET = -50  # More negative moves Y-axis label to the left
X_TICKS = 8  # Number of ticks on the x axis
Y_TICKS = 8  # Number of ticks on the y axis
TOOLTIP_SIZE = "12px" # The font size of tooltips

selectedDimensions = []

# D3 margin conventions
margin = {top: 30, right: 50, bottom: 60, left: 70}
width = CHART_WIDTH - margin.left - margin.right
height = CHART_HEIGHT - margin.top - margin.bottom
svg = d3.select("div#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", width + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(#{margin.left}, #{margin.top})")

xScale = d3.scale.linear()
            .rangeRound([0, width - 50])
yScale = d3.scale.linear()
            .rangeRound([height, 0])

color = d3.scale.category10()


xAxis = d3.svg.axis()
            .scale(xScale)
            .orient('bottom')
            .ticks(X_TICKS)

yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left")
            .ticks(Y_TICKS)



# Set up x-axis 
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0, #{ height } )")
    .call(xAxis)
    .append("text") # X axis label
        .attr("class", "label")
        .attr('x', width)
        .attr('y', X_AXIS_LABEL_OFFSET)
        .style("text-anchor", "end")
        .text( () -> return "Select X" )


# Set up y-axis 
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text") # Y axis label
        .attr('class', 'label')
        .attr("transform", "rotate(-90)")
        .attr('y', Y_AXIS_LABEL_OFFSET)
        .attr('dy', ".71em")
        .style("text-anchor", "end")
        .text( () -> return "Select Y" )

jQuery ->
    ###
    When the document is ready, send an AJAX request for the data
    ### 

    d3.json(Dataset.updateVisualizationUrl, (data) ->
        Viz.dataset = data
        drawScatterplot()
    )

    # Add click handler for selecting features
    $('li.feature-select.multicheck').on('click', () ->
        self = this
        val = $(self).val() # The index value of the selected dimension
        if $(self).hasClass('checked') 
            addToSelectedDimensions(val)
        else
            removeFromSelectedDimensions(val)
    )



drawScatterplot = () ->
    ###
    The main method that draws the scatterPlot and handles updates (enters, transitions,
    exits, etc.). This is called when first loading the plot as well as when there
    are any changes.
    ###

    # This gets the min & max values for each feature across all instances
    domainRangeObj = getMinAndMaxRangeForFeatures(Viz.dataset.instances)

    X_DIM = if X_DIM_INDEX then domainRangeObj.features[parseInt(X_DIM_INDEX)] else {
        "minVal": 0,
        "maxVal": Viz.dataset.instances.length - 1,
        "name": "dummy"
    }

    Y_DIM = if Y_DIM_INDEX then domainRangeObj.features[parseInt(Y_DIM_INDEX)] else {
        "minVal": 0,
        "maxVal": Viz.dataset.instances.length - 1,
        "name": "dummy"
    }

    tooltip = d3.select("body").data(Viz.dataset.instances)
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text( (d, i) ->
            format = d3.format(".2f")
            x = if X_DIM.name isnt "dummy" then format(d[X_DIM.name]) else i
            xLabel = if X_DIM.name isnt "dummy" then X_DIM.name else "None"
            y = if Y_DIM.name isnt "dummy" then format(d[Y_DIM.name]) else 0
            yLabel = if Y_DIM.name isnt "dummy" then Y_DIM.name else "None"
            return "#{xLabel}: #{x},\r\n #{yLabel}: #{y}"
        )
        .attr("class", "d3-tooltip")

    # Update domains
    xScale.domain([X_DIM.minVal, X_DIM.maxVal])

    yScale.domain([Y_DIM.minVal, Y_DIM.maxVal])
    color.domain(Viz.dataset.labels)

    dots = svg.selectAll(".dot")
        .data(Viz.dataset.instances)
    # Handle new points
    dots.enter().append("circle")
        .attr('class', 'dot')
        .attr('data-id', (d) -> return d['pk'] )
        .attr('r', PT_RADIUS)
        .on("mouseover", (d,i) -> mouseover(d,i))
        .on("mousemove", () -> 
            return tooltip.style("top", (event.pageY-10)+"px")
                    .style("left",(event.pageX+10)+"px")
        )
        .on("mouseout", () -> 
            return tooltip.style("visibility", "hidden") 
        )
        .attr("cx", (d, i) ->
            scaleInput = if X_DIM.name isnt "dummy" then d[X_DIM.name] else i
            d['x'] = scaleInput
            return xScale(scaleInput)
        )
        .attr("cy", (d, i) -> return height * Math.random() )
        .transition().duration(2000).delay(200)
        .attr("cy", (d, i) ->
            scaleInput = if Y_DIM.name isnt "dummy" then d[Y_DIM.name] else 0
            d['y'] = xScale(scaleInput)
            return yScale(scaleInput)
        )
        .style("fill", (d) -> return color(d.label) )

    # Remove points if instances are deleted
    dots.exit()
        .remove()

    # Redraw legend
    svg.selectAll(".legend").remove();
    legend = svg.selectAll(".legend")
        .data(color.domain())
        .enter().append('g')
        .attr('class', "legend")
        .attr("transform", (d, i) -> return "translate(0, #{i * 20})" )

    legend.append("rect")
        .attr('x', width - 18)
        .attr('width', 10)
        .attr('height', 10)
        .style('fill', color)

    legend.append("text")
        .attr("x", width - 24)
        .attr('y', 5)
        .attr('dy', 5)
        .style('text-anchor', 'end')
        .text( (d) -> return d )
        

    # Transition 1: Update axes
    transition1 = svg.transition().duration(1000)
    transition1.select('.x.axis')
        .call(xAxis)
    transition1.select('.y.axis')
        .call(yAxis)
    # Update axes labels
    transition1.select('.x.axis .label')
        .text( () -> return if X_DIM_INDEX then X_DIM.name else "Select X" )
    transition1.select('.y.axis .label')
        .text( () -> return if Y_DIM_INDEX then Y_DIM.name else "Select Y" )

    # Update dot positions
    transition1.selectAll('.dot')
        .attr("cx", (d, i) -> 
            scaleInput = if X_DIM.name isnt "dummy" then d[X_DIM.name] else i
            d['x'] = scaleInput
            return xScale(scaleInput)
        )
        .attr("cy", (d, i) ->
            scaleInput = if Y_DIM.name isnt "dummy" then d[Y_DIM.name] else 0
            d['y'] = scaleInput
            return yScale(scaleInput)
        )
        .style("fill", (d) -> return color(d.label) )

    mouseover = (d,i) ->
        ###
        On mouseover, show tooltip (coordinates) and scroll to thed
        datapoints corresponding table row using the oScroller API.
        ###
        # The selected instance object
        inst = d3.select(d)[0][0]
        instId = d['pk']
        instRow = $("tr[data-id=#{instId}]")
        # The table row number of the corresponding instance
        # FIXME: table row of newly added intances will not be defined
        window.instRowNumber = parseInt($("tr[data-id=#{instId}] .index").text() ) 
        
        format = d3.format(".2f")
        # The tooltip text
        content = "#{inst.label}: (#{format(inst.x)}, #{format(inst.y)})"
        # Only include the row number if it is defined
        content += " Row #{instRowNumber}" if not isNaN(instRowNumber)
        tooltip.style("visibility", "visible")
                .text( (d, i) ->
                    return content
                )
                .style("font-size", TOOLTIP_SIZE)
                
        $('tr.selected').removeClass('selected');
        # Scroll to the table row of the moused-over datapoint
        setTimeout(() ->
            oTable.fnSettings().oScroller.fnScrollToRow(instRowNumber)
            instRow.toggleClass("selected")
        , 750)



Viz.reloadData = () ->
    ###
    Global method for updating the plot when data is added, changed, or removed.
    Sends an AJAX request for the new data then
    ###
    d3.json(Dataset.updateVisualizationUrl, (data) -> 
        Viz.dataset = data
        drawScatterplot()
    )

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
        if prop not in [LABEL_PROP_NAME, ID_PROP_NAME, 'x', 'y'] and instances[0].hasOwnProperty(prop)
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
    drawScatterplot()

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
    drawScatterplot()



