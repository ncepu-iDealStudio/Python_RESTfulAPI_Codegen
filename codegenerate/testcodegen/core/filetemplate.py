#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time:2021/10/4 18:52
# Author:yuanronghao
# @File:filetemplate.py
# @Software:PyCharm

class FileTemplate(object):
    """
    init_: template for Test_Controller/init.py,Test_Resource/init.py,
    test_init_:template for test/init.py
    pytest_ini：template for test/pytest.ini
    Test_xController/init.py, Test_xResource/init.py
    controller_datas_:template for Test_xController/datas.py
    resource_datas_:template for Test_xResource/datas.py
    test_controller_: template for Test_xController/test_xController.py
    test_resource_: template for Test_xResource/test_xResource.py

    """

    init = """#!/usr/bin/env python
# -*- coding:utf-8 -*-
    """

    env = "base_url=https://{project_name}"

    test_service = """#!/usr/bin/env python
    # -*- coding:utf-8 -*-

    import os
    import pytest

    from test.common.function_test_util import FunctionTestUtil
    from test.utils.read_yaml import read_yaml

    base_url = os.path.dirname(os.path.abspath(__file__))


    class Test{table_name}Service:
        @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_url, "data.yaml")))
        def test_sub_count(self, caseInfo):
            FunctionTestUtil.test_body(caseInfo)
        """

    test_resource = """import os

    import pytest

    from test.common.request_util import RequestUtil
    from test.utils.read_yaml import read_yaml

    base_dir = os.path.dirname(os.path.abspath(__file__))


    class Test{table_name}Resource:

        @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/get.yaml")))
        def test_get(self, caseInfo, env_dict):
            RequestUtil.test_body(caseInfo, env_dict)

        @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/post.yaml")))
        def test_post(self, caseInfo, env_dict):
            RequestUtil.test_body(caseInfo, env_dict)

        @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/put.yaml")))
        def test_update(self, caseInfo, env_dict):
            RequestUtil.test_body(caseInfo, env_dict)

        @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/delete.yaml")))
        def test_delete(self, caseInfo, env_dict):
            RequestUtil.test_body(caseInfo, env_dict)
        """