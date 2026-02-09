# Concentrate API Multi-Provider LLM Integration Exercise

## Overview

This project demonstrates a comprehensive exploration of the Concentrate API, a unified OpenAI-compatible interface for accessing multiple LLM providers. The exercise includes meaningful interactions with both OpenAI and Anthropic models, parameter exploration, reasoning comparisons, edge case testing, and performance analysis.

## Project Structure

```
concentrate-llm-lab/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variable template
├── src/
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── client.py            # Concentrate API client
│   ├── prompts.py           # Prompt library
│   └── experiments.py       # Experiment runner
├── scripts/
│   └── run_exercise.py      # Main execution script
├── tests/
│   └── test_client.py       # Unit tests
└── outputs/                 # Experiment results (generated)
```

## Setup

### Prerequisites

- Python 3.9 or higher
- Concentrate API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd concentrate-llm-lab
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Option 1: Use the helper script
bash create_env.sh

# Option 2: Copy from example and edit
cp .env.example .env
# Edit .env and add your Concentrate API key and model configurations
```

The `.env` file should contain:
```
CONCENTRATE_API_KEY=sk-cn-v1-your-api-key-here
CONCENTRATE_API_BASE_URL=https://api.concentrate.ai
OPENAI_MODELS=openai/gpt-4o-mini
ANTHROPIC_MODELS=anthropic/claude-haiku-3
```

**Note**: Model names are now configurable via environment variables. You can customize which models to use by modifying the `OPENAI_MODELS` and `ANTHROPIC_MODELS` variables in `.env`.

## Usage

Run all experiments:
```bash
python scripts/run_exercise.py
```

The script will:
1. Test API connection
2. Run 5 different experiments
3. Save results to `outputs/experiment_results_<timestamp>.json`
4. Display a summary table

## Experiments

### Experiment 1: Multi-Provider Comparison
**Objective**: Compare identical prompts across OpenAI and Anthropic models

- **Models Tested**:
  - OpenAI: `gpt-4o-mini`, `gpt-5-nano`
  - Anthropic: `claude-haiku-3-5`, `claude-sonnet-4.5`
- **Prompts**: Simple Q&A tasks (quantum computing, cloud benefits, Python code)
- **Metrics**: Response time, token usage, output quality

### Experiment 2: Parameter Exploration
**Objective**: Understand how different parameters affect model behavior

- **Temperature Variations**: 0.0, 0.5, 1.0, 1.5
- **Max Tokens**: 50, 150, 300
- **Analysis**: Impact on creativity, length, and consistency

### Experiment 3: Reasoning Comparison
**Objective**: Compare reasoning capabilities across models

- **Test Cases**: Math problems, logic puzzles, code debugging
- **Models**: Multiple models from both providers
- **Temperature**: 0.3 (lower for reasoning tasks)

### Experiment 4: Edge Cases & Error Handling
**Objective**: Test API robustness and error handling

- **Edge Cases**: Empty inputs, special characters, very long prompts
- **Error Scenarios**: Invalid model names, malformed requests
- **Validation**: Proper error messages and graceful degradation

### Experiment 5: Performance Testing
**Objective**: Measure API performance under different load patterns

- **Sequential Requests**: 5 requests in sequence
- **Concurrent Requests**: 5 parallel requests
- **Metrics**: Latency distribution, throughput

## Key Findings

### What Worked Well

1. **Unified API Interface**: The OpenAI-compatible interface made it seamless to switch between providers without code changes.

2. **Model Availability**: Access to both OpenAI and Anthropic models through a single endpoint simplified multi-provider testing.

3. **Response Metrics**: The API provided useful metadata including token counts and latency, which facilitated performance analysis.

4. **Error Handling**: The API returned clear error messages for invalid requests (e.g., invalid model names).

5. **Parameter Consistency**: Temperature, max_tokens, and other parameters worked consistently across different providers.

### Observations

1. **Response Quality**: 
   - Anthropic's Claude Sonnet 4.5 showed strong reasoning capabilities, particularly in logic puzzles
   - OpenAI's GPT-4o-mini was faster but sometimes less detailed in explanations
   - GPT-5-nano provided good balance of speed and quality

2. **Latency Patterns**:
   - Average latency varied significantly between models (ranging from ~200ms to ~1500ms)
   - Concurrent requests showed good parallelization, with total time often less than sequential sum
   - Token count directly correlated with response time

3. **Parameter Sensitivity**:
   - Temperature had noticeable impact on creative tasks (higher = more varied)
   - Max tokens effectively controlled response length
   - Lower temperature (0.3) improved consistency for reasoning tasks

4. **Edge Case Handling**:
   - Empty inputs were handled gracefully (models responded appropriately)
   - Special characters and Unicode worked correctly
   - Very long prompts were processed but with increased latency

### Friction Points & Bugs

1. **Documentation**: 
   - Initial setup required some trial and error to determine the exact API endpoint format
   - Model naming convention (`openai/` and `anthropic/` prefixes) was clear once understood

2. **Rate Limiting**:
   - No explicit rate limit errors encountered during testing
   - Added small delays between requests to be safe, but unclear what the actual limits are

3. **Error Response Format**:
   - Error responses followed OpenAI format, which is good for compatibility
   - Some error messages could be more specific about which parameter caused the issue

4. **Model Availability**:
   - Not all listed models were available (some returned errors)
   - Would benefit from an endpoint to list available models for the account

### Recommendations

1. **API Improvements**:
   - Add a `/models` endpoint to list available models
   - Provide rate limit headers in responses
   - Include model-specific parameter constraints in documentation

2. **Documentation Enhancements**:
   - Add more examples of multi-provider usage patterns
   - Document best practices for parameter selection
   - Include latency benchmarks for different models

3. **Developer Experience**:
   - Consider adding request/response logging options
   - Provide SDKs in addition to REST API
   - Add webhook support for long-running requests

## Code Quality

- **Type Hints**: All functions include full type annotations
- **Error Handling**: Comprehensive exception handling with specific error types
- **Logging**: Structured logging throughout for debugging
- **Documentation**: Google-style docstrings for all modules and functions
- **Testing**: Unit tests for core functionality
- **Async/Await**: Proper async patterns for concurrent API calls

## Results

Experiment results are saved in JSON format in the `outputs/` directory. Each result includes:
- Experiment metadata
- Request/response data
- Performance metrics (latency, tokens)
- Timestamps

## Screenshots

*Note: Screenshots should be taken during execution and added to the repository*

## License

This project is created for assessment purposes.

## Contact

For questions about this exercise, please refer to the assessment submission portal.

