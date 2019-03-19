# Re-exported imports
from codebooks import html
from codebooks.variable import Variable

# Hidden imports
from htmlmin import minify as _minify
from pkg_resources import get_distribution as _get_distribution

__version__ = _get_distribution("codebooks").version

def htmlbook(df, title="Codebook", outfile=None, desc={}):

    output = [html.header(title, len(df.columns), len(df))]

    for varname in df.columns:
        var = Variable(df[varname], desc.get(varname, ""))
        output.append(str(html.Summary(var)))

    output.append(html.footer)

    output = _minify("".join(output), remove_empty_space=True)

    if outfile is not None:
        with open(outfile, "w") as f:
            f.write(output)
    else:
        return output

