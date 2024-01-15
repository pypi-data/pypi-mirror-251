import hashlib
import logging
import pathlib
import sys
import traceback

import pandas as pd
from tqdm import tqdm

from geo_activity_playground.core.activities import ActivityMeta
from geo_activity_playground.core.activity_parsers import ActivityParseError
from geo_activity_playground.core.activity_parsers import read_activity
from geo_activity_playground.core.tasks import WorkTracker

logger = logging.getLogger(__name__)


def import_from_directory() -> None:
    meta_file = pathlib.Path("Cache") / "activities.parquet"
    if meta_file.exists():
        meta = pd.read_parquet(meta_file)
    else:
        meta = None

    paths_with_errors = []
    work_tracker = WorkTracker("parse-activity-files")

    activity_paths = {
        int(hashlib.sha3_224(str(path).encode()).hexdigest(), 16) % 2**62: path
        for path in pathlib.Path("Activities").rglob("*.*")
        if path.is_file() and path.suffixes
    }
    activities_ids_to_parse = work_tracker.filter(activity_paths.keys())

    activity_stream_dir = pathlib.Path("Cache/Activity Timeseries")
    activity_stream_dir.mkdir(exist_ok=True, parents=True)
    new_rows: list[dict] = []
    for activity_id in tqdm(activities_ids_to_parse, desc="Parse activity files"):
        path = activity_paths[activity_id]
        try:
            activity_meta_from_file, timeseries = read_activity(path)
        except ActivityParseError as e:
            logger.error(f"Error while parsing file {path}:")
            traceback.print_exc()
            paths_with_errors.append((path, str(e)))
            continue
        except:
            logger.error(f"Encountered a problem with {path=}, see details below.")
            raise

        work_tracker.mark_done(activity_id)

        if len(timeseries) == 0:
            continue

        timeseries_path = activity_stream_dir / f"{activity_id}.parquet"
        timeseries.to_parquet(timeseries_path)

        activity_meta = ActivityMeta(
            commute=path.parts[-2] == "Commute",
            id=activity_id,
            # https://stackoverflow.com/a/74718395/653152
            name=path.name.removesuffix("".join(path.suffixes)),
            path=str(path),
        )
        if len(path.parts) >= 3 and path.parts[1] != "Commute":
            activity_meta["kind"] = path.parts[1]
        if len(path.parts) >= 4 and path.parts[2] != "Commute":
            activity_meta["equipment"] = path.parts[2]

        activity_meta.update(activity_meta_from_file)
        new_rows.append(activity_meta)

    if paths_with_errors:
        logger.warning(
            "There were errors while parsing some of the files. These were skipped and tried again next time."
        )
        for path, error in paths_with_errors:
            logger.error(f"{path}: {error}")

    new_df = pd.DataFrame(new_rows)
    merged = pd.concat([meta, new_df])

    if len(merged) == 0:
        activities_dir = pathlib.Path("Activities").resolve()
        logger.error(
            f"You seemingly want to use activity files as a data source, but you have not copied any GPX/FIT/TCX/KML files."
            f"Please copy at least one such file into {activities_dir}."
        )
        sys.exit(1)

    merged.sort_values("start", inplace=True)
    meta_file.parent.mkdir(exist_ok=True, parents=True)
    merged.to_parquet(meta_file)
    work_tracker.close()
