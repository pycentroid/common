# noinspection PyUnresolvedReferences
import pytest
import time
from unittest import TestCase
from centroid.common import SyncSeriesEventEmitter, AsyncSeriesEventEmitter, AnyDict


def next_handler(event):
    event.total += 1


def once_handler(event):
    event.total += 1


def test_use_subscribe():
    event_series = SyncSeriesEventEmitter()
    subscription = event_series.subscribe(next_handler)
    TestCase().assertEqual(len(event_series.__handlers__), 1)
    event = lambda: None
    event.total = 100
    event_series.emit(event)
    TestCase().assertEqual(event.total, 101)
    event_series.emit(event)
    TestCase().assertEqual(event.total, 102)
    subscription.unsubscribe()
    TestCase().assertEqual(len(event_series.__handlers__), 0)


def test_use_subscribe_once():
    event_series = SyncSeriesEventEmitter()
    subscription1 = event_series.subscribe(next_handler)
    subscription2 = event_series.subscribe_once(next_handler)
    TestCase().assertEqual(len(event_series.__handlers__), 2)
    event = lambda: None
    event.total = 100
    event_series.emit(event)
    TestCase().assertEqual(event.total, 102)
    event_series.emit(event)
    TestCase().assertEqual(event.total, 103)
    event_series.emit(event)
    TestCase().assertEqual(event.total, 104)
    subscription1.unsubscribe()
    TestCase().assertEqual(len(event_series.__handlers__), 1)
    subscription2.unsubscribe()


async def test_use_async_subscribe():
    series = AsyncSeriesEventEmitter()

    async def next1(event):
        time.sleep(3)
        event.total += 2

    async def next2(event):
        time.sleep(2)
        event.total -= 1

    subscription1 = series.subscribe(next1)
    subscription2 = series.subscribe(next2)
    event = AnyDict(total=100)
    await series.emit(event)
    TestCase().assertEqual(event.total, 101)
    subscription1.unsubscribe()
    subscription2.unsubscribe()
    TestCase().assertEqual(len(series.__handlers__), 0)

async def test_use_async_subscribe_once():
    series = AsyncSeriesEventEmitter()

    async def next1(event):
        time.sleep(3)
        event.total += 2

    async def next2(event):
        time.sleep(2)
        event.total -= 1

    series.subscribe(next1)
    series.subscribe_once(next2)
    event = AnyDict(total=100)
    await series.emit(event)
    TestCase().assertEqual(event.total, 101)
    await series.emit(event)
    TestCase().assertEqual(event.total, 103)
    TestCase().assertEqual(len(series.__handlers__), 2)
    