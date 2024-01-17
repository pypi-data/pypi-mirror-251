from typing import List

import termcolor

from duckietown_challenges import dtserver_get_user_submissions
from duckietown_challenges.utils import pad_to_screen_length
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations

__all__ = ["dt_challenges_cli_list"]


def dt_challenges_cli_list(args: List[str], environment: ChallengeEnvironment):
    """Lists submissions on the server."""
    token = environment.token
    _ = args
    with wrap_server_operations():
        submissions = dtserver_get_user_submissions(token)

    def key(x):
        return submissions[x]["date_submitted"]

    challenge_id2name = {}
    for submission_id, submission in list(submissions.items()):

        if not submission.get("challenge_is_open", True):
            continue

        challenge_id = submission["challenge_id"]
        challenge_name = submission.get("challenge_name", "%s" % challenge_id)
        challenge_id2name[challenge_id] = challenge_name

    challenges = sorted(challenge_id2name)
    out = []

    for challenge_id in challenges:
        out.append("")
        out.append(bold(f"Challenge {challenge_id2name[challenge_id]}"))
        out.append("")
        for submission_id in sorted(submissions, key=key):
            submission = submissions[submission_id]

            if submission["challenge_id"] != challenge_id:
                continue

            def d(dt):
                return dt.strftime("%Y-%m-%d %H:%M")

            from duckietown_challenges import get_duckietown_server_url

            server = get_duckietown_server_url()

            url = server + "/humans/submissions/%s" % submission_id

            user_label = submission.get("user_label", None) or dark("(no user label)")

            M = 30
            if len(user_label) > M:
                user_label = user_label[: M - 5] + " ..."

            user_label = user_label.ljust(M)

            s = "%4s  %s  %10s %s  %s" % (
                submission_id,
                d(submission["date_submitted"]),
                pad_to_screen_length(colored_status(submission["status"]), 10),
                user_label,
                href(url),
            )

            out.append(s)
        out.append("")

    msg = "\n".join(out)

    sprint(msg)


def colored_status(status):
    return termcolor.colored(status, color_status(status))


def color_status(s):
    colors = {
        "success": "green",
        "evaluating": "blue",
        "failed": "red",
        "retired": "cyan",
        "error": "red",
    }

    if s in colors:
        return colors[s]
    else:
        return "white"


def href(x):
    return termcolor.colored(x, "blue", attrs=["underline"])


def bold(x):
    return termcolor.colored(x, "white", attrs=["bold"])


def dark(x):
    return termcolor.colored(x, attrs=["dark"])
