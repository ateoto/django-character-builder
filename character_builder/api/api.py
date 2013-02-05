from tastypie.api import Api
from resources import (ClassTypeResource, RaceResource,
                        AlignmentResource, DeityResource, CharacterResource)


v1 = Api(api_name='v1')

v1.register(CharacterResource())
v1.register(ClassTypeResource())
v1.register(RaceResource())
v1.register(DeityResource())
v1.register(AlignmentResource())
