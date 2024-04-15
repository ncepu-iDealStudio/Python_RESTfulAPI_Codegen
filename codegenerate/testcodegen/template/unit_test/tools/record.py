from loguru import logger
import allure
from test.unit_test.utils.format import format_dict_to_json_output


def record_log_allure(name, data, type=allure.attachment_type.TEXT):

    log_info = f"{name}: {data}"
    logger.info(log_info)

    if isinstance(data, dict):
        data = format_dict_to_json_output(data)
        type = allure.attachment_type.JSON

    allure.attach(str(data), name=name, attachment_type=type)
