import  click
from    argparse        import  Namespace
from    pfmisc          import  Colors as C
from    pfmongo         import  driver, env
from    pfmongo.models  import  responseModel

NC = C.NO_COLOUR
GR = C.LIGHT_GREEN
CY = C.CYAN

def options_add(options:Namespace) -> Namespace:
    options.do          = 'showAllDB'
    return options

def showAll_asInt(options:Namespace) -> int:
    return driver.run_intReturn(options)

def showAll_asModel(options:Namespace) -> responseModel.mongodbResponse:
    return driver.run_modelReturn(options)

@click.command(cls = env.CustomCommand, help=f"""
-- list databases containing data

This command shows all the populated databases available in a given mongodb
server. It accepts no arguments.

""")
@click.pass_context
def showAll(ctx:click.Context) -> int:
    # pudb.set_trace()
    return showAll_asInt(options_add(ctx.obj['options']))
