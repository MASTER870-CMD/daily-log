"""
Generates one genuinely useful log entry when no commit happened today.
Pick a mode with the CONTENT_MODE env var: til | snippet | log

- til:     a short "today I learned" style note pulled from a rotating pool
- snippet: a small, real, usable utility function in a rotating pool of languages
- log:     a plain changelog-style note (good if you want to manually edit
           log/today.md yourself before 9pm and have this just confirm it)

Nothing here is meaningless padding — each entry is real content you could
actually read back later. Edit the POOLs below to make them genuinely yours.
"""
# import os
# import datetime
# import random

# MODE = os.environ.get("CONTENT_MODE", "til")
# today = datetime.date.today().isoformat()
# log_dir = "log"
# os.makedirs(log_dir, exist_ok=True)

import os
import datetime
import random
import time

MODE = os.environ.get("CONTENT_MODE", "til")
today = datetime.date.today().isoformat()
unique_suffix = str(int(time.time() * 1000))[-6:]
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

TIL_POOL = [
    "Python's `bisect` module gives O(log n) insertion point lookup for sorted lists — useful before reaching for a full sort.",
    "`git commit --fixup=<sha>` + `git rebase -i --autosquash` cleanly folds a fix into an earlier commit without a manual reorder.",
    "SQL window functions (`ROW_NUMBER() OVER (PARTITION BY ...)`) avoid a self-join for 'latest row per group' queries.",
    "HTTP 429 responses should be respected with the `Retry-After` header rather than a fixed backoff — many APIs set it explicitly.",
    "`curl -w '%{time_total}'` is a quick way to check request latency without extra tooling.",
]

SNIPPET_POOL = [
    ("chunk.py", "def chunk(iterable, size):\n    \"\"\"Yield successive `size`-length chunks from iterable.\"\"\"\n    it = iter(iterable)\n    while batch := list(__import__('itertools').islice(it, size)):\n        yield batch\n"),
    ("debounce.js", "function debounce(fn, wait) {\n  let t;\n  return (...args) => {\n    clearTimeout(t);\n    t = setTimeout(() => fn(...args), wait);\n  };\n}\n"),
    ("retry.py", "import time\n\ndef retry(fn, attempts=3, backoff=1.0):\n    for i in range(attempts):\n        try:\n            return fn()\n        except Exception:\n            if i == attempts - 1:\n                raise\n            time.sleep(backoff * (2 ** i))\n"),
]

def write(path, content):
    with open(path, "w") as f:
        f.write(content)

message = ""

# if MODE == "til":
#     note = random.choice(TIL_POOL)
#     path = f"{log_dir}/{today}-til.md"
#     write(path, f"# TIL — {today}\n\n{note}\n")
#     message = f"til: {today}"

# elif MODE == "snippet":
#     fname, code = random.choice(SNIPPET_POOL)
#     path = f"{log_dir}/{today}-{fname}"
#     write(path, code)
#     message = f"snippet: {fname} ({today})"

# else:  # "log"
#     path = f"{log_dir}/{today}-log.md"
#     write(path, f"# {today}\n\nNo public commit today — working on private work not pushed to GitHub.\n")
#     message = f"log: {today}"


if MODE == "til":
    note = random.choice(TIL_POOL)
    path = f"{log_dir}/{today}-{unique_suffix}-til.md"
    write(path, f"# TIL — {today}\n\n{note}\n")
    message = f"til: {today}"

elif MODE == "snippet":
    fname, code = random.choice(SNIPPET_POOL)
    path = f"{log_dir}/{today}-{unique_suffix}-{fname}"
    write(path, code)
    message = f"snippet: {fname} ({today})"

else:  # "log"
    path = f"{log_dir}/{today}-{unique_suffix}-log.md"
    write(path, f"# {today}\n\nNo public commit today — working on private work not pushed to GitHub.\n")
    message = f"log: {today}"

with open("/tmp/commit_message.txt", "w") as f:
    f.write(message)

print(f"Wrote {path} — {message}")
