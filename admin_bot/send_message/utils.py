from tele_interface.manage_data import SEND_MESSAGE


def handle_selecting_groups_to_send_message_to(ids_counter, group_ids, group_id, button_data_text, button_text):
    if group_id not in group_ids:
        text = button_text
    elif ids_counter[group_id] > 1 and ids_counter[group_id] % 2 == 0:
        text = button_text
        group_ids.remove(group_id)
        group_ids.remove(group_id)
        button_data_text = button_data_text[:len(SEND_MESSAGE)] + "|".join(group_ids)
    else:
        text = f'{button_text} ✅'

    return text, button_data_text