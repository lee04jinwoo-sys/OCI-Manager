
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.status import Status

console = Console()

class UI:
    """Modern TUI for OCI Manager using Rich (Inspired by Anki Manager)"""
    
    ICON_ROCKET = "🚀"
    ICON_SERVER = "🖥️"
    ICON_SUCCESS = "✅"
    ICON_ERROR = "❌"
    ICON_WARN = "⚠️"
    ICON_INFO = "📡"
    ICON_STEP = "🔹"

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header(title="OCI Cloud Manager"):
        console.print(Panel(
            Text(title, justify="center", style="bold white"),
            subtitle="[bold grey50]v1.0.0[/]",
            border_style="bright_blue"
        ))

    @staticmethod
    def render_instance_table(instances):
        table = Table(show_header=True, header_style="bold magenta", border_style="grey37", expand=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Name", style="bold white")
        table.add_column("State", justify="center")
        table.add_column("Public IP", style="cyan")
        table.add_column("Shape", style="green")
        table.add_column("OCPU/RAM", justify="right")
        table.add_column("Created", style="dim")

        for i, inst in enumerate(instances, 1):
            state = inst['state']
            state_style = "green" if state == "RUNNING" else "yellow" if state == "PROVISIONING" else "red"
            
            table.add_row(
                str(i),
                inst['name'],
                Text(state, style=state_style),
                inst['ip'],
                inst['shape'],
                f"{inst['cpus']} / {inst['ram']}GB",
                inst['created']
            )
        console.print(table)

    @staticmethod
    def render_billing(cost, usage):
        from rich.columns import Columns
        cost_panel = Panel(Text(f"{cost}", style="bold yellow", justify="center"), title="[bold white]Monthly Est. Cost[/]", border_style="yellow", expand=False, width=30)
        ocpu_color = "green" if usage['ocpu_pct'] < 80 else "yellow" if usage['ocpu_pct'] < 100 else "red"
        ram_color = "green" if usage['ram_pct'] < 80 else "yellow" if usage['ram_pct'] < 100 else "red"
        usage_text = Text()
        usage_text.append(f"OCPU: {usage['ocpus']}/4.0 ", style="white")
        usage_text.append(f"({usage['ocpu_pct']:.1f}%)\n", style=ocpu_color)
        usage_text.append(f"RAM:  {usage['ram']}/24GB ", style="white")
        usage_text.append(f"({usage['ram_pct']:.1f}%)", style=ram_color)
        usage_panel = Panel(usage_text, title="[bold white]Always Free Usage[/]", border_style="bright_blue", expand=False, width=35)
        console.print(Columns([cost_panel, usage_panel]))

    @staticmethod
    def main_menu():
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Key", style="bold green")
        table.add_column("Description", style="bold white")

                options = [
                    ("1", "Refresh Dashboard"),
                    ("2", "Instance Control"),
                    ("3", "SSH Connect"),
                    ("4", "Run Command (All/Select)"),
                    ("5", "Upload File (All/Select)"),
                    ("6", "Test Telegram Notification"),
                    ("Q", "Exit")
                ]
        for key, desc in options:
            table.add_row(f"[{key}]", desc)
        console.print(Panel(table, title="[bold white]Menu[/]", border_style="bright_blue", expand=False))

    @staticmethod
    def prompt(msg, default=None):
        return Prompt.ask(f"[bold white]{UI.ICON_STEP} {msg}[/]", default=default)

    @staticmethod
    def success(msg): console.print(f"{UI.ICON_SUCCESS} [bold green]{msg}[/]")
    @staticmethod
    def error(msg): console.print(f"{UI.ICON_ERROR} [bold red]{msg}[/]")
    @staticmethod
    def warn(msg): console.print(f"{UI.ICON_WARN} [bold yellow]{msg}[/]")
    @staticmethod
    def info(msg): console.print(f"{UI.ICON_INFO} [cyan]{msg}[/]")
    @staticmethod
    def wait(msg): return console.status(f"[italic grey50]{msg}...[/]")
