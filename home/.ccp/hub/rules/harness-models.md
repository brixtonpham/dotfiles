# Harness and model routing

Google bans Antigravity accounts used through omp, so each harness has one lane.

- **omp runs DeepSeek only** (`opencode-go/deepseek-*`). Its model roles in
  `~/.omp/agent/config.yml` all point there. Never pick a `google-antigravity/*`
  model in omp, and never start omp with `--model google-antigravity/...`.
- **Gemini and Antigravity work goes through the `agy` CLI:**
  `agy --dangerously-skip-permissions --model gemini-4-argon-medium`
  (`agy models` lists the rest). agy cannot resume an omp conversation; hand it
  the context in the first prompt.
- **Spawning sessions** (agent-ops, `harness-ops spawn` / `task new`): use
  `--command "agy ..."` for Gemini work, `omp` only for DeepSeek work.
