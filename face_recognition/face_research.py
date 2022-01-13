from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
import base64
import json
import time


def face_research(img_dir):
    """
    人脸搜索
    img_dir: 需要搜索的图片
    return: PersonId, PersonName
    """
    start = time.time()
    # img_dir = 'C:/Users/bjfqdclf/OneDrive/专属文件夹/学习/毕业设计\program/opencv_demo/img/1.name.jpg'
    with open(img_dir, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_code = base64_data.decode()
    try:
        # 实例化认证对象
        cred = credential.Credential("AKIDylIYXFgqiKeiV1GFwMVMxGI2WjfKjriI", "KOAfspVt0rRkmX2FBqEK9hzzjBMIejX3")
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
        print('id>>', PersonId)
        print('name>>', PersonName)
        print('本次搜索用时>>', time.time() - start)
        if Score < 80:
            print('人脸匹配度低')
            return False
        return PersonId, PersonName

    except TencentCloudSDKException as err:
        print(err)
        return False
