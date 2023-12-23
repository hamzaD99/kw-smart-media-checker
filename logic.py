from db import create_session
from models import *
import logging
from urllib.parse import quote
from datetime import datetime
logger = logging.getLogger(__name__)

def create_wp_post(property_id, wp_session, post_data = {}):
    from constants import default_post_data
    final_post_data = default_post_data
    final_post_data.update(post_data)
    try:
        post_to_add = WpPost(final_post_data)
        wp_session.add(post_to_add)
        wp_session.commit()
        wordpress_id = post_to_add.ID
        logger.info(f'Property {property_id} post added, wordpressId =  {wordpress_id}')
    except Exception as e:
        logger.error(f'Property {property_id} Error adding post to WpPost: {e}', exc_info=True)
        return False
    return wordpress_id


def add_post_meta(wp_session, wordpress_id, property_id, meta_data = {}):
    from constants import default_meta_data
    final_meta_data = {item["meta_key"]: item["meta_value"] for item in default_meta_data}
    final_meta_data.update(meta_data)
    try:
        for meta_key in final_meta_data.keys():
            row_to_add = WpPostmeta(meta_key=meta_key, meta_value=final_meta_data[meta_key], post_id=wordpress_id)
            wp_session.add(row_to_add)
        wp_session.commit()
    except Exception as e:
        logger.error(f'Property {property_id}, WpPost Id {wordpress_id} Error adding post to WpPostmeta: {e}', exc_info=True)
        return False
    logger.info(f'Property {property_id} with post ID {wordpress_id}, meta data added ({len(final_meta_data.keys())} keys)')
    return True

def add_term(wp_session, term, taxomony, parent=None):
    try:
        term_to_add = WpTerm(name=term,slug=quote(term.lower(), safe='/:.-_'),term_group=0)
        wp_session.add(term_to_add)
        wp_session.commit()
        parentId = 0
        if(parent):
            parent_object = wp_session.query(WpTerm).filter(WpTerm.name == parent).first()
            if not parent_object:
                logging.error(f'Term {term}: parent {parent} not found')
            else:
                parentId = parent_object.term_id
        tax = WpTermTaxonomy(term_id = term_to_add.term_id, taxonomy=taxomony,description=f'ADDED BY BOT RUN @ {datetime.now().strftime("%y%m%d-%H%M")}',parent = parentId,count=0)
        wp_session.add(tax)
        wp_session.commit()
    except Exception as e:
        logger.error(f'Term {term} Error adding to WpTerm: {e}', exc_info=True)
        return False
    return term_to_add

def add_post_term(wp_session, wordpress_id, property_id, terms):
    terms_added = []
    terms_not_found = []
    try:
        for term in terms:
            taxonomy = term.get('taxonomy')
            parent = term.get('parent', 0)
            term = term['name']
            term = term.strip()
            term_from_db = wp_session.query(WpTerm).filter(WpTerm.name == term).first()
            if(not term_from_db):
                logger.error(f'Property {property_id}, WpPost Id {wordpress_id} Error adding term to WpTermRelationship: term {term} not found')
                terms_not_found.append(term)
                if(not taxonomy):
                    logger.error(f'Property {property_id}, WpPost Id {wordpress_id} Error adding term to WpTermRelationship: term {term} has no taxonomy')
                    continue
                term_from_db = add_term(wp_session=wp_session,term=term,taxomony=taxonomy,parent=parent)
                if not term_from_db:
                    continue
            term_to_add = WpTermRelationship(object_id = wordpress_id, term_taxonomy_id=term_from_db.term_id, term_order=0)
            wp_session.add(term_to_add)
            tax_record = wp_session.query(WpTermTaxonomy).filter(WpTermTaxonomy.term_id == term_from_db.term_id).first()
            if tax_record:
                tax_record.count += 1
            else:
                print(f"HAMZA {term_from_db.term_id}")
            terms_added.append(term)
            wp_session.commit()
    except Exception as e:
        logger.error(f'Property {property_id}, WpPost Id {wordpress_id} Error adding post to WpTerm: {e}', exc_info=True)
        return False
    logger.info(f'Property {property_id} with post ID {wordpress_id}, terms added ({len(terms_added)} terms) ({len(terms_not_found)} terms not found)')
    if(len(terms_not_found)):
        logger.error(f'Terms not found = {terms_not_found}')
    return True

def create_post(property_id, data = {}):
    main_data = data.get('main', {})
    meta_data = data.get('meta', {})
    terms_data = data.get('terms', [])
    wp_session = create_session()
    wordpress_id = create_wp_post(property_id=property_id,wp_session=wp_session,post_data=main_data)
    if not wordpress_id:
        wp_session.close()
        return False
    meta_res = add_post_meta(wp_session=wp_session,wordpress_id=wordpress_id,property_id=property_id,meta_data=meta_data)
    if not meta_res:
        wp_session.close()
        delete_post(wordpress_id=wordpress_id, level=1)
        return False
    term_res = add_post_term(wp_session=wp_session,wordpress_id=wordpress_id,property_id=property_id,terms=terms_data)
    if not term_res:
        wp_session.close()
        delete_post(wordpress_id=wordpress_id)
        return False
    wp_session.close()
    # inner_session = create_session(inner=True)
    # try:
    #     post_to_add = InnerPost(kw_post_id=property_id,wp_post_id=wordpress_id)
    #     inner_session.add(post_to_add)
    #     inner_session.commit()
    # except Exception as e:
    #     logger.error(f'Property {property_id}, WpPost Id {wordpress_id} Error adding post to innerDB: {e}', exc_info=True)
    #     return False
    # inner_session.close()
    return wordpress_id

def delete_post(wordpress_id, level = 3):
    wp_session = create_session()
    post_to_delete = wp_session.query(WpPost).filter(WpPost.ID == wordpress_id).first()
    wp_session.delete(post_to_delete)
    try:
        wp_session.commit()
    except Exception as e:
        logger.error(f'WpPost Id {wordpress_id} Error deleting WpPost: {e}', exc_info=True)
        wp_session.close()
        return False
    if level == 1:
        logger.info(f'post ID {wordpress_id} deleted successfully, level = {level}')
        wp_session.close()
        return True
    meta_to_delete = wp_session.query(WpPostmeta).filter(WpPostmeta.post_id == wordpress_id).all()
    try:
        for meta in meta_to_delete:
            wp_session.delete(meta)
        wp_session.commit()
    except Exception as e:
        logger.error(f'WpPost Id {wordpress_id} Error deleting WpPostmeta: {e}', exc_info=True)
        wp_session.close()
        return False
    if level == 2:
        logger.info(f'post ID {wordpress_id} deleted successfully, level = {level}')
        wp_session.close()
        return True
    terms_to_delete = wp_session.query(WpTermRelationship).filter(WpTermRelationship.object_id == wordpress_id).all()
    try:
        for term in terms_to_delete:
            wp_session.delete(term)
            tax_res = wp_session.query(WpTermTaxonomy).filter(WpTermTaxonomy.term_id == term.term_taxonomy_id).first()
            if(tax_res):
                tax_res.count -= 1
            else: print(term.term_taxonomy_id)
        wp_session.commit()
    except Exception as e:
        logger.error(f'WpPost Id {wordpress_id} Error deleting WpTermRelationship: {e}', exc_info=True)
        wp_session.close()
        return False
    logger.info(f'post ID {wordpress_id} deleted successfully, level = {level}')
    wp_session.close()
    return True
