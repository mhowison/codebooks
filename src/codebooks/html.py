"""
Generator for HTML-formatted codebooks
"""

from codebooks.variable import Variable
from htmlmin import minify
from importlib import resources
from pandas import DataFrame
from typing import Dict


_css = (
    resources
    .files("codebooks.css")
    .joinpath("bootstrap.min.css")
    .read_text()
)


_header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>{title}</title>
    <style>{css}</style>
    <head>
    <body>
    <div class="container-fluid">
    <h1>{title}</h1>
    <p class="lead">
    <strong>{nvar:,d}</strong> variables x
    <strong>{nobs:,d}</strong> observations
    </p>
    <table class="table table-condensed">
    <thead>
    <th>Index</th>
    <th>Variable</th>
    <th>Type</th>
    <th>%Missing</th>
    <th colspan=6>#Distinct</th>
    </thead>
"""


_footer = "</table></div></body></html>"


def _yesno(x):
    """
    Helper function to convert 0/1 to False/True strings.
    """
    if x == 0:
        return "False"
    elif x == 1:
        return "True"
    else:
        return x


class SummaryRow(object):
    """
    Construct an HTML table row that summarizes a Variable object.
    """

    def __init__(self, var: Variable, ncategories: int = 10):
        self.var = var
        self.ncategories = ncategories
        self.set_missing()
        self.set_desc()
        self.set_span()
        self.set_html()

    def set_missing(self):
        """
        Calculate the percent missing column.
        """
        missing = 100.0 * self.var.missing.sum() / self.var.length
        if missing == 0:
            self.missing = """
                <span class="label label-success">NONE</span>
            """
        elif missing == 100:
            self.missing = """
                <span class="label label-danger">ALL</span>
            """
        elif missing < 5:
            self.missing = """
                <span class="label label-warning">{:.2f}%</span>
            """.format(missing)
        else:
            self.missing = """
                <span class="label label-danger">{:.2f}%</span>
            """.format(missing)

    def set_desc(self):
        """
        Set the variable description, if available.
        """
        if self.var.desc:
            self.desc = "<p>{}</p>".format(self.var.desc)
        else:
            self.desc = ""

    def set_span(self):
        """
        Calculate the number of columns and row span from the
        variable type.
        """
        if self.var.type == "Categorical":
            self.span = min(self.var.distinct, self.ncategories) + 1
        elif self.var.type == "Indicator":
            self.span = 3
        elif self.var.type == "Numeric" or self.var.type == "Date":
            self.span = 2
        else:
            self.span = 1

    def set_html(self):
        """
        Generate the HTML table row.
        """
        self.html = ["""
            <tr>
            <td rowspan={span}>{index}</td>
            <td rowspan={span}><strong>{name}</strong>{desc}</td>
            <td rowspan={span}>{type}</td>
            <td rowspan={span}>{missing}</td>
            <td rowspan={span}><em>{distinct:,d}</em></td>
         """.format(
            span=self.span,
            index=self.var.index,
            name=self.var.name,
            desc=self.desc,
            type=self.var.type,
            missing=self.missing,
            distinct=self.var.distinct
        )]

        if self.var.type == "Unique Key" or self.var.type == "Empty":
            self.html.append("<td colspan=5></td>")
        elif self.var.type == "Constant":
            self.html.append("""
                <td colspan=4><strong>{}</strong></td>
                <td><em>100%</em></td>
            """.format(self.var.counts.index[0]))
        elif self.var.type == "Indicator":
            self.html.append("""
                <td colspan=3><strong>Values</strong></td>
                <td><strong>Count</strong></td>
                <td><strong>Frequency</strong></td>
                </tr>
                <tr>
                <td colspan=3>{}</td>
                <td>{:,d}</td>
                <td><em>{:.1f}%</em></td>
                </tr>
                <tr>
                <td colspan=3>{}</td>
                <td>{:,d}</td>
                <td><em>{:.1f}%</em></td>
            """.format(
                _yesno(self.var.counts.index[0]),
                self.var.counts.values[0],
                100.0 * self.var.counts.values[0] / self.var.length,
                _yesno(self.var.counts.index[1]),
                self.var.counts.values[1],
                100.0 * self.var.counts.values[1] / self.var.length)
            )
        elif self.var.type == "Categorical":
            if self.var.distinct <= self.ncategories:
                self.html.append("""
                    <td colspan=3><strong>Values</strong></td>
                    <td><strong>Count</strong></td>
                    <td><strong>Frequency</strong></td>
                    </tr>
                    <tr>
                """)
                for i, x in zip(self.var.counts.index[:-1], self.var.counts.values[:-1]):
                    self.html.append("""
                        <td colspan=3>{}</td>
                        <td>{:,d}</td>
                        <td><em>{:.1f}%</em></td>
                        </tr>
                        <tr>
                    """.format(i, x, 100.0 * x / self.var.length))
                for i, x in zip(self.var.counts.index[-1:], self.var.counts.values[-1:]):
                    self.html.append("""
                        <td colspan=3>{}</td>
                        <td>{:,d}</td>
                        <td><em>{:.1f}%</em></td>
                    """.format(i, x, 100.0 * x / self.var.length))
            else:
                self.html.append("""
                    <td colspan=3><strong>Most Frequent Values</strong></td>
                    <td><strong>Count</strong></td>
                    <td><strong>Frequency</strong></td>
                    </tr>
                    <tr>
                """)
                for i, x in zip(self.var.counts.index[:self.ncategories], self.var.counts.values[:self.ncategories]):
                    self.html.append("""
                        <td colspan=3>{}</td>
                        <td>{:,d}</td>
                        <td><em>{:.1f}%</em></td>
                        </tr>
                        <tr>
                    """.format(i, x, 100.0 * x / self.var.length))
        elif self.var.type == "Numeric":
            self.html.append("""
                <td><strong>Min</strong></td>
                <td><strong>25th</strong></td>
                <td><strong>50th</strong></td>
                <td><strong>75th</strong></td>
                <td><strong>Max</strong></td>
                </tr>
                <tr>
                <td>{:.3f}</td>
                <td>{:.3f}</td>
                <td>{:.3f}</td>
                <td>{:.3f}</td>
                <td>{:.3f}</td>
            """.format(*self.var.range))
        elif self.var.type == "Date":
            self.html.append("""
                <td><strong>Min</strong></td>
                <td><strong>25th</strong></td>
                <td><strong>50th</strong></td>
                <td><strong>75th</strong></td>
                <td><strong>Max</strong></td>
                </tr>
                <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            """.format(*self.var.range))
        else:
            raise ValueError("unknown variable type '{}'".format(self.var.type))

        self.html.append("</tr>")

    def __str__(self):
        return "".join(self.html)


def generate(
    df: DataFrame,
    title: str = "Codebook",
    outfile: str = None,
    desc: Dict[str, str] = {}
):
    """
    Generate an HTML codebook and return as a string
    or write to `outfile` if specified.
    """
    output = [_header.format(
        title=title,
        css=_css,
        nvar=len(df.columns),
        nobs=len(df)
    )]

    for i, varname in enumerate(df.columns):
        var = Variable(
            df[varname],
            desc.get(varname, "")
        )
        var.index = i
        output.append(str(SummaryRow(var)))

    output.append(_footer)

    output = minify("".join(output), remove_empty_space=True)

    if outfile is not None:
        with open(outfile, "w") as f:
            f.write(output)
    else:
        return output
