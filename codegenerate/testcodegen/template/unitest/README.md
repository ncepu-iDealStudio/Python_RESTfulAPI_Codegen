yaml测试用例约定
* 接口自动化测试YAML测试用例约定：
  * 一级关键字必须包含：name,request,validate
  * 在request下必须包含：method,url
  * 传参方式：
    * get请求：必须通过params传参
    * post请求：
        传json格式，需要使用json传参
        传表单格式，需要使用data传参
    
* 函数（方法）自动化测试YAML测试用例约定：
  * 一级关键字必须包含：module_name、class_name、funtion_name、validate