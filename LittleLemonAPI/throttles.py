from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):
    # new throttle policy
    scope = 'ten'