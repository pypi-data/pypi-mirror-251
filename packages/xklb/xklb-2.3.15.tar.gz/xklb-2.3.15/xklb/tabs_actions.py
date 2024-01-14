import argparse, math, webbrowser
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple

from xklb import history, usage
from xklb.media import media_printer
from xklb.utils import arg_utils, consts, db_utils, iterables, objects, processes
from xklb.utils.log_utils import log


def parse_args(action) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="library tabs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage=usage.tabs,
    )

    parser.add_argument("--sort", "-u", nargs="+")
    parser.add_argument("--where", "-w", nargs="+", action="extend", default=[])
    parser.add_argument("--include", "-s", "--search", nargs="+", action="extend", default=[])
    parser.add_argument("--exclude", "-E", "-e", nargs="+", action="extend", default=[])
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--print", "-p", default="", const="p", nargs="?")
    parser.add_argument("--cols", "-cols", "-col", nargs="*", help="Include a column when printing")
    parser.add_argument(
        "--delete",
        "--remove",
        "--erase",
        "--rm",
        "-rm",
        action="store_true",
        help="Delete matching rows",
    )
    parser.add_argument("--limit", "-L", "-l", "-queue", "--queue")
    parser.add_argument("--skip")

    parser.add_argument("--db", "-db")
    parser.add_argument("--verbose", "-v", action="count", default=0)

    parser.add_argument("database")
    parser.add_argument("search", nargs="*")
    args = parser.parse_intermixed_args()
    args.action = action

    args.include += args.search
    if args.include == ["."]:
        args.include = [str(Path().cwd().resolve())]

    if args.db:
        args.database = args.db

    if args.sort:
        args.sort = [arg_utils.override_sort(s) for s in args.sort]
        args.sort = " ".join(args.sort)

    if args.cols:
        args.cols = list(iterables.flatten([s.split(",") for s in args.cols]))

    if args.delete:
        args.print += "d"

    if args.db:
        args.database = args.db
    args.db = db_utils.connect(args)
    log.info(objects.dict_filter_bool(args.__dict__))

    return args


def tabs_include_sql(x) -> str:
    return f"""and (
    path like :include{x}
    OR category like :include{x}
    OR frequency like :include{x}
)"""


def tabs_exclude_sql(x) -> str:
    return f"""and (
    path not like :exclude{x}
    AND category not like :exclude{x}
    AND frequency not like :exclude{x}
)"""


def construct_tabs_query(args) -> Tuple[str, dict]:
    args.filter_sql = []
    args.filter_bindings = {}

    args.filter_sql.extend([" and " + w for w in args.where])

    for idx, inc in enumerate(args.include):
        args.filter_sql.append(tabs_include_sql(idx))
        if args.exact:
            args.filter_bindings[f"include{idx}"] = inc
        else:
            args.filter_bindings[f"include{idx}"] = "%" + inc.replace(" ", "%").replace("%%", " ") + "%"
    for idx, exc in enumerate(args.exclude):
        args.filter_sql.append(tabs_exclude_sql(idx))
        if args.exact:
            args.filter_bindings[f"exclude{idx}"] = exc
        else:
            args.filter_bindings[f"exclude{idx}"] = "%" + exc.replace(" ", "%").replace("%%", " ") + "%"

    LIMIT = "LIMIT " + str(args.limit) if args.limit else ""
    OFFSET = f"OFFSET {args.skip}" if args.skip else ""

    query = f"""WITH m as (
            SELECT
                path
                , frequency
                , COALESCE(MAX(h.time_played), 0) time_last_played
                , SUM(CASE WHEN h.done = 1 THEN 1 ELSE 0 END) play_count
                , time_deleted
                , hostname
                , category
            FROM media
            LEFT JOIN history h on h.media_id = media.id
            WHERE COALESCE(time_deleted, 0)=0
            GROUP BY media.id
        )
        SELECT path
        , frequency
        {", time_last_played" if args.print else ''}
        , CASE
            WHEN frequency = 'daily' THEN cast(STRFTIME('%s', datetime( time_last_played, 'unixepoch', '+1 Day', '-5 minutes' )) as int)
            WHEN frequency = 'weekly' THEN cast(STRFTIME('%s', datetime( time_last_played, 'unixepoch', '+7 Days', '-5 minutes' )) as int)
            WHEN frequency = 'monthly' THEN cast(STRFTIME('%s', datetime( time_last_played, 'unixepoch', '+1 Month', '-5 minutes' )) as int)
            WHEN frequency = 'quarterly' THEN cast(STRFTIME('%s', datetime( time_last_played, 'unixepoch', '+3 Months', '-5 minutes' )) as int)
            WHEN frequency = 'yearly' THEN cast(STRFTIME('%s', datetime( time_last_played, 'unixepoch', '+1 Year', '-5 minutes' )) as int)
        END time_valid
        {', ' + ', '.join(args.cols) if args.cols else ''}
    FROM m
    WHERE 1=1
        {" ".join(args.filter_sql)}
        {f"and time_valid < {consts.today_stamp()}" if not args.print else ''}
    ORDER BY 1=1
        {', ' + args.sort if args.sort else ''}
        {', time_last_played, time_valid, path' if args.print else ''}
        , play_count
        , frequency = 'daily' desc
        , frequency = 'weekly' desc
        , frequency = 'monthly' desc
        , frequency = 'quarterly' desc
        , frequency = 'yearly' desc
        , ROW_NUMBER() OVER ( PARTITION BY
            play_count
            , frequency
            , hostname
            , category
        ) -- prefer to spread hostname, category over time
        , random()
    {LIMIT} {OFFSET}
    """

    return query, args.filter_bindings


def play(args, m: Dict) -> None:
    media_file = m["path"]

    webbrowser.open(media_file, 2, autoraise=False)
    history.add(args, [media_file], time_played=consts.today_stamp(), mark_done=True)


def frequency_filter(counts, media: List[Dict]) -> List[dict]:
    mapper = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "quarterly": 91,
        "yearly": 365,
    }
    filtered_media = []
    for freq, freq_count in counts:
        num_days = mapper.get(freq, 365)
        num_tabs = max(1, math.ceil(freq_count / num_days))
        log.debug(f"freq_count {freq_count} / num_days {num_days} = num_tabs {num_tabs}")

        filtered_media.extend([m for m in media if m["frequency"] == freq][:num_tabs])

    return filtered_media


def open_tabs(args, media):
    for m in media:
        play(args, m)
        MANY_TABS = 9
        if len(media) >= MANY_TABS:
            sleep(0.3)


def tabs() -> None:
    args = parse_args(consts.SC.tabs)
    history.create(args)

    query, bindings = construct_tabs_query(args)

    if args.print:
        media_printer.printer(args, query, bindings)
        return

    media = list(args.db.query(query, bindings))
    if not media:
        processes.no_media_found()

    counts = args.db.execute("select frequency, count(*) from media group by 1").fetchall()
    media = frequency_filter(counts, media)

    open_tabs(args, media)
