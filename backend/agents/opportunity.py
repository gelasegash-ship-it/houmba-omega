from ..core.models import Opportunity
class OpportunityScout:
    def rank(self, opportunities:list[Opportunity]): return sorted(opportunities,key=lambda x:x.score,reverse=True)
