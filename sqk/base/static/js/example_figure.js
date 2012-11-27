function draw(data) {
	var margin = {"right": 20, "bottom": 25, "top": 10, "height": 100, "width": 400, "left": 60};
	    width = 400 - margin.left - margin.right
	    height = 100 - margin.top - margin.bottom;
	var g = d3.select('#chart').append('svg').attr('width',width + margin.left + margin.right + 25).attr('height',height + margin.top + margin.bottom + 25).append('g').attr('transform','translate(' + margin.left + ',' + margin.top + ')')
	var scales = {
    apple_type_x: d3.scale.ordinal().domain(['a', 'b', 'c', 'd', 'e', 'f']).rangeBands([0, 320],0.1), 
    apple_type_y: d3.scale.ordinal().domain(['a', 'b', 'c', 'd', 'e', 'f']).range([65, 52, 39, 26, 13, 0]), 
    count_x: d3.scale.linear().range([0, 320]).domain([0, 9]), 
    count_y: d3.scale.linear().range([0, 65]).domain([9, 0])
};
	g.selectAll('.bars').data(data).enter().append('rect').attr('class','geom_bar').attr('id','bar_apple_type_count').attr('x',function(d) {
	return scales.apple_type_x(d.apple_type);
}
).attr('y',function(d) {
	return scales.count_y(d.count)
}
).attr('width',scales.apple_type_x.rangeBand()).attr('height',function(d) {
	return height - scales.count_y(d.count)
}
)
	xAxis = d3.svg.axis().scale(scales.apple_type_x)
	g.append("g").attr("class","xaxis").attr("transform","translate(0," + height + ")").call(xAxis)
}

function init() {
	console.debug('Hi');
}

