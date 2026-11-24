# The Daily World — 23 November 2026 in one image

[![Built for make.fun](https://img.shields.io/badge/make.fun-news--image--20261123-7c3aed)](https://make.fun)

Built for the [make.fun](https://make.fun) competition
[news-image-20261123](https://make.fun/bounty/news-image-20261123):
sum up the world's news of Monday 23 November 2026 in one image.

## What it is

`main.py` draws a one-page newspaper, **THE DAILY WORLD**, entirely with
Pillow vector drawing — no photos, no network, no downloaded assets.
Six real stories from 23 November 2026:

1. **Lead — Nvidia:** Jensen Huang reinstated as CEO; shares surge 31%.
2. **Ukraine:** sea drones sink a Russian warship at Benghazi, Libya.
3. **Climate:** COP31 in Turkey ends with no deal after record-long talks.
4. **Kyiv:** Russian strikes kill at least 15 people around the capital.
5. **Space:** BepiColombo enters orbit around Mercury after eight years.
6. **Sport:** the UK is confirmed as host of the 2035 Women's World Cup.

A bottom strip also notes the NHS AI breast-screening trial, eurozone
inflation at 4.0%, and the Indonesian factory fire that killed 24.

## Run it

```sh
python3 main.py        # writes /output/entry.png (1024x1024, <= 1 MiB)
```

Run twice: both runs write byte-identical PNGs.

## License

MIT — see [LICENSE](LICENSE).
