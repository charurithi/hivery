import falcon
from .paranuara import Resource,FriendResource,PeopleResource
api = application = falcon.API()

companyDetails = Resource()
api.add_route('/v1/company/{company_name}', companyDetails)

friendDetails = FriendResource()
api.add_route('/v1/people/{ppl_one},{ppl_two}',friendDetails)

peopleDetails = PeopleResource()
api.add_route('/v1/people/{ppl_one}',peopleDetails)
