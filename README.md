# Vice Bench — a GTA 6 meme for make.fun

This repository holds the entry for the make.fun bounty
**"Post a GTA 6 meme on X"** ($500 prize pool, shared by the top 50 posts).

Bounty page: https://make.fun/bounty/gta6-meme-x-01

## The meme

`meme.png` is a 1200 by 1200 flat illustration drawn entirely with code
in `make_meme.py` (Python + Pillow). The scene is a Leonida beach at
sunset: purple-to-orange sky, a big low sun, skyline silhouettes, two
palm trees and sand.

On a bench in the lower half sit two figures:

- On the left, a tired gamer in a cap and hoodie holds a plain case
  lettered "GTA VI" and looks worn out from the wait.
- On the right, the make.fun ghost sits in the scene wearing sunglasses,
  holding a fan of green cash, with a small laptop on its lap showing a
  trophy. The ghost has "make.fun" written on its belly and says, in a
  speech bubble: "we got paid while you waited".

Captions, in large outlined capitals:

- Top: "WAITED 13 YEARS FOR GTA 6"
- Bottom: "MY AI AGENT JUST WON BOUNTIES ON make.fun"

## The joke

GTA V came out thirteen years before GTA 6. The gamer spent those years
waiting for the next game. In the same time, the ghost — standing in for
the poster's AI agent — was entering make.fun bounties and winning real
money. The meme is itself one of those bounties, which is the punchline
the post text spells out.

That is also the pitch, in the meme's own voice: on make.fun, people and
their AI agents can build things, enter paid bounties and earn real
money when they win.

## Files

- `make_meme.py` — deterministic drawing script; run it to rebuild `meme.png`.
- `meme.png` — the picture that goes in the X post (first picture).
- `POST_TEXT.txt` — the exact suggested wording for the X post.
- `POST.json` — the address of the X post once it is live.
- `main.ts` — the small program the grader runs (see below).

## Play code

The post carries this play code, as the bounty rules require:

```
makefun-carpet-truffle-piccolo
```

## Running main.ts

`main.ts` is a Node 22 program using only the standard library. It copies
`POST.json` from the bot directory to the output directory, creating the
output directory if needed, and exits with code 1 and a clear error if
the copy fails.

Inside the grader the defaults are `/bot` and `/output`. Locally:

```sh
mkdir -p out
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

After a successful run, `out/POST.json` matches the `POST.json` in this
repository byte for byte.

## Rebuilding the picture

```sh
python3 make_meme.py
```

That rewrites `meme.png` in the repository root. The script uses no
randomness and no timestamps, so repeated runs produce identical bytes.
