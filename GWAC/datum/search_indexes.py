from haystack import indexes
from .models import Objects

class ObjectsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #对以下字段建立索引
    Object_name = indexes.CharField(model_attr='Object_name')
    Object_alias_1 = indexes.CharField(model_attr='Object_alias_1')
    Object_alias_2 = indexes.CharField(model_attr='Object_alias_2')
    Obj_Type = indexes.CharField(model_attr='Obj_Type')
    Obj_source = indexes.CharField(model_attr='Obj_source')
    Observer = indexes.CharField(model_attr='Observer')
    Obs_program = indexes.CharField(model_attr='Obs_program')
    Obj_RA = indexes.CharField(model_attr='Obj_RA')
    Obj_DEC = indexes.CharField(model_attr='Obj_DEC')
    Group_ID = indexes.CharField(model_attr='Group_ID')
    Unit_ID = indexes.CharField(model_attr='Unit_ID')
    Observation_type = indexes.CharField(model_attr='Observation_type')
    Observation_strategy = indexes.CharField(model_attr='Observation_strategy')
    Obs_date_begin = indexes.CharField(model_attr='Obs_date_begin')
    Obs_date_end = indexes.CharField(model_attr='Obs_date_end')
    note = indexes.CharField(model_attr='note')
    Obs_stage = indexes.CharField(model_attr='Obs_stage')
    mode = indexes.CharField(model_attr='mode')

    def get_model(self):
        return Objects

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(Obs_stage__in=['current', 'past', 'future'])