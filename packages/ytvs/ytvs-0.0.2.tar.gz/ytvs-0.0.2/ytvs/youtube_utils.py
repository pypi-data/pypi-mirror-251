"""
    This provide some common utils methods for YouTube resource.
"""

import isodate
from isodate.isoerror import ISO8601Error

from pyyoutube.error import ErrorMessage, PyYouTubeException


def get_video_duration(duration: str) -> int:
    """
    ISO 8601 형식의 비디오 지속 시간을 초 단위로 변환합니다. 이 형식은 YouTube API에서 비디오 지속 시간을 표현하는 데 사용됩니다.
    예: 'PT14H23M42S'는 '14시간 23분 42초'를 나타냅니다.

    Args:
        duration (str): ISO 8601 형식의 비디오 지속 시간입니다.

    Returns:
        int: 지속 시간을 초 단위로 나타낸 정수값입니다.

    예외 처리:
        ISO8601Error: 지속 시간의 형식이 잘못되었을 때 발생합니다.
    """
    try:
        seconds = isodate.parse_duration(duration).total_seconds()
        return int(seconds)
    except ISO8601Error as e:
        raise PyYouTubeException(
            ErrorMessage(
                status_code=10001,
                message=f"Exception in convert video duration: {duration}. errors: {e}",
            )
        )