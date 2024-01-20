from __future__ import annotations

import abc
import typing as t

from .abc import Timer


class DatabaseBuilder(abc.ABC):
    """
    Database Builder

    The base builder, for creating a Database Instance.
    """

    @abc.abstractmethod
    async def connect(self) -> None:
        """
        Connect to the database

        Make the connection to the database.

        Raises
        ------
        DatabaseConnectionException
            Raised when the database fails to connect properly.
        """
        ...

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """
        Shutdown the database

        Allows for safely shutting down the database.

        Raises
        ------
        DatabaseShutdownException
            Raised when an error occurs shutting down the database.
        """
        ...

    @abc.abstractmethod
    async def add(self, timer: Timer) -> None:
        """
        Add a timer to the database

        Add a new timer to your database.

        Parameters
        ----------
        timer : Timer
            The timer you wish to add.

        Raises
        ------
        DatabaseUniqueException
            a name/key value already exists of this type.
        """
        ...

    @abc.abstractmethod
    async def fetch(self, name: str, key: str) -> Timer | None:
        """
        Fetch a timer

        Fetch a timer, via its name and key.

        Parameters
        ----------
        name : str
            The name of the function, the Timer is attached too.
        key : str
            The key of the Timer

        Returns
        -------
        Timer
            If a valid timer exists, it will return a timer.
        """
        ...

    @abc.abstractmethod
    async def fetch_all(self) -> t.Sequence[Timer] | None:
        """
        Fetch all timers

        Fetch every single timer from the database.

        Returns
        -------
        typing.Sequence[Timer]
            The list of Timers from the database.
        """
        ...

    @abc.abstractmethod
    async def delete(self, name: str, key: str) -> None:
        """
        Delete a timer

        Delete a specific timer from the database.

        Parameters
        ----------
        name : str
            The name of the function, the Timer is attached too.
        key : str
            The key of the Timer
        """
        ...

    @abc.abstractmethod
    async def delete_all(self, name: str) -> None:
        """
        Delete All Timers from a specific function name.

        Parameters
        ----------
        name : str
            The name of the function, the Timer is attached too.
        """
        ...

    @abc.abstractmethod
    async def clear(self) -> None:
        """
        Clear Timers

        Clear All timers present in the database.
        """
        ...


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
