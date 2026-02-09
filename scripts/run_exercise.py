#!/usr/bin/env python3

import asyncio
import logging
import sys
from pathlib import Path

from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client import ConcentrateClient
from src.experiments import ExperimentRunner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("experiments.log"),
        logging.StreamHandler(),
    ],
)

console = Console()


async def main():
    console.print("[bold green]Concentrate API Multi-Provider LLM Exercise[/bold green]\n")

    try:
        client = ConcentrateClient()
        console.print("[green]✓[/green] Client initialized\n")

        console.print("Testing API connection...")
        if await client.test_connection():
            console.print("[green]✓[/green] API connection successful\n")
        else:
            console.print("[red]✗[/red] API connection failed. Please check your API key.")
            return

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to initialize client: {str(e)}")
        return

    runner = ExperimentRunner(client)

    try:
        await runner.experiment_1_multi_provider_comparison()
        await runner.experiment_2_parameter_exploration()
        await runner.experiment_3_reasoning_comparison()
        await runner.experiment_4_edge_cases()
        await runner.experiment_5_performance_testing()

        results_file = runner.save_results()

        runner.print_summary()

        console.print(f"\n[bold green]All experiments completed![/bold green]")
        console.print(f"Results saved to: {results_file}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Experiments interrupted by user[/yellow]")
        runner.save_results("experiment_results_interrupted.json")
    except Exception as e:
        console.print(f"\n[red]Error during experiments: {str(e)}[/red]")
        logging.exception("Experiment error")
        runner.save_results("experiment_results_error.json")


if __name__ == "__main__":
    asyncio.run(main())
