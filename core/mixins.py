from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class CustomListUpdateModelMixin:
    """
    Updates a list of model instances.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = request.data
        for instance_data in data:
            id = instance_data.pop("id", None)
            try:
                instance = get_object_or_404(self.get_queryset(), id=id)
            except:
                instance = None
            serializer = self.get_serializer(
                instance, data=instance_data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
