from ihc_attribution_api_request import post_compute_ihc
from load_to_attribution_customer_journey import insert_data_to_attribution_customer_journey
from load_to_channel_reporting import fill_channel_reporting_table
from extract_customer_journey import get_customer_journeys


def process():
    # Extract
    customer_journeys = get_customer_journeys()
    # Transform
    for conv_id, journey in customer_journeys.items():
        transformed_data = post_compute_ihc(conv_id, journey)
        print(transformed_data)
        if transformed_data:
            for item in transformed_data:
                insert_data_to_attribution_customer_journey(item["conversion_id"], item["session_id"] ,item["ihc"])

    # Load
    fill_channel_reporting_table()


if __name__ == '__main__':
    process()
