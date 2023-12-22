from sqlalchemy import Column, DateTime, Index, String, Text, text, Sequence
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Post(Base):
    __tablename__ = 'posts_added'

    id = Column(BIGINT(20), Sequence('id_seq'), primary_key=True)
    kw_post_id = Column(String(50), unique=True)
    wp_post_id = Column(BIGINT(20), unique=True)

class WpPostmeta(Base):
    __tablename__ = 'wp_postmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    post_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("0"))
    meta_key = Column(String(255), index=True)
    meta_value = Column(LONGTEXT)


class WpPost(Base):
    __tablename__ = 'wp_posts'
    __table_args__ = (
        Index('type_status_date', 'post_type', 'post_status', 'post_date', 'ID'),
    )

    ID = Column(BIGINT(20), primary_key=True)
    post_author = Column(BIGINT(20), nullable=False, index=True, server_default=text("0"))
    post_date = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_date_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_content = Column(LONGTEXT, nullable=False)
    post_title = Column(Text, nullable=False)
    post_excerpt = Column(Text, nullable=False)
    post_status = Column(String(20), nullable=False, server_default=text("'publish'"))
    comment_status = Column(String(20), nullable=False, server_default=text("'open'"))
    ping_status = Column(String(20), nullable=False, server_default=text("'open'"))
    post_password = Column(String(255), nullable=False, server_default=text("''"))
    post_name = Column(String(200), nullable=False, index=True, server_default=text("''"))
    to_ping = Column(Text, nullable=False)
    pinged = Column(Text, nullable=False)
    post_modified = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_modified_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_content_filtered = Column(LONGTEXT, nullable=False)
    post_parent = Column(BIGINT(20), nullable=False, index=True, server_default=text("0"))
    guid = Column(String(255), nullable=False, server_default=text("''"))
    menu_order = Column(INTEGER(11), nullable=False, server_default=text("0"))
    post_type = Column(String(20), nullable=False, server_default=text("'post'"))
    post_mime_type = Column(String(100), nullable=False, server_default=text("''"))
    comment_count = Column(BIGINT(20), nullable=False, server_default=text("0"))


class WpTermRelationship(Base):
    __tablename__ = 'wp_term_relationships'

    object_id = Column(BIGINT(20), primary_key=True, nullable=False, server_default=text("0"))
    term_taxonomy_id = Column(BIGINT(20), primary_key=True, nullable=False, index=True, server_default=text("0"))
    term_order = Column(INTEGER(11), nullable=False, server_default=text("0"))


class WpTermTaxonomy(Base):
    __tablename__ = 'wp_term_taxonomy'
    __table_args__ = (
        Index('term_id_taxonomy', 'term_id', 'taxonomy', unique=True),
    )

    term_taxonomy_id = Column(BIGINT(20), primary_key=True)
    term_id = Column(BIGINT(20), nullable=False, server_default=text("0"))
    taxonomy = Column(String(32), nullable=False, index=True, server_default=text("''"))
    description = Column(LONGTEXT, nullable=False)
    parent = Column(BIGINT(20), nullable=False, server_default=text("0"))
    count = Column(BIGINT(20), nullable=False, server_default=text("0"))


class WpTerm(Base):
    __tablename__ = 'wp_terms'

    term_id = Column(BIGINT(20), primary_key=True)
    name = Column(String(200), nullable=False, index=True, server_default=text("''"))
    slug = Column(String(200), nullable=False, index=True, server_default=text("''"))
    term_group = Column(BIGINT(10), nullable=False, server_default=text("0"))