from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from rich import box
from rich.markdown import Markdown
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from rich import print
from rich.panel import Panel
from rich.console import Group
from rich.panel import Panel
from rich.console import NewLine

table = Table(show_lines=True, box=box.HORIZONTALS, style="grey46", show_header=False)
table.add_column(style="white bold")
table.add_column(style="black")
table.add_column(style="magenta bold")
table.add_column(style="cyan bold")

md = Markdown("Star Wars Ep. V111: *The Last* Jedi")

p1 = Panel(md\
                                    , style="on #FFFF88", expand=False, border_style="#FFFF88")

p2 = Panel("[bold red]alert![/bold red] **Something** happenedddddddddddddddddddddddddd\njhfjkhdjkfbdfkfgbdg\nkhbfkhbkdjgbdg"\
                                    , style="on #FFFF88", expand=False, border_style="#FFFF88")


p3 = Panel("[bold red]alert![/bold red] **Something** happeneddddddddddddddddddddddddddmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm\nmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmjhfjkhdjkfbdfkfgbdgkhbfkhbkdjgbdg"\
                                    , style="on #FFFF88", expand=False, border_style="#FFFF88")

p4 = Panel("[bold red]alert![/bold red] **Something** happeneddddddddddddddddddddddddddjhfjkhdjkfbdfkfgbdgmmmmmmmmmmmmmmmmmmmmmmmmmmmmkhbfkhbkdjgbdg"\
                                    , style="on #FFFF88", expand=False, border_style="#FFFF88")

table.add_row("Dec 20, 2019", Group(p1, NewLine(), p2, fit=True), "$952,110,690")
table.add_row("May 25, 2018", Group(p3, NewLine(), p4, fit=True), "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")


console = Console()
console.print(table)


from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.console import NewLine

panel_group = Group(
    Panel("Hello", style="on blue", expand=False, border_style="blue"),
    Panel("World", style="on red", expand=False),
    fit=True
)
print(Panel(panel_group))