from __future__ import annotations

from .base import DatabaseBuilder
import typing as t
import uuid
import datetime
import asyncio
from .abc import Timer, TimerStatus
from .errors import TimerException

FuncT = t.Callable[[Timer], t.Coroutine[t.Any, t.Any, None]]


class Client:
    """
    Timer Client

    The base class, for creating everything related to database timers.

    Parameters
    ----------
    database : DatabaseBuilder
        The database you will use for the Timer class.
    delay : int
        The delay of when timers have a task created for them.

        ??? note "About delay"
            The `delay` argument can be modified, but would not be recommended.
            <br>
            <br>● Lower number: This will cause there to be more tasks, but the tasks will last for a shorter amount of time.
            <br>● Higher number: This will cause there to be more tasks, with longer times between execution of the tasks.
    """

    def __init__(self, database: DatabaseBuilder, delay: int = 60):
        self._db = database

        self._functions: list[tuple[str, FuncT]] = []

        self._tasks: dict[str, asyncio.Task[None]] = {}

    async def _delay_task(self, time: int, timer: Timer, functions: list[FuncT]):
        await asyncio.sleep(time)

        await self._db.delete(timer.name, timer.key)

        timer.status = TimerStatus.FINISHED

        for function in functions:
            await function(timer)

        self._tasks.pop(timer.key)

    async def _check(self, timer: Timer):
        """This checks if the timer either needs to be added to the tasks list, or not."""
        if timer.key in self._tasks.keys():
            raise KeyError("Timer key, matches with a pre-existing task.")
        
        func_list: list[FuncT] = []
        
        for func in self._functions:
            name = func[0]
            func = func[1]

            if name == timer.name:
                func_list.append(func)

        if len(func_list) <= 0:
            raise ValueError("No functions where started for this timer, as it does not exist.")
        
        # TODO: Add a function to delete the timer if no functions exist (if user wants that.)


        current_time = datetime.datetime.now()

        timer_end = datetime.datetime.fromtimestamp(timer.time)

        if timer_end < current_time + datetime.timedelta(hours=1):
            timer_length = int((timer_end - current_time).total_seconds())
            task = asyncio.create_task(self._delay_task(timer_length, timer, func_list))
            self._tasks.update({timer.key: task})

    async def load(self) -> None:
        """
        Load Timer

        Load the timer instance, connect to the database, and check the timers.
        """
        await self._db.connect()

        timers = await self._db.fetch_all()

        if timers:
            for timer in timers:
                await self._check(timer)

        # TODO: check every 20 minutes, if a new timer should be added to the tasks.

    async def unload(self) -> None:
        """
        Unload Timer

        Unload the timer instance, disconnect from the database, and clean up.
        """
        await self._db.shutdown()

    async def create(self, delay: int, name: str) -> Timer:
        """
        Create Timer

        Creates a new timer with the set time.

        !!! note
            This does not start the timer. You must run the start function.

        Parameters
        ----------
        delay : int
            The delay in which it will take to trigger this timer.
        name : str
            The name of the function, that will run.
        """
        key = str(uuid.uuid4())

        return Timer(name, key, -1, delay, TimerStatus.WAITING)

    async def start(self, timer: Timer) -> Timer:
        """
        Start Timer

        Start a timer, for your event.

        Parameters
        ----------
        timer : Timer
            The timer you wish to start

        Raises
        ------
        TimerException
            The timer has already ended.
        """
        if timer.status == TimerStatus.FINISHED:
            raise TimerException("This timer has already ended.")

        current_time = datetime.datetime.now()
        new_time = int(current_time.timestamp() + timer.default_time)

        new_timer = Timer(
            timer.name, timer.key, new_time, timer.default_time, TimerStatus.STARTED
        )

        await self._check(new_timer)

        await self._db.add(new_timer)

        return new_timer

    async def cancel(self, timer: Timer) -> None:
        """
        Cancel a timer

        Cancel the requested timer.

        Parameters
        ----------
        timer : Timer
            The timer you wish to cancel.
        """
        task = self._tasks.get(timer.key)

        if task:
            task.cancel()

        await self._db.delete(timer.name, timer.key)

    def subscribe(self, name: str, func: FuncT) -> None:
        self._functions.append((name, func))

    def listen(self, name: str) -> t.Callable[[FuncT], FuncT]:
        """
        Listen for the name

        This will listen for this functions name, and if any timers call that specific name, it will call it.

        !!! warning
            The name **MUST** be unique. If they are not unique, the program will not run.

        Parameters
        ----------
        name : str
            The name of the function
        """

        def decorator(func: FuncT) -> FuncT:
            self._functions.append((name, func))
            return func

        return decorator


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
