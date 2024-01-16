from rest_framework import viewsets
from rest_framework.serializers import ChoiceField
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from django_celery_beat.admin import TaskSelectWidget
from django_celery_beat.models import ClockedSchedule, SolarSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask
from .serializers import (
    ClockedScheduleSerializer, SolarScheduleSerializer, CrontabScheduleSerializer, IntervalScheduleSerializer,
    PeriodicTaskSerializer, PeriodicTaskListSerializer
)
from .filters import (
    ClockedScheduleFilter, SolarScheduleFilter, CrontabScheduleFilter, IntervalScheduleFilter, PeriodicTaskFilter
)


class ClockedScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = ClockedScheduleFilter
    ordering_fields = ['id']


class SolarScheduleViewSet(viewsets.ModelViewSet):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = SolarScheduleFilter
    ordering_fields = ['id']


class CrontabScheduleViewSet(viewsets.ModelViewSet):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = CrontabScheduleFilter
    ordering_fields = ['id']


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = IntervalScheduleFilter
    ordering_fields = ['id']


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = PeriodicTaskFilter
    ordering_fields = ['id']

    def get_serializer(self, *args, **kwargs):
        serializer = super(PeriodicTaskViewSet, self).get_serializer(*args, **kwargs)
        serializer.fields['task'] = ChoiceField(choices=TaskSelectWidget().choices[1:])
        return serializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PeriodicTaskListSerializer
        else:
            return PeriodicTaskSerializer
