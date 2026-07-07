# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

eAUrnik is a small Flask REST API that scrapes timetables from eAsistent (a Slovenian school
management system) and converts them to iCalendar (.ics) feeds. It returns the current week's
schedule, or from Saturday onward, next week's.

## Commands

```
pip install -r requirements.txt   # install dependencies
python API.py                     # run dev server (binds to :: on port 5000)
python -m unittest                # run tests (same as CI)
python -m unittest test_dates.py -k test_calculate_week   # run a single test
```

CI (`.github/workflows/python-app.yml`) runs on Python 3.12 via `pip install -r requirements.txt`
then `python -m unittest` on push/PR to `main`. There is no linter configured.

Deployment is to Vercel (`vercel.json`), which builds `API.py` with `@vercel/python` and routes
all requests through it.

## Architecture

Request flow across four modules, each with a single responsibility:

- **`API.py`** — Flask routes only. Maps three URL patterns (student, class, teacher-with-weeks)
  to `Timetable` functions and wraps the result as `text/calendar`.
- **`Timetable.py`** — orchestration and date math. Computes which Monday/school week to request,
  opens a scraping session against eAsistent, and drives `Parser` + `CalendarGenerator`.
- **`Parser.py`** — HTML scraping. Parses eAsistent's timetable HTML (via `lxml`) into a
  `(durations, lessons)` tuple: lesson time slots and a per-day/per-slot list of `(title, subtitle)`
  entries. Encodes eAsistent-specific quirks (see below).
- **`CalendarGenerator.py`** — turns the `Parser` output plus a starting Monday into an `ics`
  `Calendar` string.

Session handling: `Timetable.get_session()` hits `easistent.com` once and strips all cookies
except `vxcaccess` — eAsistent rejects requests carrying its other cookies.

School week numbering: `calculate_week()` treats Sept 1 (or the next weekday if it's a weekend)
as the start of week 1, and counts Mondays from there. This is what eAsistent's API expects as
its week parameter — see `test_dates.py` for the expected week boundaries.

eAsistent HTML quirks handled in `Parser.parse_block`:
- `ednevnik-seznam_ur_teden-td-odpadlo` (cancelled lesson) → skipped entirely.
- `ednevnik-seznam_ur_teden-td-nadomescanje` (substitution) → `" (N)"` appended to title.
- `ednevnik-seznam_ur_teden-td-zaposlitev` → `" (Z)"` appended to title.
- An icon titled `JV` or `PB` marks the block as absence/leave → skipped.

The eAsistent schedule URL encodes IDs positionally: school, class, professor, classroom,
(unused), week, student — passing `0` for any ID except school means "all". `Timetable.get_lessons`
is the single place that builds this URL.
