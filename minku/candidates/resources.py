from import_export import resources
from .models import Candidate


class CandidateResource(resources.ModelResource):
    class Meta:
        model = Candidate
