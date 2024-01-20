import base64
import json

from ytvs import proto
from ytvs.client.unofficial.parameter import DataParameterBuilder
from ytvs.client.unofficial.resources.base_resource import Resource
from ytvs.constants import MOBILE_XHR_HEADERS, CONTENT_TYPE_JSON_HEADER
from ytvs.extractor import YoutubeBasicInfoExtractor
from ytvs.utils import _search_attribute, _search_attributes, try_get


def _make_comment_ctoken(video_id, sort=0, offset=0, lc='', secret_key=''):
    """
    YouTube 댓글 페이지의 Continuation Token을 생성.
    :param video_id: 비디오 ID.
    :param sort: 댓글 정렬 방식.
    :param offset: 댓글 페이지의 오프셋.
    :param lc: 로케일 설정.
    :param secret_key: 보안 키.
    :return: 생성된 Continuation Token.
    """
    # 비디오 ID와 보안 키를 바이트로 변환
    video_id = proto.as_bytes(video_id)
    secret_key = proto.as_bytes(secret_key)

    # 페이지 정보 구성
    page_info = proto.string(4, video_id) + proto.uint(6, sort)
    offset_information = proto.nested(4, page_info) + proto.uint(5, offset)
    if secret_key:
        offset_information = proto.string(1, secret_key) + offset_information

    page_params = proto.string(2, video_id)
    if lc:
        page_params += proto.string(6, proto.percent_b64encode(proto.string(15, lc)))

    result = proto.nested(2, page_params) + proto.uint(3, 6) + proto.nested(6, offset_information)
    return base64.urlsafe_b64encode(result).decode('ascii')


class CommentThreadResource(Resource):
    KIND = 'youtube#commentThreadListResponse',# 댓글 스레드 응답 유형

    def get_comment_threads(self,
                            video_id: str,
                            sort=0,
                            offset=0,
                            lc='',
                            secret_key='',
                            page_token=None
                            ):
        """
        YouTube 비디오의 댓글 스레드를 조회.
        :param video_id: 비디오 ID.
        :param sort: 댓글 정렬 방식.
        :param offset: 댓글 페이지의 오프셋.
        :param lc: 로케일 설정.
        :param secret_key: 보안 키.
        :param page_token: 페이지 토큰.
        :return: 파싱된 댓글 스레드 데이터.
        """
        # 1. 댓글 데이터 요청
        comment_raw = self._request_data(video_id,
                                         sort,
                                         offset,
                                         lc,
                                         secret_key,
                                         page_token
                                         )

        # 2. 획득한 댓글 Raw 데이터에서 필요한 정보만 파싱
        comment = self._parse_comment_data(comment_raw)

        # 3. 추가 데이터 병합
        comment_items = comment['items']
        for comment_item in comment_items:
            comment_item['videoId'] = video_id

        # 4. 반환
        return comment

    def _request_data(self,
                      video_id: str,
                      sort=0,
                      offset=0,
                      lc='',
                      secret_key='',
                      page_token=None
                      ):
        """
        YouTube API를 통해 댓글 데이터를 요청하는 함수.
        :param video_id: 댓글을 요청할 비디오의 ID.
        :param sort: 댓글 정렬 방식.
        :param offset: 댓글 페이지의 오프셋.
        :param lc: 로케일 설정.
        :param secret_key: 보안 키.
        :param page_token: 페이지 토큰.
        :return: YouTube API로부터 받은 Raw 댓글 데이터.
        """

        if page_token is None:
            c_token = _make_comment_ctoken(video_id, sort=1 - sort, lc=lc)
        else:
            c_token = page_token
        endpoint = self.build_continuous_resource_url()
        data = json.dumps(DataParameterBuilder().set_continuation(c_token).build())

        content = self._client.fetch_url(
            endpoint, headers=MOBILE_XHR_HEADERS + CONTENT_TYPE_JSON_HEADER, data=data,
            report_text='Retrieved comments', debug_name='request_comments')
        content = content.decode('utf-8')

        raw_json = json.loads(content)
        return raw_json

    def _parse_comment_data(self, raw_data):
        """
         YouTube API로부터 받은 Raw 댓글 데이터를 파싱하는 함수.
         :param raw_data: YouTube API로부터 받은 Raw 댓글 데이터.
         :return: 파싱된 댓글 데이터.
         """
        # 댓글 Header 정보 획득
        header_renderer = _search_attribute(raw_data, 'commentsHeaderRenderer', max_depth=10)
        header = YoutubeBasicInfoExtractor.extract_comments_headerer_renderer(header_renderer)

        # 댓글 본문 정보 획득
        comments = []
        comment_thread_renderers = _search_attributes(raw_data, 'commentThreadRenderer')
        if comment_thread_renderers is None:
            total_comment = 0
            continuation_token = None
        else:
            total_comment = len(comment_thread_renderers)

            for comment_thread_renderer in comment_thread_renderers:
                # Comment thread
                comment_renderer_raw = try_get(comment_thread_renderer, lambda x: x['comment']['commentRenderer'], dict)
                comment = YoutubeBasicInfoExtractor.extract_comment_renderer(comment_renderer_raw)
                # Comment replies
                comment_replies_renderer_raw = try_get(comment_thread_renderer,
                                                       lambda x: x['replies']['commentRepliesRenderer'], dict)
                comment_replies = YoutubeBasicInfoExtractor.extract_comment_replies_renderer(comment_replies_renderer_raw)
                comment['replies'] = comment_replies
                # comment['videoId'] = video_id
                comments.append(comment)

            # 댓글 페이징 정보 획득
            comment_continuation_renderer = _search_attributes(raw_data, 'continuationItemRenderer')
            comment_continuation = YoutubeBasicInfoExtractor.extract_continuation_item_renderer(
                comment_continuation_renderer['continuationEndpoint'])
            continuation_token = try_get(comment_continuation, lambda x: x['continuation_command']['token'], str)

        return {
            'kind': self.KIND,
            'etag': None,
            'items': comments,
            'nextPageToken': continuation_token,
            'pageInfo': {
                'resultsPerPage': 20,
                'totalResults': total_comment,
            },
            'prevPageToken': None
        }
