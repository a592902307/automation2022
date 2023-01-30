# NOTE: Generated By HttpRunner v4.3.0
# FROM: .\course2\demo2_updatecourse.yaml
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import RunTestCase

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from course2.demo1_addcourse_test import TestCaseDemo1Addcourse as Demo1Addcourse


class TestCaseDemo2Updatecourse(HttpRunner):

    config = Config("更新课程").base_url("http://localhost").verify(False)

    teststeps = [
        Step(
            RunTestCase("addcourse")
            .call(Demo1Addcourse)
            .export(*["course_id", "cookie"])
        ),
        Step(
            RunRequest("updatecourse")
            .with_variables(**{"name": "python基础", "desc": "python基础课程", "idx": 10})
            .put("/api/mgr/sq_mgr/")
            .with_headers(**{"Content-Type": "application/x-www-form-urlencoded"})
            .with_cookies(**{"sessionid": "$cookie"})
            .with_data(
                {
                    "action": "modify_course",
                    "id": "$course_id",
                    "newdata": '{"name":"${name}","desc":"${desc}", "display_idx":"${idx}"}',
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.retcode", 0)
        ),
    ]


if __name__ == "__main__":
    TestCaseDemo2Updatecourse().test_start()