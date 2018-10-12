import json
import os
import time

import requests

'''
择取抖音点赞转发评论
下载视频到本地
'''


class dy_spider(object):

    def __init__(self):
        self.offset = 20
        self.count = 0
        self.max_cursor = 0
        self.base_list_url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/?max_cursor=0&user_id=95870186531&count=20&retry_type=no_retry&iid=45914405819&device_id=49656204420&ac=wifi&channel=smartisan&aid=1128&app_name=aweme&version_code=280&version_name=2.8.0&device_platform=android&ssmix=a&device_type=OS105&device_brand=SMARTISAN&language=zh&os_api=25&os_version=7.1.1&uuid=86634103643612&openudid=719e70e67c27c04a&manifest_version_code=280&resolution=1080*2070&dpi=400&update_version_code=2802&_rticket=1539326806688&ts=1539326806&as=a1b5542c26c5eb23004355&cp=4057be5d6803c23ce1%5DiKm&mas=01ca9ce34e1f7657bfee91fce8ac116ed6acaccc2c0c0ccc4c46a6'
        self.base_list_header = {
            'Host': 'aweme.snssdk.com',
            'Accept': '*/*',
            'Cookie': 'ga=GA1.2.194291978.1522333705; install_id=34233874841; login_flag=041bbf59128b260bce59a9c402c9a785; odin_tt=36734d313959427872477169434b6859060425c58463c5cf68e0c79dfd2b74c22a853ee56a796f7f29f971bba6ec6eb6; sessionid=5d9862f2c07aff3598f4451964f8b760; sid_guard=5d9862f2c07aff3598f4451964f8b760%7C1528455199%7C2592000%7CSun%2C+08-Jul-2018+10%3A53%3A19+GMT; sid_tt=5d9862f2c07aff3598f4451964f8b760; ttreq=1$bc9903bdf5301842ea8647dbaceba38fc01976de; uid_tt=7bd5b67e75b5d06eba3af36bc3658f04',
            'User-Agent': 'Aweme/1.8.5 (iPhone; iOS 11.4; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, en-US;q=0.8',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive',
        }

    def request_list_data(self):
        response = requests.get(self.base_list_url, headers=self.base_list_header)
        if 200 == response.status_code:
            self.parse_list_data(response.text)

    def parse_list_data(self, response_data):
        all_datas = json.loads(response_data)
        # print(all_datas)
        all_lists = all_datas['aweme_list']
        for list in all_lists:
            comment_count = list['statistics']['comment_count']
            share_count = list['statistics']['share_count']
            digg_count = list['statistics']['digg_count']
            nickname = list['author']['nickname']
            desc = list['desc']
            play_url = list['video']['play_addr']['url_list'][0]
            self.down_load_video(play_url, desc)
            print('昵称：{}'.format(nickname), '详情：{}'.format(desc), '评论数：{}'.format(comment_count),
                  '评论数：{}'.format(share_count), '点赞数：{}'.format(digg_count), play_url)

    def down_load_video(self, url, desc):
        path = 'F:\PythonProject\\appium_project\douyin\download\{}.mp4'.format(desc)
        print(path)
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(requests.get(url).content)
                time.sleep(2)


if __name__ == '__main__':
    d = dy_spider()
    d.request_list_data()