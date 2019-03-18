import os

_css = open(os.path.join(os.path.dirname(__file__),
                         "css",
                         "bootstrap.min.css")).read()

def _range(var):
    return """
           <table class="table">
           <thead>
           <tr><th scope="col">Min</th><th scope="col">25th Percentile</th><th scope="col">Median</th><th scope="col">75th Percentile</th><th scope="col">Max</th></tr>
           </thead>
           <tr>{}</tr>
           </table>
           """.format("".join("<tr>{}</tr>".format(x) for x in var.range), var=var)

def header(title, nvar, nobs):
    return """
           <!DOCTYPE html>
           <html lang="en">
           <head>
           <title>{0}</title>
           <style>{1}</style>
           <head>
           <body>
           <div class="container">
           <h1>{0}</h1>
           <p class="lead"><strong>{2:,d}</strong> variables x <strong>{3:,d}</strong> observations</p>
           """.format(title, _css, nvar, nobs)

footer = "</div></body></html>"

class Summary(object):

    def __init__(self, var):

        nmissing = var.missing.sum()
        if nmissing == 0:
            missing = """<span class="label label-success">NONE MISSING</span>"""
        else:
            missing = """<span class="label label-warning">{:.2f}% MISSING</span>""".format(100.0 * nmissing / var.length)
            
        self.html = ["""
                     <hr/>
                     <div>
                     <p class="lead">{}
                     <small><span class="label label-default">{}</span>&nbsp;{}</small>
                     </p>
                     """.format(var.name, var.type.upper(), missing)]

        if var.type == "Unique Key":
            pass
        elif var.type == "Constant":
            self.html.append("<h4>Value: '{}'</h4>".format(var.counts.index[0]))
        elif var.type == "Indicator":
            self.html.append("<h4>{:.1f}% {} / {:.1f}% {}</h4>".format(100.0 * var.counts.ix[0] / var.length,
                                                                       var.counts.index[0],
                                                                       100.0 * var.counts.ix[1] / var.length,
                                                                       var.counts.index[1]))
        elif var.type == "Categorical":
            if var.distinct <= 10:
                self.html.append("")
            elif var.distinct <= 100:
        elif var.type == "Continuous":
            self.html.append("")
        else:
            raise ValueError("unknown variable type '{}'".format(var.type))

        self.html.append("</div>")

    def __str__(self):
        return "".join(self.html)

