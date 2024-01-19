import logging
from enum import Enum
from typing import Any, Generator, Set

from iamcore.client.evaluete import authorize
from rest_framework import permissions
from rest_framework.request import Request

from ..settings import IAM_APPLICATION_NAME, IAM_TENANT_ID, IAM_ACCOUNT_NAME

logger = logging.getLogger(__name__)


def action_adapter(application, resource_type, method):
    methods = {
        "POST": "create",
        "DELETE": "delete",
        "GET": "read",
        "PUT": "update",
        "PATCH": "update",
    }
    action = application
    if not resource_type:
        return action + ":*"
    action += ":" + resource_type

    if not method:
        return action + ":*"

    return action + ":" + methods.get(method, "*")


class AuthMode(Enum):
    EVALUATE_RESOURCE_ID = 0
    EVALUATE_RESOURCE_TYPE = 1


class LazyCheckId:
    def __init__(self, generator: Generator[str, Any, None]):
        self.generator: Generator[str, Any, None] = generator
        self.resource_ids: Set[str] = set()

    def check(self, resource_id):
        if resource_id in self.resource_ids:
            return True
        for rid in self.generator:
            self.resource_ids.add(rid)
            if rid == resource_id:
                return True
        raise IAMUnauthorizedException("Not authorized resource id")


class IAMTenantManagerPermissions(permissions.BasePermission):
    @staticmethod
    def is_batch(view):
        return hasattr(view, 'BATCH') and getattr(view, 'BATCH')

    def detect_auth_mode(self, request, view) -> AuthMode:
        if hasattr(request, 'auth_mode'):
            return request.auth_mode
        if request.method == 'GET' and self.is_batch(view):
            request.auth_mode = AuthMode.EVALUATE_RESOURCE_TYPE
        else:
            request.auth_mode = AuthMode.EVALUATE_RESOURCE_ID
        return request.auth_mode

    def has_permission(self, request, view):
        if not hasattr(view, "RESOURCE_TYPE"):
            logger.error("Missing RESOURCE_TYPE attribute definition for model " + view.__class__)
            return False
        if self.detect_auth_mode(request, view) == AuthMode.EVALUATE_RESOURCE_ID:
            return True
        resource_type = view.RESOURCE_TYPE
        action = action_adapter(IAM_APPLICATION_NAME, resource_type, request.method)
        tenant_id = self.get_tenant_id(request, view, None)
        resource_path = ""
        if hasattr(view, "get_resource_path") and callable(getattr(view, "get_resource_path")):
            resource_path = view.get_resource_path(request, None)
        resources_ids: Generator[str, Any, None] = authorize(
            request.auth_headers,
            request.user.irn,
            IAM_ACCOUNT_NAME,
            IAM_APPLICATION_NAME,
            tenant_id,
            resource_type,
            resource_path,
            action
        )
        request.resources = LazyCheckId(resources_ids)
        return True

    @staticmethod
    def has_object_permission_by_type(request: Request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        resource_id = "*"
        if hasattr(view, "get_resource_id") and callable(getattr(view, "get_resource_id")):
            resource_id = view.get_resource_id(request, obj)
        return request.resources_ids.check(resource_id)

    @classmethod
    def has_object_permission_by_id(cls, request: Request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not hasattr(view, "RESOURCE_TYPE"):
            logger.error("Missing RESOURCE_TYPE attribute definition for model " + view.__class__)
            return False
        resource_type = view.RESOURCE_TYPE

        if not hasattr(view, "get_resource_id") and not hasattr(view, "get_resource_path"):
            return True
        resource_path = ""
        resource_id = "*"
        if hasattr(view, "get_resource_id") and callable(getattr(view, "get_resource_id")):
            resource_id = view.get_resource_id(request, obj)
        elif hasattr(obj, "get_resource_id") and callable(getattr(obj, "get_resource_id")):
            resource_id = obj.get_resource_id(request)
        if hasattr(view, "get_resource_path") and callable(getattr(view, "get_resource_path")):
            resource_path = view.get_resource_path(request, obj)
        elif hasattr(obj, "get_resource_path") and callable(getattr(obj, "get_resource_path")):
            resource_path = obj.get_resource_path(request)

        action = action_adapter(IAM_APPLICATION_NAME, resource_type, request.method)
        tenant_id = cls.get_tenant_id(request, view, obj)
        logger.info(f"Going to verify {action} action for {resource_id}")
        authorize(
            request.auth_headers,
            request.user.irn,
            IAM_APPLICATION_NAME,
            tenant_id,
            resource_type,
            resource_path,
            action,
            resource_ids=[resource_id]
        )
        return True

    def has_object_permission(self, request: Request, view, obj):
        if self.detect_auth_mode(request, view) == AuthMode.EVALUATE_RESOURCE_TYPE:
            return self.has_object_permission_by_type(request, view, obj)
        return self.has_object_permission_by_id(request, view, obj)

    @staticmethod
    def get_tenant_id(request: Request, view, obj):
        if hasattr(view, "get_tenant_id") and callable(getattr(view, "get_resource_id")):
            return view.get_tenant_id(request, obj)
        tenant_id_params = (
            'tenant_id', 'tenant-id', 'tenantId'
        )
        for param in tenant_id_params:
            if param in request.query_params.keys():
                return request.query_params.get(param)
        return IAM_TENANT_ID
