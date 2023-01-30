# NOTE: Generated By HttpRunner v4.3.0
# FROM: course1\demo1_login.yaml
from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseDemo1Login(HttpRunner):

    config = (
        Config("登录测试用例")
        .variables(**{"account": "auto", "psw": "sdfsdfsdf", "code": 0})
        .base_url("http://localhost")
        .verify(False)
        .export(*["cookie"])
    )

    teststeps = [
        Step(
            RunRequest("step1_login_request")
            .post("/api/mgr/loginReq")
            .with_data({"username": "$account", "password": "$psw"})
            .extract()
            .with_jmespath("body.retcode", "retcode")
            .with_jmespath("cookies.sessionid", "cookie")
            .validate()
            .assert_equal("$retcode", 0)
        ),
    ]


if __name__ == "__main__":
    TestCaseDemo1Login().test_start()