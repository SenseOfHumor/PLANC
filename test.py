from rich.console import Console
import time

console = Console()
with console.status("[bold green]Thinking...", spinner="toggle2"):
    time.sleep(3)
console.print("[bold green]Done![/]")
