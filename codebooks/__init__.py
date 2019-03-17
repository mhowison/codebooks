from htmlmin import minify

import .html
from .variable import Variable

def htmlbook(df, title="Codebook", outfile=None):

    output = [html.header(title)]

    for varname in df.columns:
        var = Variable(df[varname])
        output.append(str(html.Summary(var)))

    output.append(html.footer)

    return minify("".join(output), remove_empty_space=True)

