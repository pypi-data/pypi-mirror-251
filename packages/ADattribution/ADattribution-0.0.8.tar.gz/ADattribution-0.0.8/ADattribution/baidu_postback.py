from lazysdk import lazyrequests


def postback(
        token: str,
        bd_vid: str,
        new_type_list: list,
        convert_time: int = None,
        convert_value: int = None,

        deviceType=None,
        deviceId=None,
        isConvert=None,
        confidence=None,
        ext_info=None,
        theaterId=None,
        theaterShortPlayId=None,
        theaterUserId=None
):
    """
    百度回传
    :param token:
    :param bd_vid:
    :param new_type_list:
    :param convert_time: unix时间戳（精确到秒）;选填，转化类型为45、46、47、48时必填
    :param convert_value: 转化金额（单位分）;选填，回传具体商品金额有助于提升模型优化准确性（数值需大于0）
    :param confidence: 置信度，0-100数字
    参考文档：https://dev2.baidu.com/content?sceneType=0&pageId=101211&nodeId=658
    """
    post_types = list()
    for each in new_type_list:
        each_data = {
            'logidUrl': f'https://open.fanshang888.com/api/cache/receive/open_api/ad/baidu/track?&bd_vid={bd_vid}',
            'newType': each
        }
        if convert_time:
            each_data['convertTime'] = convert_time
        if convert_value:
            each_data['convertValue'] = convert_value

        if deviceType:
            each_data['deviceType'] = deviceType
        if deviceId:
            each_data['deviceId'] = deviceId
        if isConvert:
            each_data['isConvert'] = isConvert
        if confidence:
            each_data['confidence'] = confidence
        if ext_info:
            each_data['ext_info'] = ext_info
        if theaterId:
            each_data['theaterId'] = theaterId
        if theaterShortPlayId:
            each_data['theaterShortPlayId'] = theaterShortPlayId
        if theaterUserId:
            each_data['theaterUserId'] = theaterUserId

        post_types.append(
            each_data
        )
    url = 'https://ocpc.baidu.com/ocpcapi/api/uploadConvertData'
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json={
            'token': token,
            'conversionTypes': post_types
        },
        return_json=True,
        timeout=5
    )
