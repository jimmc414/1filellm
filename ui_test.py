from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt

def main():
    console = Console()

    layout = Layout()

    # Divide the layout: header, sidebar, main, footer
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="main")
    )

    # Add content to the header
    layout["header"].update(Panel("[bold magenta]Dashboard Prototype[/bold magenta]", style="on blue"))

    # Add content to the sidebar
    sidebar_content = Text.from_markup(
        "\n[link=file://./navigate]Navigate[/link]\n"
        "[link=file://./settings]Settings[/link]\n"
        "[link=file://./help]Help[/link]\n", 
        justify="left"
    )
    layout["sidebar"].update(Panel(sidebar_content, title="Menu", border_style="green"))

    # Add content to the main area
    main_content = Text("Welcome to the Dashboard!\n\nHere you could display data, charts, etc.")
    layout["main"].update(Panel(main_content, title="Main Content"))

    # Add footer
    layout["footer"].update(Panel("[bold]Status: Ready[/bold]", style="on red"))

    # Render the layout
    console.print(layout)

    # Interaction: simulate modal popup by asking for input
    action = Prompt.ask("\nEnter an action (navigate, settings, help, or quit)")
    if action.lower() == "quit":
        exit()
    else:
        console.print(Panel(f"Action: {action} selected", style="on yellow"))

if __name__ == "__main__":
    main()
