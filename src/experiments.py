import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table

from src.client import ConcentrateClient, APIRequestError
from src.prompts import PromptLibrary

logger = logging.getLogger(__name__)
console = Console()


class ExperimentRunner:

    def __init__(self, client: ConcentrateClient, output_dir: Path = Path("outputs")):
        self.client = client
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict[str, Any]] = []

    async def experiment_1_multi_provider_comparison(self) -> Dict[str, Any]:
        console.print("\n[bold blue]Experiment 1: Multi-Provider Comparison[/bold blue]")
        console.print("Testing identical prompts across OpenAI and Anthropic models\n")

        from src.config import ANTHROPIC_MODELS, OPENAI_MODELS

        test_models = {
            "openai": OPENAI_MODELS[:2] if len(OPENAI_MODELS) >= 2 else OPENAI_MODELS,
            "anthropic": ANTHROPIC_MODELS[:2] if len(ANTHROPIC_MODELS) >= 2 else ANTHROPIC_MODELS,
        }

        prompts = PromptLibrary.get_simple_qa_prompts()
        experiment_results = []

        for prompt_data in prompts:
            prompt_name = prompt_data["name"]
            prompt_content = prompt_data["content"]

            console.print(f"[cyan]Testing prompt: {prompt_name}[/cyan]")

            for provider, models in test_models.items():
                for model in models:
                    try:
                        result = await self.client.chat_completion(
                            model=model,
                            messages=[{"role": "user", "content": prompt_content}],
                            temperature=0.7,
                            max_tokens=256,
                        )

                        response_text = result["choices"][0]["message"]["content"]
                        metrics = result.get("metrics", {})

                        experiment_results.append(
                            {
                                "experiment": "multi_provider_comparison",
                                "prompt_name": prompt_name,
                                "provider": provider,
                                "model": model,
                                "prompt": prompt_content,
                                "response": response_text,
                                "metrics": metrics,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                        console.print(
                            f"  ✓ {model}: {metrics.get('latency_ms', 0)}ms, "
                            f"{metrics.get('total_tokens', 0)} tokens"
                        )

                        await asyncio.sleep(0.5)

                    except APIRequestError as e:
                        console.print(f"  ✗ {model}: Error - {str(e)}")
                        experiment_results.append(
                            {
                                "experiment": "multi_provider_comparison",
                                "prompt_name": prompt_name,
                                "provider": provider,
                                "model": model,
                                "error": str(e),
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

        self.results.extend(experiment_results)
        return {"experiment": "multi_provider_comparison", "results": experiment_results}

    async def experiment_2_parameter_exploration(self) -> Dict[str, Any]:
        console.print("\n[bold blue]Experiment 2: Parameter Exploration[/bold blue]")
        console.print("Testing parameter variations (temperature, max_tokens, top_p)\n")

        from src.config import OPENAI_MODELS

        base_prompt = "Write a creative short story about a robot learning to paint."
        test_model = OPENAI_MODELS[0] if OPENAI_MODELS else "openai/gpt-4o-mini"

        temperatures = [0.0, 0.5, 1.0, 1.5]
        experiment_results = []

        console.print("[cyan]Testing temperature variations[/cyan]")
        for temp in temperatures:
            try:
                result = await self.client.chat_completion(
                    model=test_model,
                    messages=[{"role": "user", "content": base_prompt}],
                    temperature=temp,
                    max_tokens=200,
                )

                response_text = result["choices"][0]["message"]["content"]
                metrics = result.get("metrics", {})

                experiment_results.append(
                    {
                        "experiment": "parameter_exploration",
                        "parameter": "temperature",
                        "value": temp,
                        "model": test_model,
                        "prompt": base_prompt,
                        "response": response_text,
                        "metrics": metrics,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                console.print(f"  ✓ Temperature {temp}: {len(response_text)} chars")
                await asyncio.sleep(0.5)

            except APIRequestError as e:
                console.print(f"  ✗ Temperature {temp}: Error - {str(e)}")

        max_tokens_values = [50, 150, 300]
        console.print("\n[cyan]Testing max_tokens variations[/cyan]")
        for max_tokens in max_tokens_values:
            try:
                result = await self.client.chat_completion(
                    model=test_model,
                    messages=[{"role": "user", "content": "Explain machine learning in detail."}],
                    temperature=0.7,
                    max_tokens=max_tokens,
                )

                response_text = result["choices"][0]["message"]["content"]
                metrics = result.get("metrics", {})

                experiment_results.append(
                    {
                        "experiment": "parameter_exploration",
                        "parameter": "max_tokens",
                        "value": max_tokens,
                        "model": test_model,
                        "response": response_text,
                        "metrics": metrics,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                console.print(f"  ✓ Max tokens {max_tokens}: {len(response_text)} chars")
                await asyncio.sleep(0.5)

            except APIRequestError as e:
                console.print(f"  ✗ Max tokens {max_tokens}: Error - {str(e)}")

        self.results.extend(experiment_results)
        return {"experiment": "parameter_exploration", "results": experiment_results}

    async def experiment_3_reasoning_comparison(self) -> Dict[str, Any]:
        console.print("\n[bold blue]Experiment 3: Reasoning Comparison[/bold blue]")
        console.print("Testing reasoning capabilities across models\n")

        from src.config import ANTHROPIC_MODELS, OPENAI_MODELS

        reasoning_prompts = PromptLibrary.get_reasoning_prompts()
        test_models = (OPENAI_MODELS[:2] if len(OPENAI_MODELS) >= 2 else OPENAI_MODELS) + (
            ANTHROPIC_MODELS[:2] if len(ANTHROPIC_MODELS) >= 2 else ANTHROPIC_MODELS
        )

        experiment_results = []

        for prompt_data in reasoning_prompts:
            prompt_name = prompt_data["name"]
            prompt_content = prompt_data["content"]

            console.print(f"[cyan]Testing: {prompt_name}[/cyan]")

            for model in test_models:
                try:
                    result = await self.client.chat_completion(
                        model=model,
                        messages=[{"role": "user", "content": prompt_content}],
                        temperature=0.3,
                        max_tokens=512,
                    )

                    response_text = result["choices"][0]["message"]["content"]
                    metrics = result.get("metrics", {})

                    experiment_results.append(
                        {
                            "experiment": "reasoning_comparison",
                            "prompt_name": prompt_name,
                            "model": model,
                            "prompt": prompt_content,
                            "response": response_text,
                            "metrics": metrics,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    console.print(f"  ✓ {model}: {metrics.get('latency_ms', 0)}ms")
                    await asyncio.sleep(0.5)

                except APIRequestError as e:
                    console.print(f"  ✗ {model}: Error - {str(e)}")
                    experiment_results.append(
                        {
                            "experiment": "reasoning_comparison",
                            "prompt_name": prompt_name,
                            "model": model,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

        self.results.extend(experiment_results)
        return {"experiment": "reasoning_comparison", "results": experiment_results}

    async def experiment_4_edge_cases(self) -> Dict[str, Any]:
        console.print("\n[bold blue]Experiment 4: Edge Cases & Error Handling[/bold blue]")
        console.print("Testing edge cases and API robustness\n")

        from src.config import OPENAI_MODELS

        edge_case_prompts = PromptLibrary.get_edge_case_prompts()
        test_model = OPENAI_MODELS[0] if OPENAI_MODELS else "openai/gpt-4o-mini"

        experiment_results = []

        for prompt_data in edge_case_prompts:
            prompt_name = prompt_data["name"]
            prompt_content = prompt_data["content"]

            console.print(f"[cyan]Testing edge case: {prompt_name}[/cyan]")

            try:
                result = await self.client.chat_completion(
                    model=test_model,
                    messages=[{"role": "user", "content": prompt_content}],
                    temperature=0.7,
                    max_tokens=256,
                )

                response_text = result["choices"][0]["message"]["content"]
                metrics = result.get("metrics", {})

                experiment_results.append(
                    {
                        "experiment": "edge_cases",
                        "case_name": prompt_name,
                        "model": test_model,
                        "input": prompt_content[:100] + "..." if len(prompt_content) > 100 else prompt_content,
                        "response": response_text,
                        "metrics": metrics,
                        "handled": True,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                console.print(f"  ✓ Handled successfully: {len(response_text)} chars")
                await asyncio.sleep(0.5)

            except APIRequestError as e:
                experiment_results.append(
                    {
                        "experiment": "edge_cases",
                        "case_name": prompt_name,
                        "model": test_model,
                        "error": str(e),
                        "handled": False,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                console.print(f"  ✗ Error: {str(e)}")

        console.print("\n[cyan]Testing invalid model name[/cyan]")
        try:
            await self.client.chat_completion(
                model="invalid/model-name",
                messages=[{"role": "user", "content": "Test"}],
            )
            console.print("  ✗ Should have failed but didn't")
        except APIRequestError as e:
            experiment_results.append(
                {
                    "experiment": "edge_cases",
                    "case_name": "invalid_model",
                    "error": str(e),
                    "handled": True,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            console.print(f"  ✓ Correctly rejected invalid model: {str(e)[:50]}")

        self.results.extend(experiment_results)
        return {"experiment": "edge_cases", "results": experiment_results}

    async def experiment_5_performance_testing(self) -> Dict[str, Any]:
        console.print("\n[bold blue]Experiment 5: Performance Testing[/bold blue]")
        console.print("Testing API performance with sequential and concurrent requests\n")

        from src.config import OPENAI_MODELS

        test_model = OPENAI_MODELS[0] if OPENAI_MODELS else "openai/gpt-4o-mini"
        test_prompt = "Count from 1 to 10."
        num_requests = 5

        experiment_results = []

        console.print(f"[cyan]Sequential requests ({num_requests})[/cyan]")
        sequential_times = []

        for i in range(num_requests):
            try:
                start = asyncio.get_event_loop().time()
                result = await self.client.chat_completion(
                    model=test_model,
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=50,
                )
                elapsed = (asyncio.get_event_loop().time() - start) * 1000
                sequential_times.append(elapsed)

                metrics = result.get("metrics", {})
                console.print(f"  Request {i+1}: {metrics.get('latency_ms', 0)}ms")
                await asyncio.sleep(0.3)

            except APIRequestError as e:
                console.print(f"  Request {i+1}: Error - {str(e)}")

        if sequential_times:
            avg_seq = sum(sequential_times) / len(sequential_times)
            experiment_results.append(
                {
                    "experiment": "performance_testing",
                    "test_type": "sequential",
                    "num_requests": num_requests,
                    "avg_latency_ms": avg_seq,
                    "latencies": sequential_times,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            console.print(f"  Average latency: {avg_seq:.2f}ms\n")

        console.print(f"[cyan]Concurrent requests ({num_requests})[/cyan]")

        async def make_request(index: int) -> Optional[Dict[str, Any]]:
            try:
                result = await self.client.chat_completion(
                    model=test_model,
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=50,
                )
                return {"index": index, "metrics": result.get("metrics", {})}
            except APIRequestError as e:
                console.print(f"  Request {index+1}: Error - {str(e)}")
                return None

        concurrent_start = asyncio.get_event_loop().time()
        concurrent_results = await asyncio.gather(*[make_request(i) for i in range(num_requests)])
        concurrent_elapsed = (asyncio.get_event_loop().time() - concurrent_start) * 1000

        concurrent_times = [
            r["metrics"].get("latency_ms", 0) for r in concurrent_results if r is not None
        ]

        if concurrent_times:
            avg_concurrent = sum(concurrent_times) / len(concurrent_times)
            experiment_results.append(
                {
                    "experiment": "performance_testing",
                    "test_type": "concurrent",
                    "num_requests": num_requests,
                    "total_time_ms": concurrent_elapsed,
                    "avg_latency_ms": avg_concurrent,
                    "latencies": concurrent_times,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            console.print(f"  Total time: {concurrent_elapsed:.2f}ms")
            console.print(f"  Average latency: {avg_concurrent:.2f}ms")

        self.results.extend(experiment_results)
        return {"experiment": "performance_testing", "results": experiment_results}

    def save_results(self, filename: Optional[str] = None) -> Path:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"experiment_results_{timestamp}.json"

        filepath = self.output_dir / filename

        output_data = {
            "timestamp": datetime.now().isoformat(),
            "total_experiments": len(self.results),
            "results": self.results,
        }

        with open(filepath, "w") as f:
            json.dump(output_data, f, indent=2)

        console.print(f"\n[green]Results saved to: {filepath}[/green]")
        return filepath

    def print_summary(self):
        table = Table(title="Experiment Summary")

        table.add_column("Experiment", style="cyan")
        table.add_column("Total Tests", style="magenta")
        table.add_column("Successful", style="green")
        table.add_column("Failed", style="red")

        experiment_counts: Dict[str, Dict[str, int]] = {}

        for result in self.results:
            exp_name = result.get("experiment", "unknown")
            if exp_name not in experiment_counts:
                experiment_counts[exp_name] = {"total": 0, "success": 0, "failed": 0}

            experiment_counts[exp_name]["total"] += 1
            if "error" in result:
                experiment_counts[exp_name]["failed"] += 1
            else:
                experiment_counts[exp_name]["success"] += 1

        for exp_name, counts in experiment_counts.items():
            table.add_row(
                exp_name.replace("_", " ").title(),
                str(counts["total"]),
                str(counts["success"]),
                str(counts["failed"]),
            )

        console.print("\n")
        console.print(table)
