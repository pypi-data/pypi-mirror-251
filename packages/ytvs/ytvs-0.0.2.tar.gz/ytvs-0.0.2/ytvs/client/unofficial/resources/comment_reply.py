import base64
import json

from ytvs import proto
from ytvs.client.unofficial.resources.base_resource import Resource
from ytvs.constants import MOBILE_XHR_HEADERS, CONTENT_TYPE_JSON_HEADER


class CommentResource(Resource):
    def get_comments(self, page_token,  # Unofficial 방법으로는 미지원
                     ):
        c_token = page_token
        # Caption
        API_KEY = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
        request_url = f'{BASE_URL}?key={API_KEY}'
        data = json.dumps({
            'context': {
                'client': {
                    'hl': 'ko',  # en
                    'gl': 'KR',  # US
                    'clientName': 'WEB',  # MWEB
                    'clientVersion': '2.20210804.02.00',
                },
            },
            'params': c_token.replace('=', '%3D'),
        })
        endpoint = f'{self.CONTINUATION_URL}'
        content = self._client.fetch_url(
            request_url, headers=MOBILE_XHR_HEADERS + CONTENT_TYPE_JSON_HEADER, data=data,
            report_text='Retrieved comments', debug_name='request_comments')
        content = content.decode('utf-8')

        raw_data = json.loads(content)

    def _make_comment_ctoken(self, video_id, sort=0, offset=0, lc='', secret_key=''):
        video_id = proto.as_bytes(video_id)
        secret_key = proto.as_bytes(secret_key)

        page_info = proto.string(4, video_id) + proto.uint(6, sort)
        offset_information = proto.nested(4, page_info) + proto.uint(5, offset)
        if secret_key:
            offset_information = proto.string(1, secret_key) + offset_information

        page_params = proto.string(2, video_id)
        if lc:
            page_params += proto.string(6, proto.percent_b64encode(proto.string(15, lc)))

        result = proto.nested(2, page_params) + proto.uint(3, 6) + proto.nested(6, offset_information)
        return base64.urlsafe_b64encode(result).decode('ascii')
