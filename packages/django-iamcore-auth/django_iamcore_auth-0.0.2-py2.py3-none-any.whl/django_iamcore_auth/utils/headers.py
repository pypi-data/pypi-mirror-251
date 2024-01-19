import logging

from django.http.request import HttpHeaders

logger = logging.getLogger(__name__)


def get_auth_headers(headers: HttpHeaders):
    if isinstance(headers, HttpHeaders):
        return {
            'X-iamcore-API-Key': headers.get('X-iamcore-API-Key'),
            'Authorization': headers.get('Authorization')
        }
    if isinstance(headers, dict):
        return {
            k: v
            for k, v in headers.items()
            if k.lower() in ('authorization', 'x-iamcore-api-key')
        }
    logger.error(f"Invalid headers class {headers.__class__} failed to extract auth headers.")
    return dict()
