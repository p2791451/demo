import sys
import requests
import subprocess
import stbt_rig
import argparse
import os
import threading


class JenkinsJob(object):
    def __init__(self):
        print("Inside jenkins main")
        self.project = sys.argv[1]
        self.module = sys.argv[2]
        self.node = sys.argv[3]

        self.node_id = self.get_node_id(self.node)
        self.test_suite_path = self.build_test_suite_path(self.project, self.module)
        self.test_pack_rev = self.get_text_pack_revision()
        self.test_suite = self.get_list_of_all_test_cases(self.test_suite_path, self.test_pack_rev)

        self.node_cmd = "--node-id={}".format(self.node_id)
        self.test_pack_revision = "--test-pack-revision={}".format(self.test_pack_rev)
        self.cmd = ["hi", self.node_cmd, "run"]
        self.cmd.extend(self.test_suite)
        #self.cmd.append("--force")
        self.cmd.append(self.test_pack_revision)
        stbt_rig.main(self.cmd)

    def build_test_suite_path(self, project, module):
        """
        author: Prasad Hegde
        description: Builds the path of the test suite by concatenating project and
        module to "tests"
        :param project: AppleTv / Roku / SpectrumGuide
        :param module: SanitySuite / RegressionSuite / RepetetionSuite /
        RegressionSuite/.{DVR,VOD,cGuide,Search,LiveTv}
        :return: test_suite_path
        """
        test_suite_path = "tests/"+project+"/"+module
        return test_suite_path

    def get_node_id(self, node):
        """
        author: Prasad Hegde
        description: Returns node id for the nodes
        :param node: Master, Samus
        :return: node id
        """
        node_dict = {'MasterHand':'00044b80f5f9',
                     'Samus':'00044b80f7f2',
                     'Fox':'00044b80f654',
                     'Kirby':'00044b80f745',
                     'Mewtwo':'00044b80f7de',
                     'Falco':'00044b80f7e0'
                     }

        return "stb-tester-"+node_dict.get(node, "empty")

    def get_text_pack_revision(self):
        """
        author: Prasad Hegde
        description: Returns the latest revision pack id of the current branch
        :return: revision id
        """
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

    def get_list_of_all_test_cases(self, test_suite_path, test_pack_rev):
        """
        author: Prasad Hegde
        description: GETS the list of all test scripts in the current branch
        and the filters only those scripts which come under "test_suite_path"
        :param test_suite_path:
        :return: test_suite
        """
        #Need to accept token value from jenkins
        tests = requests.get(
            "https://charter.stb-tester.com/api/v2/test_pack/%s/test_case_names" % test_pack_rev,
            headers={"Authorization": "token jhOcOnVcmdGcdXQhdhLjkC6rcqKBR-bU"}
            )
        if tests.status_code == 200:
            print("Status is : ",tests.status_code  )
            test_suite=[]
            for test in tests.json():
                if test.startswith(test_suite_path):
                    test_suite.append(test)
            return test_suite
        print("Exception occurred while making a GET request to retrieve Test "
              "Scripts with status code: "+ str(tests.status_code))
        sys.exit(-1)


if __name__ == "__main__":
    print("Before creating object")
    obj = JenkinsJob()
    print("after creating obj")
    #obj.my_main()
    print("after calling jenkins main")