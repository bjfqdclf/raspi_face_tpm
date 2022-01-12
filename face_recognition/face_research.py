from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
from base.conf_obtain import sys_config
import base64
import json
import time


def face_research(img_dir):
    start = time.time()
    with open(img_dir, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_code = base64_data.decode()
    try:
        # 实例化认证对象
        cred = credential.Credential(sys_config.SecretId, sys_config.SecretKey)
        client = iai_client.IaiClient(cred, "ap-shanghai")

        # 实例化请求对象
        req = models.SearchFacesReturnsByGroupRequest()
        req.GroupIds = ['face_system']
        req.MaxFaceNum = 1
        req.Image = base64_code
        req.NeedPersonInfo = 1  # 开启返回详细信息
        # req.NeedFaceAttributes = 1
        # req.NeedQualityDetection = 0

        # client对象调用访问接口
        resp = client.SearchFacesReturnsByGroup(req)
        resp_json = resp.to_json_string()
        resp_dic = json.loads(resp_json)
        ResultsReturnsByGroup = resp_dic['ResultsReturnsByGroup'][0]
        GroupCandidates = ResultsReturnsByGroup['GroupCandidates'][0]
        Candidates = GroupCandidates['Candidates'][0]
        PersonId = Candidates['PersonId']
        PersonName = Candidates['PersonName']
        print('id>>', PersonId)
        print('name>>', PersonName)
        print(time.time() - start)
        return PersonId, PersonName


    except TencentCloudSDKException as err:
        print(err)
        return False
