    .popover( (d,i)->
            svg2 = d3.select(document.createElement("svg"))
                .attr("height",50)
            g = svg2.append("g")

            g.append("rect")
              .attr("width",d.r*5)
              .attr("height",5)

            g.append("text")
              .text("(#{d.x}, #{d.y})")
              .attr("dy","10")
            {
                title: "#{d.label}"
                content: svg2
                detection: "shape"
                placement: "fixed"
                gravity: "right"
                position: [width,70]
                displacement: [0, 0]
                mousemove: false
            }
        )

# this overrides mouseover
        .tooltip( (d, i) ->
            r = +d3.select(this).attr('r')
            x = +d3.select(this).attr('cx')
            return {
                type: "tooltip",
                text: "x: #{d.x}; radius: #{r}",
                detection: "shape",
                placement: "mouse",
                gravity: "right",
                displacement: [r+2, -20],
                mousemove: true
            }
        )