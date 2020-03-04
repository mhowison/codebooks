import matplotlib.pyplot as plt
import os
import seaborn as sns
from io import StringIO

sns.set(font="Noto Sans")

color = sns.color_palette("Blues")[-2]

_css = open(os.path.join(os.path.dirname(__file__),
                         "css",
                         "bootstrap.min.css")).read()

def header(title, nvar, nobs):
    return """
           <!DOCTYPE html>
           <html lang="en">
           <head>
           <title>{0}</title>
           <style>{1}</style>
           <head>
           <body>
           <div class="container-fluid">
           <h1>{0}</h1>
           <p class="lead"><strong>{2:,d}</strong> variables x <strong>{3:,d}</strong> observations</p>
           <table class="table table-condensed">
           <thead>
           <th>Index</th><th>Variable</th><th>Type</th><th>%Missing</th><th colspan=8>#Distinct</th>
           </thead>
           """.format(title, _css, nvar, nobs)

footer = "</table></div></body></html>"

def yesno(x):
    if x == 0: return "False"
    elif x == 1: return "True"
    else: return x

class Summary(object):

    def __init__(self, var):

        missing = 100.0 * var.missing.sum() / var.length
        if missing == 0:
            missing = """<span class="label label-success">NONE</span>"""
        elif missing == 100:
            missing = """<span class="label label-danger">ALL</span>"""
        elif missing < 5:
            missing = """<span class="label label-warning">{:.2f}%</span>""".format(missing)
        else:
            missing = """<span class="label label-danger">{:.2f}%</span>""".format(missing)

        if var.desc:
            desc = "<p>{}</p>".format(var.desc)
        else:
            desc = ""

        if var.type == "Categorical":
            span = min(var.distinct+1, 6)
        elif var.type == "Indicator":
            span = 3
        elif var.type == "Numeric":
            span = 2
        else:
            span = 1

        self.html = ["""
                     <tr>
                     <td rowspan={span}>{index}</td>
                     <td rowspan={span}><strong>{name}</strong>{desc}</td>
                     <td rowspan={span}>{type}</td>
                     <td rowspan={span}>{missing}</td>
                     <td rowspan={span}><em>{distinct:,d}</em></td>
                     """.format(span=span, index=var.index, name=var.name, desc=desc, type=var.type, missing=missing, distinct=var.distinct)]

        if var.type == "Unique Key" or var.type == "Empty":
            self.html.append("<td colspan=7></td>")
        elif var.type == "Constant":
            self.html.append("<td colspan=6><strong>{}</strong></td><td><em>100%</em></td>".format(var.counts.index[0]))
        elif var.type == "Indicator":
            self.html.append("""
                             <td colspan=5><strong>Values</strong></td>
                             <td><strong>Count</strong></td>
                             <td><strong>Frequency</strong></td>
                             </tr><tr>
                             <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                             </tr><tr>
                             <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                             """.format(yesno(var.counts.index[0]),
                                        var.counts.values[0],
                                        100.0 * var.counts.values[0] / var.length,
                                        yesno(var.counts.index[1]),
                                        var.counts.values[1],
                                        100.0 * var.counts.values[1] / var.length))
        elif var.type == "Categorical":
            if var.distinct <= 5:
                self.html.append("""<td colspan=5><strong>Values</strong></td>
                                    <td><strong>Count</strong></td>
                                    <td><strong>Frequency</strong></td>
                                    </tr><tr>""")
                for i, x in zip(var.counts.index[:-1], var.counts.values[:-1]):
                    self.html.append("""
                                     <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                                     </tr><tr>
                                     """.format(i, x, 100.0 * x / var.length))
                for i, x in zip(var.counts.index[-1:], var.counts.values[-1:]):
                    self.html.append("""
                                     <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                                     """.format(i, x, 100.0 * x / var.length))
            else:
                self.html.append("""<td colspan=5><strong>Example Values</strong></td>
                                    <td><strong>Count</strong></td>
                                    <td><strong>Frequency</strong></td>
                                    </tr><tr>""")
                for i, x in zip(var.counts.index[:2], var.counts.values[:2]):
                    self.html.append("""
                                     <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                                     </tr><tr>
                                     """.format(i, x, 100.0 * x / var.length))
                self.html.append("<td colspan=7>...</td></tr><tr>")
                for i, x in zip(var.counts.index[-2:-1], var.counts.values[-2:-1]):
                    self.html.append("""
                                     <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                                     </tr><tr>
                                     """.format(i, x, 100.0 * x / var.length))
                for i, x in zip(var.counts.index[-1:], var.counts.values[-1:]):
                    self.html.append("""
                                     <td colspan=5>{}</td><td>{:,d}</td><td><em>{:.1f}%</em></td>
                                     """.format(i, x, 100.0 * x / var.length))
        elif var.type == "Numeric":
            self.html.append("""
                             <td><strong>Min</strong></td>
                             <td><strong>25th</strong></td>
                             <td><strong>50th</strong></td>
                             <td><strong>75th</strong></td>
                             <td><strong>Max</strong></td>
                             <td colspan=2></td>
                             </tr><tr>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td colspan=2></td>
                             """.format(*var.range))
        else:
            raise ValueError("unknown variable type '{}'".format(var.type))

        self.html.append("</tr>")

    def __str__(self):
        return "".join(self.html)

