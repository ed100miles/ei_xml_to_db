from sqlalchemy.orm import Session
import os
from sqalm import Activity, engine
from xmltodict import parse
from tqdm import tqdm

ei310_path = "/Users/edmiles/Code/ei/ei/data/ei310_cutoff_spold/datasets"


def get_general_comment(activity):
    if "generalComment" not in activity:
        return ""
    if "text" not in activity["generalComment"]:
        return ""
    if type(activity["generalComment"]["text"]) is list:
        return "\n".join(activity["generalComment"])
    return activity["generalComment"]["text"]["#text"]


with Session(engine) as session:
    for filename in tqdm(os.listdir(ei310_path)):
        with open(os.path.join(ei310_path, filename)) as f:
            xml = parse(f.read())
            if "childActivityDataset" in xml["ecoSpold"]:  # think about this
                activity_description = xml["ecoSpold"]["childActivityDataset"][
                    "activityDescription"
                ]
                activity = activity_description["activity"]
                classification = activity_description["classification"]
                geography = activity_description["geography"]
                time_period = activity_description["timePeriod"]

                # pprint(activity)

                act = Activity(
                    id=filename,
                    filename=filename,
                    activity_name=activity["activityName"]["#text"],
                    included_activities_start=(
                        activity["includedActivitiesStart"].get("#text", "")
                        if "includedActivitiesStart" in activity
                        else ""
                    ),
                    included_activities_end=(
                        activity["includedActivitiesEnd"].get("#text", "")
                        if "includedActivitiesEnd" in activity
                        else ""
                    ),
                    general_comments=get_general_comment(activity),
                    classification_system=str(classification),
                    classification_value=str(classification),
                    geography_shortname=geography["shortname"]["#text"],
                    # geography_comments: geography
                    time_period_start_data=time_period["@startDate"],
                    time_period_end_data=time_period["@endDate"],
                    time_period_is_data_valid_for_entire_period=time_period[
                        "@isDataValidForEntirePeriod"
                    ],
                    # time_period_comments: Mapped[str]
                )
                session.add(act)
    session.commit()
