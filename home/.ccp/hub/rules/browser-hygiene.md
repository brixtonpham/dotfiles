# Browser and RAM hygiene

Browsers, renders, dev servers and parallel jobs eat RAM and outlive the task if left open.
This Mac crashes when free RAM runs out, and many sessions share it.

- **RAM ceiling: 80% used, so at least 20% stays free at all times.** Check with
  `memory_pressure | tail -1` (the "free percentage" line).
  - Before anything heavy (browser, render, build, model run, a batch of agents):
    start it only when free is 30% or more, so it has room to grow.
  - Under 30% free: start nothing new until you've closed something, or run the
    job on the home box.
  - Under 20% free: close your idle browsers, servers and renders now, and shrink
    your agent pool.
- **Close what you open, as soon as you're done** — not at the end of the session:
  - `bsk`: `bsk tab close` the tabs you opened, then `bsk session stop <your-id>`
    (never `--all`).
  - Headless: Puppeteer/Playwright, headless Chrome (`--print-to-pdf`,
    screenshots). Call `browser.close()` / kill your own PID.
  - Claude in Chrome / `omp` `browser`: close the tabs you created.
  - Dev servers (`next dev` etc.): kill them.
- **Renders** (Remotion, ffmpeg, video/image batches):
  - Run them on the home box when it's up and its GPU is idle (`ssh me.ubuntu.home nvidia-smi`).
  - Locally, one render at a time with capped parallelism (Remotion `--concurrency 2`).
  - After it finishes or fails, make sure its `chrome-headless-shell` and ffmpeg
    processes are gone.
- **Confirm:** `ps -ax | grep -E 'chrome-headless|headless|remotion|ffmpeg'` and
  `bsk session list` show none of yours.
- **Only yours.** Never kill a process another session started (e.g. a video render).
- Tell subagents and workflow agents this rule when they will browse, render or
  screenshot, or run heavy jobs.
