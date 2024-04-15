import os

import allure
import pytest

from test.unit_test.common.decorators import allure_decorate
from test.unit_test.common.request_utli import RequestUtil
from test.unit_test.utils.read_yaml import read_yaml

base_dir = os.path.dirname(os.path.abspath(__file__))


# @pytest.mark.skipif(
#     "not config.getoption('--version-test')",
#     reason="No API version provided"
# )

@allure.feature('API版本接口')
class TestApiVersionResource:

    @allure_decorate("获取API版本")
    @pytest.mark.version
    @pytest.mark.parametrize("case_info", read_yaml(os.path.join(base_dir, "data/get.yaml")))
    def test_get(self, case_info, env_dict):
        RequestUtil.test_body(case_info, env_dict)
