"""
A micro event loop library implementation from scratch.

This library provides a minimal but feature-complete asynchronous event loop
implementation for educational purposes. It demonstrates the core concepts of
asynchronous programming including:

- Task scheduling and management
- I/O multiplexing with non-blocking sockets
- Timeouts and sleep functionality
- Task cancellation
- Coroutine-based concurrency

The implementation uses Python's generator-based coroutines and the select module
for I/O multiplexing, providing a simplified model of how modern async frameworks
like asyncio work under the hood.

Understanding the Magic Behind Await:
------------------------------------
When you write "result = await coroutine_function()", Python actually desugars this into:

    coroutine = coroutine_function()            # obtain the coroutine object
    result = yield from coroutine.__await__()"  # delegate to the coroutine's generator

The __await__ method returns an iterator that follows the generator protocol. The
"yield from" expression delegates to this iterator until it's exhausted.

How Yield From Works:
-------------------
"yield from" is a Python feature that allows a generator to delegate part of its
operations to another generator. When you write:

    yield from some_generator()

It's equivalent to:

    for value in some_generator():
        yield value

But "yield from" also properly handles the return value of the sub-generator and
propagates exceptions. This allows for creating complex generator chains where values,
exceptions, and control flow can be passed between them seamlessly - which is exactly
what we need for implementing async/await.

Communication Between Coroutines and the Event Loop:
-------------------------------------------------
This mechanism enables two-way communication between coroutines and the event loop:

1. When a coroutine awaits something (like socket I/O or a timeout), it yields a
   request object to the event loop and suspends execution.

2. The event loop receives this request (e.g., "I need to read from this socket"),
   registers the appropriate file descriptor or timer, along with the associated
   coroutine, and then continues running other coroutines.

3. When the requested operation completes (e.g., data is available on the socket),
   the event loop resumes the coroutine by calling .send() with the result.

4. The coroutine continues execution from exactly where it left off, with the
   result of the await expression now available.

This cooperative multitasking system allows many coroutines to execute concurrently
without threads, sharing a single event loop that efficiently manages I/O operations.
"""

import asyncio
import select
import socket
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Coroutine, Generator, cast


@dataclass
class Task:
    """
    Represents a scheduled coroutine within the event loop.

    A Task wraps a coroutine and tracks its execution state including results,
    exceptions, and cancellation status.
    """

    def __init__(self, coroutine: Coroutine[Any, Any, Any]):
        """
        Initialize a new task with the given coroutine.

        Args:
            coroutine: The coroutine to be executed by this task
        """
        self.coroutine: Coroutine[Any, Any, Any] = coroutine
        self.generator: Generator[Any, Any, Any] = coroutine.__await__()
        self.result: Any = None
        self.exception: Exception | None = None
        self.cancelled: bool = False

    def cancel(self) -> None:
        """Mark the task as cancelled. The event loop will inject a CancelledError."""
        self.cancelled = True


class EventLoopRequest[T]:
    """
    Base class for all requests that can be awaited within the event loop.

    This is a typed generic class that defines the basic mechanism for yielding
    control back to the event loop. Subclasses represent specific types of
    requests (timeout, socket I/O, task scheduling, etc).
    """

    def __await__(self) -> Any:
        """
        Make this class awaitable in an async function.

        When an instance is awaited, it yields itself to the event loop and
        suspends the current coroutine until the event loop resumes it.

        Returns:
            The result provided by the event loop when resuming this coroutine
        """
        result = yield self
        return cast(T, result)


@dataclass
class Timeout(EventLoopRequest[None]):
    """
    Request that suspends the current coroutine for a specified time period.

    The event loop will resume this coroutine after the specified number of
    seconds have elapsed.
    """

    seconds: float


@dataclass
class Readable(EventLoopRequest[None]):
    """
    Request that suspends the current coroutine until a socket is readable.

    The event loop will resume this coroutine when data is available to be read
    from the specified socket.
    """

    socket: socket.socket


@dataclass
class Writable(EventLoopRequest[None]):
    """
    Request that suspends the current coroutine until a socket is writable.

    The event loop will resume this coroutine when the specified socket is ready
    to accept data for writing.
    """

    socket: socket.socket


@dataclass
class Errored(EventLoopRequest[None]):
    """
    Request that suspends the current coroutine until a socket has an error.

    The event loop will resume this coroutine when an error condition is detected
    on the specified socket.
    """

    socket: socket.socket


@dataclass
class Schedule(EventLoopRequest[Task]):
    """
    Request to schedule a new coroutine to be executed by the event loop.

    When awaited, returns a Task object representing the scheduled coroutine.
    """

    coroutine: Coroutine[Any, Any, Any]


@dataclass
class CancelTask(EventLoopRequest[None]):
    """
    Request to cancel a running task.

    The event loop will mark the specified task as cancelled and inject a
    CancelledError into its execution.
    """

    task: Task


class WatchedSocket:
    """
    A wrapper for socket objects being monitored by the event loop.

    This class associates a socket with the task that is waiting for I/O on that
    socket, and implements the necessary methods for use with select.select().
    """

    def __init__(self, socket: socket.socket, thread: Task):
        """
        Initialize a watched socket.

        Args:
            socket: The socket to watch
            thread: The task waiting for I/O on this socket
        """
        self.socket = socket
        self.socket.setblocking(False)
        self.thread: Task = thread

    def fileno(self) -> int:
        """
        Return the socket's file descriptor.

        This method is required for compatibility with select.select().

        Returns:
            The socket's file descriptor as an integer
        """
        return self.socket.fileno()

    def __eq__(self, other: object) -> bool:
        """
        Compare this WatchedSocket with another object.

        Two WatchedSocket objects are equal if they wrap the same socket.

        Args:
            other: The object to compare with

        Returns:
            True if the objects are equal, False otherwise
        """
        if not isinstance(other, WatchedSocket):
            return NotImplemented
        return self.socket == other.socket

    def __hash__(self) -> int:
        """
        Return a hash value for this WatchedSocket.

        This method enables WatchedSocket objects to be used in sets.

        Returns:
            An integer hash value
        """
        return hash(self.socket)


def event_loop(main: Coroutine[Any, Any, Any]) -> None:  # noqa: C901
    """
    The core event loop implementation that drives the asynchronous execution.

    This function implements a basic event loop that:
    1. Manages the execution of tasks (coroutines)
    2. Handles I/O operations using non-blocking sockets
    3. Schedules timeouts and delays
    4. Supports task cancellation

    The event loop continues running until all tasks have completed or have been
    cancelled.

    Args:
        main: The main coroutine to execute as the entry point
    """
    task_queue: list[tuple[Task, Any]] = [(Task(main), None)]
    read_watches: set[WatchedSocket] = set()
    write_watches: set[WatchedSocket] = set()
    error_watches: set[WatchedSocket] = set()
    timers: list[tuple[datetime, Task]] = []

    while True:
        # Run all the threads until they finish or yield a socket
        while len(task_queue) > 0:
            thread, data = task_queue.pop(0)

            try:
                yielded = thread.coroutine.send(data)

                # Check if the task has been cancelled
                if thread.cancelled:
                    # Inject a CancelledError into the task
                    try:
                        thread.generator.throw(
                            asyncio.CancelledError("Task was cancelled")
                        )
                        # If the exception is caught, the task continues
                        task_queue.append((thread, None))
                    except StopIteration as e:
                        thread.result = e.value
                    except Exception as e:
                        thread.exception = e
                    finally:
                        continue

                match yielded:
                    case Schedule(coroutine):
                        t = Task(coroutine)
                        # resume the task which requested scheduling
                        task_queue.insert(0, (thread, t))
                        # add the new task to the queue
                        task_queue.append((t, None))

                    case CancelTask(task):
                        task.cancel()
                        # Resume the task that requested the cancellation
                        task_queue.insert(0, (thread, None))

                    case Timeout(seconds):
                        timers.append(
                            (
                                datetime.now() + timedelta(seconds=seconds),
                                thread,
                            )
                        )

                    case Readable(socket):
                        read_watches.add(WatchedSocket(socket, thread))

                    case Writable(socket):
                        write_watches.add(WatchedSocket(socket, thread))

                    case Errored(socket):
                        error_watches.add(WatchedSocket(socket, thread))

                    case _:
                        raise RuntimeError(
                            f"Expected a EventLoopRequest object, got a {type(yielded).__qualname__}"
                        )

            except StopIteration as e:
                thread.result = e.value
                break

            except Exception as e:
                thread.exception = e
                import traceback

                print(f"Exception in thread {thread}:")
                traceback.print_exc()
                break

        # Remove cancelled tasks from timers
        timers = [(time, thread) for time, thread in timers if not thread.cancelled]
        wakeup_date = min(timers, key=lambda x: x[0])[0] if timers else None

        # Remove watches for cancelled tasks
        read_watches = {
            socket
            for socket in read_watches
            if socket.fileno() >= 0 and not socket.thread.cancelled
        }
        write_watches = {
            socket
            for socket in write_watches
            if socket.fileno() >= 0 and not socket.thread.cancelled
        }
        error_watches = {
            socket
            for socket in error_watches
            if socket.fileno() >= 0 and not socket.thread.cancelled
        }
        # Wait for any of the sockets to become ready, or until the next timer expires
        if read_watches or write_watches or error_watches or wakeup_date:
            try:
                timeout = (
                    max(
                        (wakeup_date - datetime.now()).total_seconds(),
                        0,
                    )
                    if wakeup_date
                    else None
                )
                # prune negative filenos
                (
                    read_sockets,
                    write_sockets,
                    error_sockets,
                ) = select.select(
                    read_watches,
                    write_watches,
                    error_watches,
                    timeout,
                )
                for socket in read_sockets:
                    task_queue.append((socket.thread, socket))
                    read_watches.remove(socket)
                for socket in write_sockets:
                    task_queue.append((socket.thread, socket))
                    write_watches.remove(socket)
                for socket in error_sockets:
                    task_queue.append((socket.thread, socket))
                    error_watches.remove(socket)
                for i, (time, thread) in enumerate(timers):
                    if datetime.now() >= time:
                        task_queue.append((thread, None))
                        timers.pop(i)
            except InterruptedError:
                continue

        if len(task_queue) == 0:
            # done
            break


async def schedule(
    coroutine: Coroutine[Any, Any, Any],
) -> Task:
    """
    Schedule a new coroutine to be executed by the event loop.

    This is the primary way to create new concurrent tasks within the event loop.
    The scheduled coroutine will run concurrently with the current coroutine.

    Args:
        coroutine: The coroutine to schedule

    Returns:
        A Task object representing the scheduled coroutine
    """
    task = await Schedule(coroutine)
    return task


async def cancel(task: Task):
    """
    Cancel a running task.

    The cancelled task will receive a CancelledError exception, which it can
    catch to perform cleanup operations before terminating.

    Args:
        task: The task to cancel
    """
    await CancelTask(task)


async def sleep(seconds: float):
    """
    Suspend the current coroutine for the specified number of seconds.

    This function yields control back to the event loop and resumes execution
    after the specified time has elapsed.

    Args:
        seconds: The number of seconds to sleep
    """
    await Timeout(seconds)


async def recv(socket: socket.socket, count: int) -> bytes:
    """
    Receive data from a socket asynchronously.

    This function suspends the current coroutine until data is available
    to be read from the socket.

    Args:
        socket: The socket to receive data from
        count: The maximum number of bytes to receive

    Returns:
        The received data as bytes
    """
    await Readable(socket)
    return socket.recv(count)


async def send(socket: socket.socket, data: bytes) -> int:
    """
    Send data to a socket asynchronously.

    This function suspends the current coroutine until the socket is ready
    to accept data for writing.

    Args:
        socket: The socket to send data to
        data: The data to send

    Returns:
        The number of bytes sent
    """
    await Writable(socket)
    return socket.send(data)


async def connect(host: str, port: int) -> socket.socket:
    """
    Create and connect a socket to the specified host and port asynchronously.

    This function creates a non-blocking socket, initiates a connection,
    and waits for the connection to complete without blocking the event loop.

    Args:
        host: The host to connect to
        port: The port to connect to

    Returns:
        The connected socket

    Raises:
        ConnectionError: If the connection fails
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)

    try:
        sock.connect((host, port))
    except BlockingIOError:
        # Expected, the connection is in progress
        pass

    # Wait for the socket to become writable, which means the connection is complete
    await Writable(sock)

    # Check if the connection succeeded
    error = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
    if error != 0:
        raise ConnectionError(f"Connection failed with error: {error}")

    return sock


async def listen(host: str, port: int, backlog: int = 5) -> socket.socket:
    """
    Create a server socket and start listening for connections asynchronously.

    This function binds a socket to the specified host and port, and puts it
    in listening mode to accept incoming connections.

    Args:
        host: The host to bind to
        port: The port to bind to
        backlog: The maximum number of queued connections

    Returns:
        The server socket
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.setblocking(False)
    server_sock.bind((host, port))
    server_sock.listen(backlog)
    await Readable(server_sock)
    return server_sock


async def accept(
    server_sock: socket.socket,
) -> tuple[socket.socket, tuple[str, int]]:
    """
    Accept a connection on the server socket asynchronously.

    This function suspends the current coroutine until a new connection is
    available on the server socket.

    Args:
        server_sock: The server socket to accept connections on

    Returns:
        A tuple containing the client socket and the client address
    """
    await Readable(server_sock)
    client_sock, addr = server_sock.accept()
    client_sock.setblocking(False)
    return client_sock, addr


if __name__ == "__main__":  # noqa: C901
    """
    Demo application that showcases the event loop functionality.

    This section contains example implementations of:
    1. An echo server that handles multiple concurrent clients
    2. A client that sends messages to the server
    3. Demonstrations of sleep, socket operations, and task cancellation
    """
    server_sock = None

    async def echo_handler(client_sock: socket.socket, addr: tuple[str, int]):
        """
        Handle a client connection by echoing received data.

        This coroutine receives data from a client socket and sends it back.
        It demonstrates basic socket I/O operations.

        Args:
            client_sock: The client socket to handle
            addr: The client's address (host, port)
        """
        print(f"New connection from {addr[0]}:{addr[1]}")

        try:
            while True:
                data = await recv(client_sock, 1024)
                if not data:
                    break

                print(f"Received from {addr[0]}:{addr[1]}: {data.decode().strip()}")
                await send(client_sock, data)
        except Exception as e:
            print(f"Error handling client {addr[0]}:{addr[1]}: {e}")
        finally:
            client_sock.close()
            print(f"Connection closed from {addr[0]}:{addr[1]}")

    async def server(host: str, port: int):
        """
        Start a server that accepts connections and spawns handlers for each client.

        This coroutine demonstrates how to create a server socket, accept incoming
        connections, and schedule tasks to handle each connection.

        Args:
            host: The host to bind to
            port: The port to bind to
        """
        global server_sock
        server_sock = await listen(host, port)
        print(f"Server listening on {host}:{port}")

        try:
            while True:
                client_sock, addr = await accept(server_sock)
                # Schedule a new task to handle this client
                await schedule(echo_handler(client_sock, addr))
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_sock.close()

    async def client(host: str, port: int, messages: list[str]):
        """
        Connect to a server and send a series of messages.

        This coroutine demonstrates how to create a client socket, send data,
        and receive responses.

        Args:
            host: The host to connect to
            port: The port to connect to
            messages: A list of messages to send to the server
        """
        print(f"Client connecting to {host}:{port}")
        sock = await connect(host, port)
        try:
            for message in messages:
                print(f"Client sending: {message}")
                await send(sock, message.encode())

                response = await recv(sock, 1024)
                print(f"Client received: {response.decode().strip()}")

                # Add a small delay between messages
                await sleep(0.5)

            print("Client finished sending messages")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            sock.close()

    async def demo_sleep():
        """
        Demonstrate basic sleep functionality.

        This coroutine shows how to use sleep to introduce delays and how to
        schedule multiple concurrent tasks.
        """
        print("\n--- Sleep Demo ---")
        print("Start")
        await schedule(sleep_print(1, "One"))
        await schedule(sleep_print(2, "Two"))
        await sleep(3)  # Wait for the scheduled tasks to complete
        print("End sleep demo")

    async def sleep_print(seconds: float, message: str):
        """
        Sleep for the specified duration and then print a message.

        Args:
            seconds: The number of seconds to sleep
            message: The message to print after sleeping
        """
        await sleep(seconds)
        print(message)

    async def demo_socket():
        """
        Demonstrate concurrent socket server and client.

        This coroutine shows how to use the event loop to run a server and client
        concurrently, handling multiple connections simultaneously.
        """
        print("\n--- Socket Demo ---")
        # Schedule the server task
        host, port = "127.0.0.1", 7777
        server_task = await schedule(server(host, port))

        # Give the server a moment to start
        await sleep(0.1)

        # Schedule the client task with some messages
        messages = [
            "Hello from the client!",
            "This is a test message",
            "Goodbye!",
        ]
        await schedule(client(host, port, messages))

        # Wait for the tasks to finish
        await sleep(5)
        server_task.cancel()
        print("Socket demo finished")

    async def demo_cancellation():
        """
        Demonstrate task cancellation.

        This coroutine shows how to schedule a task, let it run for a while,
        and then cancel it. It demonstrates proper error handling for cancellation.
        """
        print("\n--- Cancellation Demo ---")
        print("Starting a long-running task that will be cancelled")

        async def long_running_task():
            """A task that runs indefinitely until cancelled."""
            print("Long-running task started")
            count = 0
            try:
                while True:
                    count += 1
                    print(f"Long-running task iteration {count}")
                    await sleep(1)
            except asyncio.CancelledError:
                print("Task was cancelled!")
                raise
            finally:
                print("Long-running task cleanup")

        # Schedule the long-running task
        task = await schedule(long_running_task())

        # Let it run for a bit
        await sleep(3)

        # Cancel the task
        print("Cancelling the task...")
        await cancel(task)

        # Wait a moment to see the cancellation effect
        await sleep(1)
        print("Cancellation demo finished")

    async def main():
        """
        Run all demos.

        This is the main entry point for the demo application. It runs each demo
        in sequence to showcase different aspects of the event loop.
        """
        print("Starting async-from-scratch demos")

        # Run the basic sleep demo
        await demo_sleep()

        # Run the socket demo
        await demo_socket()

        # Run the cancellation demo
        await demo_cancellation()

        print("\nAll demos completed successfully!")

    # Start the event loop with the main coroutine
    event_loop(main())
