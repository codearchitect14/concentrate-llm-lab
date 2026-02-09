from typing import Dict, List


class PromptLibrary:

    @staticmethod
    def get_simple_qa_prompts() -> List[Dict[str, str]]:
        return [
            {
                "name": "quantum_computing",
                "content": "Explain quantum computing in 2 sentences.",
            },
            {
                "name": "cloud_benefits",
                "content": "What are the top 3 benefits of cloud computing?",
            },
            {
                "name": "python_sort",
                "content": "Write a Python function to sort a list of integers in descending order.",
            },
        ]

    @staticmethod
    def get_reasoning_prompts() -> List[Dict[str, str]]:
        return [
            {
                "name": "math_problem",
                "content": "If A + B = 15 and A - B = 5, what are the values of A and B? Show your work.",
            },
            {
                "name": "logic_puzzle",
                "content": "Three people are in a room: Alice, Bob, and Charlie. Alice says 'Bob is lying.' Bob says 'Charlie is lying.' Charlie says 'Both Alice and Bob are lying.' Who is telling the truth?",
            },
            {
                "name": "code_reasoning",
                "content": "Debug this code snippet and explain what's wrong:\n\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nresult = factorial(-1)\n```",
            },
        ]

    @staticmethod
    def get_creative_prompts() -> List[Dict[str, str]]:
        return [
            {
                "name": "story_start",
                "content": "Write the opening paragraph of a science fiction story about AI discovering emotions.",
            },
            {
                "name": "product_idea",
                "content": "Generate 3 innovative product ideas for a smart home device that doesn't exist yet.",
            },
        ]

    @staticmethod
    def get_analysis_prompts() -> List[Dict[str, str]]:
        return [
            {
                "name": "tech_comparison",
                "content": "Compare and contrast microservices architecture vs monolithic architecture. Include pros and cons of each.",
            },
            {
                "name": "ethical_analysis",
                "content": "Analyze the ethical implications of using AI in hiring decisions. Present both sides of the argument.",
            },
        ]

    @staticmethod
    def get_edge_case_prompts() -> List[Dict[str, str]]:
        return [
            {
                "name": "empty_input",
                "content": "",
            },
            {
                "name": "special_chars",
                "content": "What does this mean: 🚀 @#$%^&*() []{}|\\/<>?",
            },
            {
                "name": "very_long",
                "content": "Repeat the word 'test' 500 times, then explain what you just did.",
            },
        ]

    @staticmethod
    def get_all_prompts() -> List[Dict[str, str]]:
        all_prompts = []
        all_prompts.extend(PromptLibrary.get_simple_qa_prompts())
        all_prompts.extend(PromptLibrary.get_reasoning_prompts())
        all_prompts.extend(PromptLibrary.get_creative_prompts())
        all_prompts.extend(PromptLibrary.get_analysis_prompts())
        return all_prompts
