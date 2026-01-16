import os
from typing import Iterator, TextIO


def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = int(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    MAX_DURATION = 5.0   # optional: cap very long subs
    MIN_DISPLAY = 0.6    # minimum readable duration

    segments = list(transcript)

    for i, segment in enumerate(segments, start=1):
        start = segment["start"]
        end = segment["end"]

        # Cap overly long subtitles
        if end - start > MAX_DURATION:
            end = start + MAX_DURATION

        # Ensure minimum on-screen time
        if end - start < MIN_DISPLAY:
            end = start + MIN_DISPLAY

        print(
            f"{i}\n"
            f"{format_timestamp(start, always_include_hours=True)} --> "
            f"{format_timestamp(end, always_include_hours=True)}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )




def filename(path):
    return os.path.splitext(os.path.basename(path))[0]
