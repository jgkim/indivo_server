"""
Vocabularies JSON Serializer

"""

from django.core.serializers.json import Serializer
from indivo.settings import VOCAB_SERVER_URL

class JSONSerializer(Serializer):
    def end_serialization(self):
        for i, obj in enumerate(self.objects):
            self.objects[i] = obj.get('fields', {})
            self.objects[i]['_id'] = obj.get('pk')

            if 'identifier' in self.objects[i]:
                self.objects[i]['@id'] = '{}/{}/{}'.format(VOCAB_SERVER_URL, self.objects[i]['vocabulary'], self.objects[i]['identifier'])
            else:
                self.objects[i]['@id'] = '{}/{}'.format(VOCAB_SERVER_URL, self.objects[i]['_id'])

        return super(JSONSerializer, self).end_serialization()