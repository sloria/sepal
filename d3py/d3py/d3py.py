from css import CSS
import javascript as JS
import numpy as np

import logging

import webbrowser
from HTTPHandler import CustomHTTPRequestHandler, ThreadedHTTPServer
import threading

from cStringIO import StringIO
import time
from datetime import datetime

import json


class D3object(object):
    def build_js():
        raise NotImplementedError

    def build_css():
        raise NotImplementedError

    def build_html():
        raise NotImplementedError

    def build_geoms():
        raise NotImplementedError

    def save_data(self):
        raise NotImplementedError

    def save_css(self):
        raise NotImplementedError

    def save_js(self):
        raise NotImplementedError

    def save_html(self):
        raise NotImplementedError

    def build(self):
        self.build_js()
        self.build_css()
        self.build_html()
        self.build_geoms()

    def update(self):
        self.build()
        self.save()

    def save(self):
        self.save_data()
        self.save_css()
        self.save_js()
        self.save_html()

    def clanup(self):
        raise NotImplementedError

    def show(self):
        self.update()
        self.save()

    def __enter__(self):
        self.interactive = False
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        if ex_tb is not None:
            print "Cleanup after exception: %s: %s"%(ex_type, ex_value)
        self.cleanup()

    def __del__(self):
        self.cleanup()


class Figure(D3object):
    def __init__(self, data, name="figure", width=400, height=100, port=8001, 
            template=None, font="Asap", logging=False, **kwargs):
        """
        data : dataFrame
            data used for the plot. This dataFrame is column centric
        name : string
            name of visualisation. This will appear in the title
            bar of the webpage, and is the name of the folder where
            your files will be stored.
            
        keyword args are converted from foo_bar to foo-bar if you want to pass
        in arbitrary css to the figure    
        
        """
        # store data
        self.name = name
        self.data = data
        self.filemap = {"static/d3.js":{"fd":open("static/d3.js","r"), "timestamp":time.time()},}
        self.save_data()

        # Networking stuff
        self.port = port
        self.server_thread = None
        self.httpd = None
        # interactive is True by default as this is designed to be a command line tool
        # we do not want to block interaction after plotting.
        self.interactive = True
        self.logging = logging

        # initialise strings
        self.js = JS.JavaScript()
        self.margins = {"top": 10, "right": 20, "bottom": 25, "left": 60, "height":height, "width":width}
        
        # we use bostock's scheme http://bl.ocks.org/1624660
        self.css = CSS()
        self.html = ""
        self.template = template or "".join(open('static/d3py_template.html').readlines())
        self.js_geoms = JS.JavaScript()
        self.css_geoms = CSS()
        self.geoms = []
        # misc arguments - these go into the css!
        self.font = font
        self.args = {
            "width": width - self.margins["left"] - self.margins["right"],
            "height": height - self.margins["top"] - self.margins["bottom"],
            "font-family": "'%s'; sans-serif"%self.font
        }
        kwargs = dict([(k[0].replace('_','-'), k[1]) for k in kwargs.items()])
        self.args.update(kwargs)

    def ion(self):
        """
        Turns interactive mode on ala pylab
        """
        self.interactive = True

    def set_data(self, data):
        errmsg = "the %s geom requests %s which is not the given dataFrame!"
        for geom in self.geoms:
            for param in geom.params:
                if param:
                    assert param in data, errmsg%(geom.name, param)
        self.update()

    def add_geom(self, geom):
        errmsg = "the %s geom requests %s which is not in our dataFrame!"
        for p in geom.params:
            if p:
                assert p in self.data, errmsg%(geom.name, p)
        self.geoms.append(geom)
        self.save()
    
    def build_scales(self):
        """
        create appropriate scales for each column of the data frame
        """
        # we take a slightly over the top approach to scales at the moment
        scale = {}
        width = self.args["width"]
        height = self.args["height"]
        for colname in self.data.columns:
            # we test to see if the column contains strings or numbers
            if type(self.data[colname][0]) is str:
                logging.info("using ordinal scale for %s"%colname)
                # if the column contains characters, build an ordinal scale
                height_linspace = np.linspace(height,0,len(self.data[colname]))
                height_linspace = [int(h) for h in height_linspace]
                
                width_linspace = np.linspace(0, width,len(self.data[colname]))
                width_linspace = [int(w) for w in width_linspace]
                
                y_range = JS.Object("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("range",  height_linspace)
                    
                x_range = JS.Object("d3.scale") \
                    .add_attribute("ordinal") \
                    .add_attribute("domain", list(self.data[colname])) \
                    .add_attribute("rangeBands",  [0, width], 0.1)
                                    
            elif type(self.data[colname][0]) == datetime:
                logging.info("using time scale for %s"%colname)
                # min and max time in milliseconds
                max_time = time.mktime(max(self.data[colname]).timetuple())*1000
                min_time = time.mktime(min(self.data[colname]).timetuple())*1000
                
                y_range = JS.Object("d3.time") \
                    .add_attribute("scale") \
                    .add_attribute("range", [0, height]) \
                    .add_attribute("domain", [max_time, min_time])

                x_range = JS.Object("d3.time") \
                    .add_attribute("scale") \
                    .add_attribute("range", [0, width]) \
                    .add_attribute("domain", [min_time, max_time])

            else:
                y_range = JS.Object("d3.scale") \
                    .add_attribute("linear") \
                    .add_attribute("range",  [0, height])
                    
                x_range = JS.Object("d3.scale") \
                    .add_attribute("linear")\
                    .add_attribute("range",  [0, width])
                
                if min(self.data[colname]) < 0:
                    x_range.add_attribute("domain", [min(self.data[colname]), max(self.data[colname])])
                    y_range.add_attribute("domain", [max(self.data[colname]), min(self.data[colname])])
                else:
                    x_range.add_attribute("domain", [0, max(self.data[colname])])
                    y_range.add_attribute("domain", [max(self.data[colname]), 0])
                    
            scale.update({"%s_y"%colname: str(y_range), "%s_x"%colname: str(x_range)})
            
        return scale
        

    def build_js(self):
        draw = JS.Function("draw", ("data",))
        draw += "var margin = %s;"%json.dumps(self.margins).replace('""','')
        draw += "    width = %s - margin.left - margin.right"%self.margins["width"]
        draw += "    height = %s - margin.top - margin.bottom;"%self.margins["height"]
        # this approach to laying out the graph is from Bostock: http://bl.ocks.org/1624660
        draw += "var g = " + JS.Object("d3").select("'#chart'") \
            .append("'svg'") \
            .attr("'width'", 'width + margin.left + margin.right + 25') \
            .attr("'height'", 'height + margin.top + margin.bottom + 25') \
            .append("'g'") \
            .attr("'transform'", "'translate(' + margin.left + ',' + margin.top + ')'")
        
        scale = self.build_scales()
        draw += "var scales = %s;"%json.dumps(scale, sort_keys=True, indent=4).replace('"', '')
        self.js = JS.JavaScript() + draw + JS.Function("init")

    def build_css(self):
        # build up the basic css
        chart = {
        }
        chart.update(self.args)
        self.css["#chart"] = chart

    def build_html(self):
        # we start the html using a template - it's pretty simple
        self.html = self.template
        self.html = self.html.replace("{{ name }}", self.name)
        self.html = self.html.replace("{{ font }}", self.font)
        self.save_html()

    def build_geoms(self):
        self.js_geoms = JS.JavaScript()
        self.css_geoms = CSS()
        for geom in self.geoms:
            self.js_geoms.merge(geom.build_js())
            self.css_geoms += geom.build_css()

    def __add__(self, geom):
        self.add_geom(geom)

    def __iadd__(self, geom):
        self.add_geom(geom)
        return self

    def data_to_json(self):
        """
        converts the data frame stored in the figure to JSON
        """
        def cast(a):
            try:
                return float(a)
            except ValueError:
                return a
            except TypeError:
                if type(a) == datetime:
                    return time.mktime(a.timetuple()) * 1000

                return a

        d = [
            dict([
                (colname, cast(row[i]))
                for i,colname in enumerate(self.data.columns)
            ])
            for row in self.data.values
        ]
        try:
            s = json.dumps(d, sort_keys=True, indent=4)
        except OverflowError, e:
            print "Error: Overflow on variable (type %s): %s: %s"%(type(d), d, e)
            raise
        return s

    def save_data(self,directory=None):
        """
        save a json representation of the figure's data frame
        
        Parameters
        ==========
        directory : str
            specify a directory to store the data in (optional)
        """
        # write data
        filename = "%s.json"%self.name
        self.filemap[filename] = {"fd":StringIO(self.data_to_json()),
                "timestamp":time.time()}

    def save_css(self):
        # write css
        filename = "%s.css"%self.name
        css = "%s\n%s"%(self.css, self.css_geoms)
        self.filemap[filename] = {"fd":StringIO(css),
                "timestamp":time.time()}

    def save_js(self):
        # write javascript
        final_js = JS.JavaScript()
        final_js.merge(self.js)
        final_js.merge(self.js_geoms)

        filename = "%s.js"%self.name
        js = "%s"%final_js
        self.filemap[filename] = {"fd":StringIO(js),
                "timestamp":time.time()}

    def save_html(self):
        # update the html with the correct port number
        self.html = self.html.replace("{{ port }}", str(self.port))
        # write html
        filename = "%s.html"%self.name
        self.filemap[filename] = {"fd":StringIO(self.html),
                "timestamp":time.time()}

    def show(self, interactive=None):
        super(Figure, self).show()

        if interactive is not None:
            blocking = not interactive
        else:
            blocking = not self.interactive

        if blocking:
            self.serve(blocking=True)
        else:
            # if not blocking, we serve the 
            self.serve(blocking=False)
            # fire up a browser
            webbrowser.open_new_tab("http://localhost:%s/%s.html"%(self.port, self.name))

    def serve(self, blocking=True):
        """
        start up a server to serve the files for this vis.

        """
        if self.server_thread is None or self.server_thread.active_count() == 0:
            Handler = CustomHTTPRequestHandler
            Handler.filemap = self.filemap
            Handler.logging = self.logging
            try:
                self.httpd = ThreadedHTTPServer(("", self.port), Handler)
            except Exception, e:
                print "Exception %s"%e
                return False
            if blocking:
                self.server_thread = None
                self.httpd.serve_forever()
            else:
                self.server_thread = threading.Thread(
                    target=self.httpd.serve_forever
                )
                self.server_thread.daemon = True
                self.server_thread.start()
            print "You can find your chart at http://localhost:%s/%s/%s.html"%(self.port, self.name, self.name)

    def cleanup(self):
        try:
            if self.httpd is not None:
                print "Shutting down httpd"
                self.httpd.shutdown()
                self.httpd.server_close()
        except Exception, e:
            print "Error in clean-up: %s"%e
