"""사용자가 작성한 HTML(Quill 에디터 출력)에서 위험한 태그와 속성을 제거한다."""
import nh3

# Quill 'snow' 테마 기본 툴바가 만들어내는 태그만 허용
ALLOWED_TAGS = {
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's',
    'a', 'ol', 'ul', 'li', 'h1', 'h2', 'h3',
    'blockquote', 'pre', 'code', 'span',
}
ALLOWED_ATTRIBUTES = {
    '*': {'class'},        # ql-align-center, ql-indent-1 등 Quill 서식 클래스
    'a': {'href', 'target'},
}


def clean_html(value):
    if not value:
        return value
    return nh3.clean(
        str(value),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes={'http', 'https', 'mailto'},
        link_rel='noopener noreferrer nofollow',
    )
