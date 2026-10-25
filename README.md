# OpenCode + Qwen: local coding setup

Three small Python projects to try with **OpenCode + Ollama + Qwen3.5 9B**. Download the tools and model first, then disconnect the internet and ask the agent to read code, make changes and run tests on your Mac.

All three examples use Python's standard library. Their starting code is deliberately broken or unfinished so you have a task for the agent.

| Example | Task | Tests |
| --- | --- | --- |
| [Expense total](#4-check-the-first-example) | Fix a function that adds expenses | 5 |
| [CSV sales report](examples/csv-report/README.md) | Implement a report from local CSV data | 7 |
| [Log analyzer](examples/log-analyzer/README.md) | Fix error counts and slowest-request reporting | 7 |

This is a hands-on walkthrough, not a model benchmark. The expense fix was completed in the recorded walkthrough; the other two projects are exercises to try with the same setup.

## Before you start

This guide is for macOS and assumes Homebrew is installed. The walkthrough used an Apple M5 MacBook Air with 24 GB of unified memory. Qwen's download was about 7.6 GB in that setup; runtime memory also needs room for the context and other apps.

- **Terminal A:** installations, downloads, OpenCode and tests.
- **Terminal B:** Ollama only. Leave it running.
- Run **one command at a time** and check the result before continuing.

## 1. Get the project and install the tools

While connected to the internet, run this in **Terminal A**:

```bash
brew install ollama node python git
```

Create the project folder:

```bash
mkdir -p "$HOME/Projects/localcode"
```

Clone this repository:

```bash
git clone https://github.com/RittikaJ/opencode-qwen-local-setup.git "$HOME/Projects/localcode/opencode-qwen-local-setup"
```

Open it:

```bash
cd "$HOME/Projects/localcode/opencode-qwen-local-setup"
```

Install the OpenCode version used in the walkthrough:

```bash
npm install --prefix .tools --save-exact opencode-ai@1.19.4
```

Wait for the prompt to return, then check its version:

```bash
.tools/node_modules/.bin/opencode --version
```

Expected: `1.19.4`.

## 2. Start Ollama

Open **Terminal B** and run:

```bash
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 OLLAMA_CONTEXT_LENGTH=65536 ollama serve
```

Leave this window running. Ollama serves the model on this Mac with its cloud features disabled.

## 3. Download Qwen

Back in **Terminal A**, while still online:

```bash
ollama pull qwen3.5:9b
```

Wait for `success`, then check the model list:

```bash
ollama list
```

Expected: a row containing `qwen3.5:9b`.

The included [opencode.json](opencode.json) selects this local model for both the main and helper model. It points to Ollama at `http://127.0.0.1:11434/v1`, asks before edits and shell commands, and disables web search and fetching.

## 4. Check the first example

In **Terminal A**, from the repository root:

```bash
python3 expense_total.py
```

The starter prints `8.00`; the correct total is `25.50`.

Run the tests:

```bash
python3 -m unittest -v
```

Expected before the fix: **three failures out of five tests**. These failures are intentional. The tests cover the sample expenses, refunds, decimal arithmetic, an empty list and a single expense.

## 5. Open the local agent while online

In **Terminal A**:

```bash
.tools/node_modules/.bin/opencode --pure
```

OpenCode reads the local model configuration from this folder. `--pure` disables external plugins. Check that **Qwen3.5 9B local** is selected.

Enter this in OpenCode:

```text
Read expense_total.py and run the tests. Explain the bug without editing any files.
```

Review and approve the local test command if asked. Wait for the answer, then exit OpenCode:

```text
/exit
```

Leave Ollama running in Terminal B. Use this same direct launch command for the offline run so the required runtime components are already available.

## 6. Disconnect the internet

Turn **Wi-Fi off**. Disconnect Ethernet or phone tethering if connected.

In **Terminal A**, check that Ollama still responds:

```bash
curl --noproxy '*' --fail http://127.0.0.1:11434/api/tags
```

Expected: JSON listing `qwen3.5:9b`. Localhost connects within your Mac, so it works without Wi-Fi.

Try an external address:

```bash
curl --noproxy '*' --connect-timeout 5 --max-time 10 --head https://example.com
```

This should fail. Our walkthrough returned `Could not resolve host: example.com`. Keep external connections disconnected during the task; this request is a spot check of connectivity.

## 7. Ask OpenCode to fix the code offline

In **Terminal A**:

```bash
.tools/node_modules/.bin/opencode --pure
```

Use **Build** mode and enter:

```text
Fix the bug in expense_total.py so the existing tests pass. Don't change the tests or install anything. Run the tests and explain your fix.
```

Review and approve its requests to edit the file and run the tests.

## 8. Check the result yourself

When OpenCode finishes, exit:

```text
/exit
```

Run the tests in **Terminal A**:

```bash
python3 -m unittest -v
```

Expected after a successful fix: **all five tests pass**.

Run the program:

```bash
python3 expense_total.py
```

Expected: `25.50`.

Review the changes and check that the tests were not edited:

```bash
git diff
```

## 9. Try the other two projects

Continue from the repository root with Ollama still running in Terminal B:

- **[Build a CSV sales report](examples/csv-report/README.md):** group products, add quantities and revenue, and format a report. The starter is unfinished; all seven tests initially fail or error.
- **[Fix a log analyzer](examples/log-analyzer/README.md):** count HTTP errors and select the slowest request. The starter has three failures out of seven tests.

Each walkthrough includes a prompt, exact test commands and expected output. These expected results are targets for the exercise, not claims that every model attempt will succeed. Keep the original tests and run them yourself after reviewing the agent's changes.

When finished, press **Control + C** in Terminal B to stop Ollama.

## Useful references

- [Ollama with OpenCode](https://docs.ollama.com/integrations/opencode)
- [OpenCode configuration](https://opencode.ai/docs/config/)
- [Qwen3.5 9B model card](https://huggingface.co/Qwen/Qwen3.5-9B)
