# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from chartit import DataPool, Chart
import time
from pytorque.models import PBSServer, PBSUserStat


class ChartGenerator():
    @staticmethod
    def getJobStatChart(title, currentTime):
        statistics =\
        DataPool(
            series=
            [{'options': {
                'source': PBSServer.objects.filter(time__gte=(currentTime - timedelta(hours=+2)))},
              #order_by('time')[9:]
              'terms': [
                  ('time', lambda d: time.mktime(d.timetuple())),
                  'running_jobs',
                  'queued_jobs',
                  'total_jobs']}
            ])

        #Step 2: Create the Chart object
        chart = Chart(
            datasource=statistics,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
              'terms': {
                  'time': [
                      'running_jobs',
                      'queued_jobs',
                      'total_jobs']
              }}],
            chart_options=
                {'title': {
                'text': title},
                 'xAxis': {
                     'title': {
                         'text': 'Time'}}},
            x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%H:%M"), False))

        return chart

    @staticmethod
    def getUserStatChart(title, currentTime):
        try:
            lastUserStatTime = PBSUserStat.objects.latest('time').time
        except Exception as exc:
            lastUserStatTime = datetime.now()

        statistics = DataPool(
            series=
            [{'options': {
                'source': PBSUserStat.objects.filter(
                    time__gte=(lastUserStatTime - timedelta(minutes=+9))) #.order_by('-time')
            },
              'terms': [
                  'username',
                  'jobCount']}
            ])

        chart = Chart(
            datasource=statistics,
            series_options=
            [{'options': {
                'type': 'bar',
                'stacking': False},
              'terms': {
                  'username': [
                      'jobCount']
              }}],
            chart_options=
                {'title': {
                'text': title},
                 'xAxis': {
                     'title': {
                         'text': 'User'}}})

        return chart