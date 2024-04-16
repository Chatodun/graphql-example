class HideIntrospectMiddleware:
    """
    This middleware should use for production mode. This class hide the
    introspection.
    """
    def resolve(self, next, root, info, **kwargs):
        if isinstance(root, tuple) and root[0] == 'user' and not info.context.user.has_perm('auth.view_user'):
            return ''
        return next(root, info, **kwargs)
