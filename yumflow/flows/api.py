from flows.models import Flow, DataFrame
from rest_framework import viewsets, permissions
from .serializers import DataFrameSerializers, FlowSerializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .MLTools.main import *

class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = FlowSerializers

    @action(detail=True, methods=['post'])
    def set_train_test_data(self, request, pk=None):
        flow = self.get_object()
        trainData =  request.FILES.get("train_data")
        x_train, y_train = read_CSV_data(trainData.read(), request.data["label_name"])
        testData =  request.FILES.get("test_data")
        x_test, y_test = read_CSV_data(testData.read(), request.data["label_name"])
        
        df1 = DataFrame(data=x_train)
        df1.save()
        if flow.x_train != None:
            flow.x_train.delete()
        flow.x_train = df1
        flow.save()
        
        df2 = DataFrame(data=y_train)
        df2.save()        
        if flow.y_train != None:
            flow.y_train.delete()
        flow.y_train = df2
        flow.save()

        df3 = DataFrame(data=x_test)
        df3.save()        
        if flow.x_test != None:
            flow.x_test.delete()
        flow.x_test = df3
        flow.save()

        df4 = DataFrame(data=y_test)
        df4.save()        
        if flow.y_test != None:
            flow.y_test.delete()
        flow.y_test = df4
        flow.save()
        return Response(FlowSerializers(flow).data)
        
        
    @action(detail=True, methods=['get'])
    def get_gathering_data_info(self, request, pk=None):
        flow = self.get_object()

        datas = {
            'x_train':flow.x_train.info() if flow.x_train else None ,
            'y_train':flow.y_train.info()if flow.y_train else None ,
            'x_test':flow.x_test.info()if flow.x_test else None ,
            'y_test': flow.y_test.info()if flow.y_test else None ,
        }
        return Response(datas)

    
    @action(detail=True, methods=['post'])
    def set_data_by_instagram_account(self, request, pk=None):
        flow = self.get_object()
        a = request.data["data"]
        # todo
        return Response({"error":"asdad"})
    


class DataFrameViewSet(viewsets.ModelViewSet):
    queryset = DataFrame.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DataFrameSerializers
    
