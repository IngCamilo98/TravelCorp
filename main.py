import json
import time
from datetime import date

from dotenv import load_dotenv

from config.constants import CITIES
from config.settings import execution_sleep_time
from etl.load import create_list_load_data_cities

load_dotenv()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def execute_etl():
    try:
        data_final = create_list_load_data_cities(CITIES)
        output_path = "output.json"
        try:
            with open(output_path, "r", encoding="utf-8") as infile:
                existing_data = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []
        if not isinstance(existing_data, list):
            existing_data = [existing_data]
        existing_data.append(data_final)
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(existing_data, outfile, indent=4, ensure_ascii=False, cls=DateTimeEncoder)
    except Exception as e:
        print(f"Error executing ETL process: {e}")
        raise e


if __name__ == "__main__":
    while True:
        execute_etl()
        print(f"Waiting for {execution_sleep_time} seconds before the next execution...")
        time.sleep(execution_sleep_time)
