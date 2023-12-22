from db import create_session, close_session
from models import *

session = create_session()
result = session.query(WpPost).filter(WpPost.ID==23010).all()
for r in result:
    print(r.post_title)
# result = session.query(Post).filter(Post.kw_post_id == 'hh4h4').all()
# if len(result):
#     post = result.pop()
#     print(post.kw_post_id)

close_session(session)