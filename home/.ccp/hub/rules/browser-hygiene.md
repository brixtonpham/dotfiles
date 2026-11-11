# Browser and RAM hygiene

Browsers, dev servers and parallel jobs eat RAM and outlive the task if left open.
This Mac crashes when free RAM runs out, and many sessions share it.

- **Close what you open, as soon as you're done:**
  - Headless: Remotion `chrome-headless-shell`, Puppeteer/Playwright, headless
    Chrome (`--print-to-pdf`, screenshots). Call `browser.close()` / kill your own PID.
  - `bsk`: `bsk tab close` the tabs you opened, then `bsk session stop <your-id>`
    (never `--all`).
  - Claude in Chrome / `omp` `browser`: close the tabs you created.
  - Dev servers (`next dev` etc.): kill them.
- **Keep 20–30% RAM free.** Before starting anything heavy (browser, render, build,
  model run, a batch of agents), run `memory_pressure | tail -1`.
  - Under 30% free: start nothing new until you've closed something, or run the job
    on the home box.
  - Under 20% free: close your idle browsers and servers now, and shrink your agent pool.
- **Confirm:** `ps -ax | grep -E 'chrome-headless|headless'` and `bsk session list`
  show none of yours.
- **Only yours.** Never kill a process another session started (e.g. a video render).
- Tell subagents and workflow agents this rule when they will browse, render or
  screenshot, or run heavy jobs.
