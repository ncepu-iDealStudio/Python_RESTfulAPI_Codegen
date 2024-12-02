import importlib

from loguru import logger
from manage import app

from test.unit_test.tools.format import center_text
from test.unit_test.tools.record import record_log_allure


class FunctionTestUtil:

    @classmethod
    def test_body(cls, case_info):
        case_name = case_info['case_name']
        module_name = case_info['module_name']
        class_name = case_info['class_name']
        funtion_name = case_info['funtion_name']
        params = case_info.get('params', {})
        validate = case_info['validate']

        module = importlib.import_module("service." + module_name)
        class_object = module.__getattribute__(class_name)

        # 日志输出测试信息
        start_line = center_text(f"方法service::{module_name}::{class_name}::{funtion_name}测试开始")
        case_name_line = center_text(case_name, fill_char=' ')
        end_line = center_text(f"方法service::{module_name}::{class_name}::{funtion_name}测试通过")
        # 在测试用例开始之前输出
        logger.info(f'\n{start_line}')
        logger.info(f'\n{case_name_line}')

        with app.app_context():
            response_data = getattr(class_object, funtion_name)(**params)

            for name, data in {
                "case_info": case_info,
                "调用方法": f"{class_name}.{funtion_name}",
                "请求参数": params,
                "返回结果": response_data,
            }.items():
                record_log_allure(name, data)

            # 断言
            for eq_k, eq_v in validate['eq'].items():
                assert_result = "成功" if response_data.get(eq_k) == eq_v else "失败"
                record_log_allure(
                    name=f"{eq_k} 断言{assert_result}",
                    data={"expect": eq_v, "actual": response_data.get(eq_k)}
                )
                assert response_data.get(eq_k) == eq_v

        # 在测试用例结束之后输出
        logger.info(f'\n{end_line}\n')
