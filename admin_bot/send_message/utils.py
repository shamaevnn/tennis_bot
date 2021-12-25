from typing import List, Tuple, Union

from base.models import TrainingGroup, Player
from .manage_data import (
    SEND_MESSAGE,
    ALL_GROUPS,
    SEND_TO_ALL,
    SEND_TO_ARBITRARY_SCHEDULE,
)
from .static_text import (
    SENDING_TO_ALL_GROUPS_TYPE_TEXT,
    WILL_SEND_TO_ALL_TYPE_TEXT,
    WILL_SEND_TO_FREE_SCHEDULE,
    WILL_SEND_TO_THE_FOLLOWING_GROUPS,
    TYPE_TEXT_OF_MESSAGE,
)


def handle_selecting_groups_to_send_message_to(
    ids_counter, group_ids, group_id, button_data_text, button_text
):
    if group_id not in group_ids:
        text = button_text
    elif ids_counter[group_id] > 1 and ids_counter[group_id] % 2 == 0:
        text = button_text
        group_ids.remove(group_id)
        group_ids.remove(group_id)
        button_data_text = button_data_text[: len(SEND_MESSAGE)] + "|".join(group_ids)
    else:
        text = f"{button_text} ✅"

    return text, button_data_text


def get_text_and_player_ids_to_send_message_to(
    group_ids: List[Union[str, int]],
) -> Tuple[str, List]:
    list_of_group_ids = list(set([int(x) for x in group_ids if x]))
    if int(ALL_GROUPS) in list_of_group_ids:
        # pressed 'send to all groups'
        text = SENDING_TO_ALL_GROUPS_TYPE_TEXT

        banda_groups = TrainingGroup.objects.filter(
            status=TrainingGroup.STATUS_GROUP, max_players__gt=1
        ).distinct()
        player_ids = list(
            set(
                Player.objects.filter(traininggroup__in=banda_groups).values_list(
                    "tg_id", flat=True
                )
            )
        )
    elif int(SEND_TO_ALL) in list_of_group_ids:
        # pressed 'send to all'
        text = WILL_SEND_TO_ALL_TYPE_TEXT
        player_ids = list(
            set(
                Player.objects.filter(
                    status__in=[
                        Player.STATUS_TRAINING,
                        Player.STATUS_ARBITRARY,
                        Player.STATUS_IND_TRAIN,
                    ]
                ).values_list("tg_id", flat=True)
            )
        )
    elif int(SEND_TO_ARBITRARY_SCHEDULE) in list_of_group_ids:
        # pressed 'send to free view_schedule'
        text = WILL_SEND_TO_FREE_SCHEDULE
        player_ids = list(
            set(
                Player.objects.filter(status=Player.STATUS_ARBITRARY).values_list(
                    "tg_id", flat=True
                )
            )
        )
    else:
        group_names = "\n".join(
            list(
                TrainingGroup.objects.filter(id__in=list_of_group_ids).values_list(
                    "name", flat=True
                )
            )
        )
        text = f"{WILL_SEND_TO_THE_FOLLOWING_GROUPS}\n{group_names}\n{TYPE_TEXT_OF_MESSAGE}"
        player_ids = list(
            set(
                Player.objects.filter(traininggroup__in=list_of_group_ids).values_list(
                    "tg_id", flat=True
                )
            )
        )

    return text, player_ids
