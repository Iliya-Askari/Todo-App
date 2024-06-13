from rest_framework import serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    '''
    show in the Task
    '''
    # Display user based on username
    user = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'complete','created_date')

    def get_fields(self):
        '''
        The complete field only works for updating the task
        '''
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and not self.instance:
            fields.pop('complete', None)
        return fields
    
    def create(self, validated_data):
        '''
        The user field is filled automatically, provided that the user is logged in
        '''
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)