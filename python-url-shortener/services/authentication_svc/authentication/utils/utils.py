REDIS_ADDRESS = "my-release-redis-master.default.svc.cluster.local"

class User:
    def __init__(self, request_context):
        self.request_context = request_context

    @property
    def username(self):
            return self.request_context.values.get("username")

    @property
    def password(self):
            return self.request_context.values.get("password")

    @property
    def user_id(self):
            return self.request_context.values.get("user_id") or self.request_context.remote_addr