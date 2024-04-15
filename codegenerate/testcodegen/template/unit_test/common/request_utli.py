import requests
from loguru import logger
from requests.exceptions import RequestException

from test.unit_test.tools.format import center_text
from test.unit_test.tools.check import check_url
from test.unit_test.tools.record import record_log_allure


class RequestUtil:
    # 初始化一个session对象
    session = requests.session()

    @classmethod
    def send_request(cls, method, url, headers=None, data=None):
        """ 发送请求并返回响应对象 """
        method = method.lower()  # 方法统一转换为小写
        try:
            if method == 'get':
                response = cls.session.get(url=url, headers=headers, params=data)
            elif method in ['post', 'put', 'delete']:
                response = cls.session.request(method, url=url, headers=headers, data=data)
            else:
                logger.exception(f"未知的请求方法: {method}")
                raise ValueError(f"未知的请求方法: {method}")
            return response
        except RequestException as e:
            logger.exception(f"请求过程出现异常: {e}")
            raise RequestException

    @classmethod
    def test_body(cls, case_info, env_dict):
        """ 进行接口测试并进行断言 """
        api_name = case_info.get("api_name")
        case_name = case_info['case_name']
        request_info = case_info['request']
        method = request_info['method']
        headers = request_info.get('headers', {})

        data_key = 'params' if method.lower() == 'get' else 'data'
        data = case_info.get(data_key, {})

        try:
            url = env_dict['base_url'] + request_info['url']
            check_url(url)
            if method.lower() in ['put', 'delete']:
                url = url + '/' + str(data.pop('id'))
        except Exception as e:
            logger.exception(e)

        validate = case_info['validate']

        # 设置Token
        headers.setdefault('token', env_dict.get('token'))

        # 日志输出测试信息
        start_line = center_text(f"开始测试: {api_name}")
        case_name_line = center_text(case_name, fill_char=' ')
        end_line = center_text(f"测试接口 '{api_name}' 通过")
        # 在测试用例开始之前输出
        logger.info(f"\n\n{start_line}")
        logger.info(f'\n{case_name_line}')

        # 发送请求并获取响应数据
        try:
            response = cls.send_request(method, url, headers, data)
            response_data = response.json()
        except ValueError as e:
            logger.exception("响应数据不是有效的JSON格式")
            raise ValueError("响应数据不是有效的JSON格式")

        for name, data in {
            "env_dict": env_dict,
            "case_info": case_info,
            "请求URL": url,
            "请求方法": method.upper(),
            "请求头部": headers,
            "请求数据": data,
            "响应头部": dict(response.headers),
            "响应数据": response_data
        }.items():
            record_log_allure(name, data)

        # 断言内容
        for eq_k, eq_v in validate['eq'].items():
            if eq_k == 'status_code':
                assert_result = "成功" if response.status_code == eq_v else "失败"
                record_log_allure(
                    name=f"{eq_k} 断言{assert_result}",
                    data={"expect": eq_v, "actual": response.status_code}
                )
                assert response.status_code == eq_v
            else:
                assert_result = "成功" if response_data.get(eq_k) == eq_v else "失败"
                record_log_allure(
                    name=f"{eq_k} 断言{assert_result}",
                    data={"expect": eq_v, "actual": response_data.get(eq_k)}
                )
                assert response_data.get(eq_k) == eq_v

        # 在测试用例结束之后输出
        logger.info(f"\n{end_line}")
