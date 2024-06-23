"""
codebooks: automatic generation of codebooks from dataframes
"""

# Re-exported imports
from codebooks import html
from codebooks.variable import Variable

# Hidden imports
from htmlmin import minify as _minify
from importlib import resources

__version__ = resources.read_text(__name__, "VERSION").strip()

def htmlbook(df, title="Codebook", outfile=None, desc={}):

    output = [html.header(title, len(df.columns), len(df))]

    for i, varname in enumerate(df.columns):
        var = Variable(df[varname], desc.get(varname, ""))
        var.index = i
        output.append(str(html.Summary(var)))

    output.append(html.footer)

    output = _minify("".join(output), remove_empty_space=True)

    if outfile is not None:
        with open(outfile, "w") as f:
            f.write(output)
    else:
        return output
