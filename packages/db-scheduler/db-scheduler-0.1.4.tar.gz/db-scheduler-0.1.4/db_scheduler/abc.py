import attrs
import enum


class TimerStatus(enum.Enum):
    """
    The current state, of the [Timer][db_scheduler.abc.Timer]
    """

    FINISHED = 0
    """The timer has finished."""
    STARTED = 1
    """The timer has been started."""
    WAITING = 2
    """
    The timer is waiting to be started.
    
    !!! NOTE
        If its waiting, the time variable, will be -1.
    """


@attrs.define
class Timer:
    """
    Timer

    The base timer, that is returned when a Timer gets started, or ends.
    """

    name: str
    """The name, attached to a function, that it will call."""
    key: str
    """The key, or unique ID given."""
    time: int
    """The end time, of when this timer is to end. (-1 if the timer has not been started yet.)"""
    default_time: int
    """The default time, that this event will take."""
    status: TimerStatus
    """The current state of this timer."""


# MIT License

# Copyright (c) 2024 Platy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
