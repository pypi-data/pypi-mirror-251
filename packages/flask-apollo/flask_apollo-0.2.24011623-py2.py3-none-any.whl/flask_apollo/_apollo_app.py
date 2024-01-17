# -*- coding: utf-8 -*-
# @Time     : 2023/5/17 10:34
# @Author   : binger
from functools import wraps
from typing import Optional, Dict

from flask import Flask

from .apollo import Apollo


class FlaskApollo(Apollo):
    UPDATE_FUNC_CB_FIELD = "cb"

    def __init__(self, config_url, app_id, cluster="default", secret=None, request_timeout=None,
                 ip=None, notification_rule: Optional[Dict[str, Dict]] = None):
        self._notification_rule = notification_rule or {"application": {"prefix": ""}}
        super().__init__(config_url, app_id, cluster, secret, keep_hot_update=False, request_timeout=request_timeout,
                         ip=ip, namespaces=self._notification_rule.keys(), change_func=self._handle_data_change)
        self._result_map = {}
        self._sync_all_result_cb = None
        self.app = None

    def init_app(self, app: Flask) -> None:
        self.app = app
        self.init(lambda namespace, data: self.app.config.from_mapping(data))

    def init(self, sync_all_result_cb=None) -> None:
        self._sync_all_result_cb = sync_all_result_cb
        self.sync_for_app()
        self.start()

    def _handle_data_change(self, namespace, notification_id, configurations: dict, old_configurations: dict) -> None:
        n_info = self._notification_rule.get(namespace, {})
        prefix = n_info.get("prefix")
        if prefix:
            configurations = {key: value for key, value in configurations.items() if key.startswith(prefix)}

        callable(self._sync_all_result_cb) and self._sync_all_result_cb(namespace, configurations)
        func = n_info.get(self.UPDATE_FUNC_CB_FIELD)
        if callable(func):
            self._result_map[namespace] = func(notification_id, configurations, old_configurations)

    def register_for_sync(self, namespace: Optional[str], prefix=None):
        # 监听启动后，不允许注册
        # assert not self.is_syncing, "The monitoring has already started, and the current registration is invalid"

        def decorator(func):
            self._notification_rule[namespace] = {self.UPDATE_FUNC_CB_FIELD: func, "prefix": prefix}
            self.add_notification_ids((namespace,))

            @wraps(func)
            def wrapper(*args, **kwargs):
                return self._result_map.get(namespace)

            return wrapper

        return decorator
