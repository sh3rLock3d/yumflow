from flows.models import Flow, DataFrame
from rest_framework import viewsets, permissions
from .serializers import DataFrameSerializers, FlowSerializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .MLTools.main import *
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

class FlowViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = FlowSerializers

    def get_queryset(self):
        return self.request.user.flows.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['post'])
    def set_data(self, request, pk=None):
        flow = self.get_object()

        data =  request.FILES.get("trainData")

        data = read_CSV_data(data.read(), request.data["addTimeCol"])
        
        df1 = DataFrame(data=data)
        df1.save()
        if flow.data != None:
            flow.data.delete()
        flow.data = df1
        print(df1.data)
        flow.save()
        return Response(FlowSerializers(flow).data)
    
    @action(detail=True, methods=['post'])
    def append_data(self, request, pk=None):
        flow = self.get_object()

        data =  request.FILES.get("trainData")

        df2 = read_CSV_data(data.read(), request.data["addTimeCol"])
        
        df1 = flow.data.data
        # todo if df1 == null

        df = append_data(df1, df2)
        
        flow.data.data = df
        flow.data.save()
        
        return Response(FlowSerializers(flow).data)
        
    @action(detail=True, methods=['get'])
    def get_gathering_data_info(self, request, pk=None):
        flow = self.get_object()

        datas = {
            'data':flow.data.info() if flow.data else None ,
        }
        return Response(datas)

    
    @action(detail=True, methods=['post'])
    @parser_classes([JSONParser])
    def prepare_data(self, request, pk=None):
        flow = self.get_object()
        #print('start')
        #print(type(request.body))
        #print('end')
        #data = flow.data
        df = filter_data(request.data['cols'], request.data['colFilter'], request.data['constraints'])
        
        return Response({'status': 'password set'})

    

    
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
    
