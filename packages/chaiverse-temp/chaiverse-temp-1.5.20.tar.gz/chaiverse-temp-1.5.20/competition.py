import requests

from chaiverse.utils import get_url


COMPETITIONS_ENDPOINT = '/competitions'


COMPETITION_TYPE_CONFIGURATION = {}

COMPETITION_TYPE_CONFIGURATION['default'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'submission_id',
        'is_custom_reward',
        'stay_in_character',
        'user_preference',
        'entertaining',
        'overall_rank',
        'repetition',
        'safety_score',
        'thumbs_up_ratio',
        'total_feedback_count',
        'model_parameter_size',
        'status'
    ],
    "sort_column": "overall_score"
}

COMPETITION_TYPE_CONFIGURATION['submission_closed_feedback_round_robin'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'thumbs_up_ratio',
        'overall_rank',
        'total_feedback_count',
        'repetition',
        'stay_in_character',
        'user_preference',
        'entertaining',
        'safety_score',
        'is_custom_reward',
        'submission_id',
        'model_parameter_size',
    ],
    "sort_column": "thumbs_up_ratio",
}


def get_competitions():
    url = get_url(COMPETITIONS_ENDPOINT)
    response = requests.get(url)
    assert response.ok, response.json()
    return response.json()

