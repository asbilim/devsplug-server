from rest_framework.serializers import ModelSerializer
from .models import ProblemItem,Problems,Attachment


class AttachmentSerializer(ModelSerializer):

    class Meta:

        model = Attachment
        fields =  ['title','file']
class ProblemItemSerializer(ModelSerializer):

    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta:

        fields = "__all__"
        model = ProblemItem

class ProblemSerializer(ModelSerializer):

    problems = ProblemItemSerializer(many=True,read_only=True)
    class Meta:

        fields = "__all__"
        model = Problems

