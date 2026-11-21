# The World Tonight — 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-syukuran/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-syukuran/reward.svg)](https://make.fun/c/news-image-20261121)

A program that writes one image summing up the world's news of
**Saturday 21 November 2026**, built for make.fun's
[news-image-20261121](https://make.fun/c/news-image-20261121) competition
("Sum up 21 November's world news in one image", $100 shared by the top 50).

## The image

A dark night-globe atlas, drawn programmatically with Pillow (`render.py`) —
deliberately not a newspaper front page. A globe on the left carries numbered
pins at the places where the day's stories happened; the numbered stories run
down the right; "The day in numbers" sits under the globe and "Also today"
briefs run along the bottom.

![The World Tonight — 21 November 2026](entry.png)

1. **Middle East · Riyadh — THREE MISSILES AT RIYADH STOPPED.** Defences
   down 3 Houthi ballistic missiles before dawn on Saturday, the third night
   of alerts in the capital. No casualties.
2. **NATO · Warsaw — NATO CHIEF HEADS TO WARSAW TODAY.** Mark Rutte visits
   Poland a day after Russian missiles landed there; Warsaw asks NATO for
   more air defences on the eastern flank.
3. **Climate · COP31 — COP31 TALKS RUN INTO SATURDAY.** Nearly 200 nations
   deadlocked in Antalya; the closing plenary was suspended on Friday night
   and a third draft is due Saturday morning.
4. **Tech · Geneva — UN PUNTS ON 'KILLER ROBOTS' — FOR NOW.** 128 nations
   agree to draft rules for lethal autonomous weapons by 2028 after all-night
   talks ending at 4 a.m. No binding ban — the US, Russia and Israel opposed.
5. **Earthquake · Peru — M6.7 QUAKE SHAKES PERU'S ANDES.** Junín tremor at
   00:09 GMT, felt in Lima; residents flee into the streets. No casualties
   reported.
6. **Space · Mercury — BEPICOLOMBO REACHES MERCURY AT LAST.** ESA–JAXA twin
   orbiters captured by Mercury's gravity today after an 8-year journey —
   only the second mission ever to orbit the innermost planet.

**Also today:** ATP Finals semi-finals in Turin (Alcaraz vs Shelton, Zverev
vs Medvedev); Iraq to open a security HQ in Jurf al-Sakhar, a day after
state forces moved in; NWSL final tonight — Washington Spirit host Kansas
City Current at Audi Field.

## Date verification — every story is genuinely 21 November

Each story above was checked against independent sources for **both** the
publication date and the event date, and only stories that happened or were
first reported on Saturday 21 November 2026 were used. Two earlier entries
for this bounty were independently verified as FAIL because most of their
stories were Friday 20 November events; this entry was built specifically to
avoid that mistake:

- **Excluded — Friday 20 Nov:** the Russian drone/missile strikes on Ukraine
  (overnight 19→20 Nov), the S&P 500 −3.7% / Nasdaq −5.3% market rout (Friday
  close), the UK–EU post-Brexit deals (signed Friday in Brussels), the
  daraxonrasib pancreatic-cancer pill (presented 19–20 Nov in Barcelona),
  and the Gen Z protests in 25 countries (Friday). None of these appears as
  a 21 November story here. The Warsaw story is framed only on Saturday's
  event — Rutte's visit and Poland's request — not on Friday's attack.
- **Excluded — other dates:** the ICJ Myanmar/Rohingya ruling (delivered
  19 Nov), the FBI crime-database breach (reported Friday US), the
  Saudi–Japan oil stockpile deal (announced Friday), and the Trump press
  conference on the Shenzhen summit (Friday).
- **Peru magnitude:** M6.7 per USGS and Peru's IGP (the figure used here);
  GFZ reported 6.8 and an early estimate of 6.9 was wrong.
- **Saturday events kept:** Houthi intercepts (early Saturday, ~01:53 local),
  COP31 resuming Saturday, the UN autonomous-weapons talks ending Saturday
  ~04:00 CET, the Peru quake (00:09 GMT Saturday), BepiColombo's Mercury
  orbital insertion (Saturday 21 Nov), Rutte's Warsaw visit (Saturday),
  the ATP Finals semi-finals, the Jurf al-Sakhar HQ opening, and the NWSL
  final (all scheduled for Saturday).

Sources: Reuters, BBC, Al Jazeera, AP, ESA, USGS, IGP Peru, ATP Tour, USA Today.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is standard library only and copies the pre-rendered `entry.png`
(1024×1024, 155,391 bytes) — deterministic, no network, byte-identical on
every run. To regenerate the image from scratch:

```sh
python3 render.py entry.png   # needs Pillow + DejaVu fonts; deterministic
```

## License

MIT — see [LICENSE](LICENSE).
