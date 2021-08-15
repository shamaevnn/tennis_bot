import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def have_not_paid_users_info(payments_values):
    return '\n'.join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['n_fact_visiting']} ({x['group_name']})"
            for x in payments_values
        )
    )