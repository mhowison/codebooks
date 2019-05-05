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
           <style>{1} svg {{ margin: 0; padding: 0; }}</style>
           <head>
           <body>
           <div class="container">
           <h1>{0}</h1>
           <p class="lead"><strong>{2:,d}</strong> variables x <strong>{3:,d}</strong> observations</p>
           """.format(title, _css, nvar, nobs)

footer = "</div></body></html>"

class Summary(object):

    def __init__(self, var):

        missing = 100.0 * var.missing.sum() / var.length
        if missing == 0:
            missing = """<span class="label label-success">NONE MISSING</span>"""
        elif missing < 5:
            missing = """<span class="label label-warning">{:.2f}% MISSING</span>""".format(missing)
        else:
            missing = """<span class="label label-danger">{:.2f}% MISSING</span>""".format(missing)
            
        self.html = ["""
                     <hr/>
                     <div>
                     <h4>{}&nbsp;&nbsp;
                     <small><span class="label label-default">{}</span>&nbsp;{}</small>
                     </h4>
                     """.format(var.name, var.type.upper(), missing)]

        if var.desc:
            self.html.append("<p>{}</p>".format(var.desc))

        if var.type == "Unique Key":
            pass
        elif var.type == "Constant":
            self.html.append("<h4>Value: '{}'</h4>".format(var.counts.index[0]))
        elif var.type == "Indicator":
            self.html.append("""
                             <table class="table table-condensed">
                             <tr>
                             <th scope="row">{}</th>
                             <td>{:,d} ({:.1f}%)</td>
                             </tr>
                             <tr>
                             <th scope="row">{}</th>
                             <td>{:,d} ({:.1f}%)</td>
                             </tr>
                             </table>
                             """.format(var.counts.index[0],
                                        var.counts.iloc[0],
                                        100.0 * var.counts.iloc[0] / var.length,
                                        var.counts.index[1],
                                        var.counts.iloc[1],
                                        100.0 * var.counts.iloc[1] / var.length))
        elif var.type == "Categorical":
            if var.distinct <= 15:
                plt.figure(figsize=(14, (var.distinct+1)*0.33))
                sns.barplot(x=var.counts.values, y=var.counts.index, color=color)
                sns.despine()
                svg = StringIO()
                plt.savefig(svg, format="svg", bbox_inches="tight", pad_inches=0)
                plt.close()
                svg.seek(0)
                self.html.append(svg.getvalue())
            elif var.distinct <= 50:
                plt.figure(figsize=(14, 2.5 + 0.05*max(len(x) for x in var.counts.index)))
                sns.barplot(x=var.counts.index, y=var.counts.values, color=color)
                sns.despine()
                plt.xticks(rotation=90)
                svg = StringIO()
                plt.savefig(svg, format="svg", bbox_inches="tight", pad_inches=0)
                plt.close()
                svg.seek(0)
                self.html.append(svg.getvalue())
            else:
                self.html.append("""
                                 <table class="table table-condensed">
                                 <thead>
                                 <th scope="col" colspan="2">Top 5</th>
                                 <th scope="col" colspan="2">Bottom 5</th>
                                 <th scope="col">#Distinct</th>
                                 </thead>
                                 """)
                n = len(var.counts)
                for i in range(5):
                    self.html.append("""
                                     <tr>
                                     <td>{}</td>
                                     <td>{:,d} ({:.1f}%)</td>
                                     <td>{}</td>
                                     <td>{:,d} ({:.1f}%)</td>
                                     <td>{}</td>
                                     </tr>
                                     """.format(var.counts.index[i],
                                                var.counts.iloc[i],
                                                100.0 * var.counts.iloc[i] / var.length,
                                                var.counts.index[n-(5-i)],
                                                var.counts.iloc[n-(5-i)],
                                                100.0 * var.counts.iloc[n-(5-i)] / var.length,
                                                "{:,d}".format(var.distinct) if i==0 else ""))
                self.html.append("</table>")
        elif var.type == "Continuous":
            plt.figure(figsize=(15.5, 2.5))
            sns.distplot(var.values)
            sns.despine()
            plt.xticks(var.range, ["Min", "25th", "50th", "75th", "Max"], rotation=90, fontsize=8)
            plt.yticks([])
            plt.gca().xaxis.tick_top()
            plt.tick_params(length=0, width=0)
            svg = StringIO()
            plt.savefig(svg, format="svg", bbox_inches="tight", pad_inches=0)
            plt.close()
            svg.seek(0)
            self.html.append("""
                             <div class="row">
                             {}
                             </div>
                             <table class="table table-condensed">
                             <thead>
                             <th scope="col">Min</th>
                             <th scope="col">25th</th>
                             <th scope="col">50th</th>
                             <th scope="col">75th</th>
                             <th scope="col">Max</th>
                             <th scope="col">#Distinct</th>
                             </thead>
                             <tr>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:.3g}</td>
                             <td>{:,d}</td>
                             </tr>
                             </table>
                             """.format(svg.getvalue(), *var.range, var.distinct))
            plt.close()
        else:
            raise ValueError("unknown variable type '{}'".format(var.type))

        self.html.append("</div>")

    def __str__(self):
        return "".join(self.html)

