import os

_css = open(os.path.join(os.path.dirname(__file__),
                         "css",
                         "bootstrap.min.css")).read()

def header(title):
    return """
           <!DOCTYPE html>
           <html lang="en">
           <head>
           <title>{0}</title>
           <style>{1}</style>
           <head>
           <body>
           <h1>{0}</h1>
           """.format(title, _css)

footer = "</body></html>"

class Summary(obj):

    def __init__(self, var):
        html = []
        if var.type == "Key":
            self.html.append("""
                             <div>
                             <h2>{var.name} <small class="text-muted">KEY</small></h2>
                             <table class="table">
                             <tr><th scope="row">Min:</td><td>{var.min}</td></tr>
                             <tr><th scope="row">Max:</td><td>{var.max}</td></tr>
                             <tr><th scope="row">Dense:</td><td>{var.dense}</td></tr>
                             </table>
                             </div>
                             """.format(var=var)

    def __str__(self):
        return "".join(html)

