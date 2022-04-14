from main import is_request
from sim.channels import Channel, ChannelBalancer
from sim.request import Request
from collections import Counter


def test_success_put():
    # Given
    channel = Channel(processing_intensity=5)
    request = Request(0.1)
    # When
    channel.put(request)
    # Then
    assert channel.free == False and channel.processing_time > 0 and channel.request == request


def test_unsuccess_put():
    # Given
    channel = Channel(processing_intensity=5)
    request = Request(0.1)
    channel.put(request)
    catched_error = False
    # When
    try:
        channel.put(request)
    except BufferError:
        catched_error = True
    # Then
    assert catched_error


def test_success_step():
    # Given
    channel = Channel(processing_intensity=5)
    request = Request(0.1)
    channel.put(request)
    step = 0.01
    # When
    result = channel.step(step)
    # then
    assert result is None and channel.processing_time == request.time_in_processing - step


def test_expired_step():
    # Given
    channel = Channel(processing_intensity=5)
    request = Request(0.1)
    channel.put(request)
    step = channel.processing_time
    # When
    result = channel.step(step)
    # Then
    assert channel.request is None and channel.free


def test_clean_request_expired_step():
    # Given
    channel = Channel(processing_intensity=5)
    request = Request(0.1)
    channel.put(request)
    step = channel.processing_time
    # When
    result = channel.step(step)
    result = channel.step(step)
    # Then
    assert result is None and channel.free and channel.request is None




def test_channel_balancer_success_put():
    # Given
    cb = ChannelBalancer([Channel(processing_intensity=10), Channel(processing_intensity=5)])
    request = Request(0.1)
    # When
    result = cb.put(request)
    # Then
    assert result.time_in_processing > 0


def test_channel_balancer_fail_put():
    # Given
    cb = ChannelBalancer([Channel(processing_intensity=10), Channel(processing_intensity=5)])
    request = Request(0.1)
    cathched_error = False
    # When
    cb.put(request)
    cb.put(request)
    try:
        cb.put(request)
    except BufferError:
        cathched_error = True
    # Then
    assert cathched_error


def test_channel_balancer_on_interval():
    current_time = 0
    step = 0.0001
    income_intensity = 4.8
    cb = ChannelBalancer(channels=[Channel(2), Channel(2)])
    result_lst = []
    while current_time < 50:
        request = None
        result = None
        if is_request(step, income_intensity):
            request = Request(current_time)
            try:
                result = cb.put(request)
            except BufferError:
                pass
        cb.step(step)
        if result:
            result_lst.append(result)
        current_time += step
    dublicate = [k for k, v in Counter([result.create_time for result in result_lst]).items() if v > 1]
    assert len(result_lst) > 1 > len(dublicate)
