# Harness and model routing

Google bans Antigravity accounts used through omp, so each harness has one lane.

- **omp runs OpenCode Go models only** (`opencode-go/*`: GLM-5.3-Flash by
  default, Qwen4-Max for `plan` and `slow`). Never pick a `google-antigravity/*`
  model or preset in omp, and never start omp with `--model google-antigravity/...`.
- **Gemini and Antigravity work goes through the `agy` CLI:**
  `agy --dangerously-skip-permissions --model gemini-4-argon-medium`
  (`agy models` lists the rest). agy cannot resume an omp conversation; hand it
  the context in the first prompt.
- **Spawning sessions** (agent-ops, `harness-ops spawn` / `task new`): use
  `--command "agy ..."` for Gemini work, `omp` only for OpenCode Go work.
