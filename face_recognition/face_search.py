from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
from base.log_server import LogServer
import base64
import json
import time
from base.conf_obtain import sys_config


def face_search(img_dir=False, img=False):
    """
    人脸搜索
    img_dir: 需要搜索的图片
    return: PersonId, PersonName
    """
    log = LogServer('face_search')
    start = time.time()
    if img_dir:
        with open(img_dir, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_code = base64_data.decode()
    if img:
        base64_code = img
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
        Score = Candidates['Score']  # 匹配度(官方SDK文档建议80)
        log.info(f'{PersonName}({PersonId})匹配度:{Score}% & 搜索耗时:{time.time() - start}')

        if Score < 80:
            log.info('人脸匹配度低')
            return False
        return PersonId, PersonName

    except TencentCloudSDKException as err:
        log.error(err)
        return False
