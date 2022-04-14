from sim.channels import Channel, ChannelBalancer
from sim.request import Request


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
    assert result == request and channel.free


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
