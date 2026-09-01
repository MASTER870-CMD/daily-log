# daily-log-agent

Checks every day at 9pm IST whether you've authored a commit anywhere on
GitHub that day. If not, it adds one small, real entry (a TIL note, a
utility snippet, or a log line — your choice) to this repo and commits it,
so your contribution graph reflects an actual (if small) daily habit
rather than sitting empty — without ever touching your private/confidential
project repo.

## Setup

1. Create a **new public repo** on GitHub (e.g. `daily-log`) and push this
   folder's contents to it.
2. Create a **Personal Access Token**:
   - GitHub → Settings → Developer settings → Fine-grained tokens (or classic PAT with `repo` scope)
   - Give it read access to your repos (needed so the search API can see
     your commit activity, including private repos if you want those counted).
3. In the new repo → Settings → Secrets and variables → Actions → New repository secret:
   - Name: `DAILY_CHECK_PAT`
   - Value: the token from step 2
4. Edit `.github/workflows/daily-check.yml`:
   - Adjust the cron time if you're not in IST (`30 15 * * *` = 9:00pm IST / 15:30 UTC)
   - Set `CONTENT_MODE` to `til`, `snippet`, or `log`
5. Push. Test it immediately via the "Run workflow" button (Actions tab →
   Daily commit check → Run workflow) instead of waiting for 9pm.

## Notes

- The commit search checks **all repos your PAT can see**, public and
  private — so if you *do* commit somewhere else (even privately) that
  day, the bot correctly stays quiet.
- Edit `TIL_POOL` / `SNIPPET_POOL` in `scripts/generate_entry.py` to make
  the fallback content actually yours instead of the placeholder examples.
- If the GitHub search API has a hiccup, the script fails safe (assumes
  you *did* commit) so it won't spam a commit on an API error.
