from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    
#agr throttling ki alag se file ni bnani to scope throttling use kro .