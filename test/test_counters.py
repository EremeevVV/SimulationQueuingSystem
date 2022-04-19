from sim.counters import RequestCounter, StateCounter
from sim.request import Request


# StateCounter tests
def test_state_counter_init():
    # Given
    num_channels = 2
    max_queue_size = 4
    # When
    st = StateCounter(num_channels, max_queue_size)
    # Then
    expected = f'{num_channels} requests in channels and {max_queue_size} in queue'
    assert len(st.counter) == len(st.states_names) and st.states_names[-1] == expected


def test_state_counter_count():
    # Given
    num_channels = 2
    max_queue_size = 4
    st = StateCounter(num_channels, max_queue_size)
    # When
    st.count(2, 3)
    st.count(2, 3)
    # Then
    expected = 2
    assert st.counter[-2] == expected


def test_state_counter_get_probability_be_in_state():
    # Given
    num_channels = 2
    max_queue_size = 4
    st = StateCounter(num_channels, max_queue_size)
    st.counter = [c for c in range(7)]
    # When
    prob = st.get_probability_be_in_state(6)
    # Then
    expected = 6 / 21
    assert prob == expected


def test_state_counter_get_mean_queue():
    # Given
    num_channels = 2
    max_queue_size = 4
    st = StateCounter(num_channels, max_queue_size)
    st.counter = [c for c in range(7)]
    # When
    mean_queue = st.get_mean_queue()
    # Then
    expected = 50 / 21
    assert mean_queue == expected


def test_state_counter_get_mean_busy_channels():
    # Given
    num_channels = 2
    max_queue_size = 4
    st = StateCounter(num_channels, max_queue_size)
    st.counter = [c for c in range(7)]
    # When
    mean_busy_channels = st.get_mean_busy_channels()
    # Then
    expected = 41 / 21
    assert mean_busy_channels == expected


def test_request_counter_get_absolute_bandwidth():
    # Given
    rc = RequestCounter()
    interval = 10
    req_count = 7
    rc.success_counter= [Request(i) for i in range(req_count)]
    # When
    result = rc.get_absolute_bandwidth(interval)
    # Then
    assert result == req_count/interval

def test_request_counter_get_relative_bandwidth():
    # Given
    rc = RequestCounter()
    success_count = 7
    reject_count = 3
    rc.success_counter = [Request(i) for i in range(success_count)]
    rc.rejected_counter = [Request(i) for i in range(success_count,success_count+reject_count)]

    # When
    result = rc.get_relative_bandwidth()
    # Then
    assert result == success_count / (success_count+reject_count)


def test_request_counter_get_reject_probability():
    # Given
    rc = RequestCounter()
    success_count = 7
    reject_count = 3
    rc.success_counter = [Request(i) for i in range(success_count)]
    rc.rejected_counter = [Request(i) for i in range(success_count, success_count + reject_count)]
    # When
    result = rc.get_reject_probability()
    # Then
    assert result == reject_count / (success_count + reject_count)
