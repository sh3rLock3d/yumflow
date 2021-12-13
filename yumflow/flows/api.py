from flows.models import Flow, DataFrame, ModelResult, PrepareData, ModelOfTrain
from rest_framework import viewsets, permissions
from .serializers import DataFrameSerializers, FlowSerializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .MLTools.main import *
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.core.files import File
import os
from rest_framework import status

class FlowViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = FlowSerializers
        
    
    def get_queryset(self):
        return self.request.user.flows.all()

    def create(self, request, *args, **kwargs):
        for i in self.request.user.flows.all():
            if i.title == request.data.get('title'):
                content = {'message': 'عنوان تکراری است'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            key, value = serializer.errors.popitem()
            if key == 'title':
                key = "عنوان: "
            elif key == 'description':
                key = 'توضیحات: '
            content = {'message': key+value[0]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['post'])
    def set_data(self, request, pk=None):
        flow = self.get_object()

        data =  request.FILES.get("trainData")
        try:
            data = read_CSV_data(data.read(), request.data["addTimeCol"])
        except:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        df1 = DataFrame(data=data)
        df1.save()
        if flow.data != None:
            flow.data.delete()
        flow.data = df1
        flow.save()
        return Response(FlowSerializers(flow).data)
    
    @action(detail=True, methods=['post'])
    def append_data(self, request, pk=None):
        flow = self.get_object()
        data =  request.FILES.get("trainData")    
        try:
            df2 = read_CSV_data(data.read(), request.data["addTimeCol"])
        except:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        df1 = flow.data.data
        
        if df1 == None:
            content = {'message': 'داده ای وجود ندارد که به آن اضافه کنیم.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = append_data(df1, df2)
        except:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        flow.data.data = df
        flow.data.save()
        
        return Response(FlowSerializers(flow).data)
        
    @action(detail=True, methods=['get'])
    def get_gathering_data_info(self, request, pk=None):
        flow = self.get_object()
        if flow.data == None:
            content = {'message': 'داده ای ساخته نشده تا نمایش داده شود .'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        datas = show_digest_of_data(flow.data.data)
        return Response(datas)

    
    @action(detail=True, methods=['post'])
    @parser_classes([JSONParser])
    def prepare_data(self, request, pk=None):
        flow = self.get_object()
        # df = filter_data(request.data['cols'], request.data['colFilter'], request.data['constraints'], flow.data.data)
        
        name = request.data.get('name')

        if request.data['name'] == None:
            content = {'message': 'برای مدل جدید داده ای انتخاب نشده است.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            preparation =  PrepareData(cols = request.data['cols'], colFilter = request.data['colFilter'], constraints= create_query(request.data['constraints']))
        except:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        preparation.save()
        
        try:
            modelOfResult = ModelResult(name=name, preparation=preparation)
        except:
            content = {'message': 'نام تکراری است'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        modelOfResult.save()

        flow.modelResult.add(modelOfResult)
        flow.save()

        return Response({'status': 'done'})

    @action(detail=True, methods=['get'])
    @parser_classes([JSONParser])
    def get_all_flow_models(self, request, pk=None):
        flow = self.get_object()
        res = []
        for mor in flow.modelResult.all():
            res.append({
                "name":mor.name,
                "id":mor.id,
                "prepration_id":mor.preparation.id,
                "modelOfTrain_id": mor.modelOfTrain.id if mor.modelOfTrain else None,
                "testResult_id": mor.testResult.id if mor.testResult else None,
                "score": mor.testResult.score if  mor.testResult else -1,
            })
        return Response({'models': res})

    @action(detail=True, methods=['post'])
    @parser_classes([JSONParser])
    def train_data(self, request, pk=None):
        flow = self.get_object()
        modelResult = None
        id = request.get('id')
        if id == None:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        for mor in flow.modelResult.all():
            if mor.id == id:
                modelResult = mor
                break

        if modelResult == None:
            content = {'message': 'چنین شناسه ای وجود ندارد'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


        preparation = modelResult.preparation

        if preparation == None:
            content = {'message': 'ابتدا داده ها را وارد کنید'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            filter_data(preparation.cols, preparation.colFilter, preparation.constraints, flow.data.data)
        except:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        with File(open('flows/MLTools/createModel/final_test/insta_trained_model.txt', mode='rb'), name='insta_trained_model.txt') as f:
            m = ModelOfTrain(upload=f)
            m.save()
            modelResult.modelOfTrain = m
            modelResult.save()
            flow.save()
        
        return Response({'status': 'done'})
        
    @action(detail=True, methods=['post'])
    @parser_classes([JSONParser])
    def test_data(self, request, pk=None):
        flow = self.get_object()

        modelResult = None
        id = request.data.get('id')
        if id == None:
            content = {'message': 'داده های ورودی معتبر نیست'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        for mor in flow.modelResult.all():
            if mor.id == id:
                modelResult = mor
                break

        if modelResult == None:
            content = {'message': 'چنین شناسه ای وجود ندارد'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        m = modelResult.modelOfTrain.upload
        os.popen(f'cp {m.path} flows/MLTools/createModel/final_test/insta_trained_model.txt')
        data =  request.FILES.get("testData")
        data = read_CSV_data(data.read(), False)        
        res = test_data(data)
        return Response({'result': res})

    


class DataFrameViewSet(viewsets.ModelViewSet):
    queryset = DataFrame.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DataFrameSerializers
    
