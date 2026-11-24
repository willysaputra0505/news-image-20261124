# The World in One Day — Tuesday, 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/willysaputra0505/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/willysaputra0505/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single 1024×1024 poster summing up the world's news of Tuesday 24 November 2026, drawn deterministically with Python + PIL.

## The day's stories

1. **Russian strikes kill at least 12 in Kyiv region** — A drone flattens a block of flats in Dymer; rescuers still search the rubble for the missing. *(Reuters)*
2. **Huang's return lifts tech: Nvidia adds nearly $1tn** — Nvidia jumps 31% as its founder is reinstated; SK hynix ADRs surge 20% and Asian markets rally. *(Seoul Economic Daily / AJP)*
3. **Denmark's top court backs 'ghetto law' evictions** — The Supreme Court rules the housing law is not ethnic discrimination, backing the hard line on immigration. *(Reuters)*
4. **Trump gets path to erase hush-money conviction** — Appeals judges revive his bid to move the case to federal court, where he can argue immunity. *(AP)*
5. **Java factory fire: 24 dead, about 30 still missing** — Rescuers pick through the ruined candy plant in Cikande as DNA tests are needed to name the dead. *(Reuters / Bernama)*
6. **FIFA picks 2031 and 2035 Women's Cup hosts** — USA, Mexico, Costa Rica and Jamaica take 2031 — the first 48-team edition; the UK hosts 2035. *(FIFA)*

Also today: Ukraine strikes back — drones hit oil sites in Tatarstan, Perm and Rostov; NATO meets — allies meet in Brussels over missiles in Poland; Grok sued — Virginia and Oregon sue SpaceX over Grok images; under-16 ban — Bangladesh court orders social-media limits.

## Run it

```sh
python3 generate.py   # renders entry.png (1024x1024, < 1 MiB)
node main.ts          # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`generate.py` draws the poster with PIL primitives only — no network, no randomness, no timestamps — so two runs produce identical bytes. `main.ts` uses Node 22 stdlib only: it checks `entry.png` exists, creates the output directory, copies the file, and verifies the output size.

## Files

- `entry.png` — the poster
- `generate.py` — the PIL poster generator (all icons drawn with PIL primitives)
- `main.ts` — the make.fun entry point
