"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple thread pool library to execute commands in a multithreaded
#  environment
#
#  The thread pool lib supports a timeout mechanism when executing the
#  commands. Specify the timeout value in seconds when creating the thread
#  pool. If the execution time of the command exceeds the timeout value,
#  a timout exception will occur and the command will be retried.
#  The number of retries can also be specified when creating the thread pool.
#  If the command wasn't successful after the specified number of retries,
#  the command will be considered as failed. In this case, a message
#  '##FAILURE##' will be put into the output queue and the item will be put
#  back into the input queue. If the command was successful, the result of
#  the command will be put into the output queue.
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import atexit
import ctypes
import queue
import threading

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  CLASS DEFINITIONS
# -------------------------------------------------------------
# pylint too-few-public-methods
class ThreadPoolFunction:
    """
    This class represents a function that can be executed by a thread pool.

    Methods
    -------
    callableFunction(outputQueue, item)
        This function will be called from the thread pool in order to execute
        a specific command. The command is provided in the item parameter
        and is application specific. After processing the command, the result
        of the command can be put into the outputQueue.

    Attributes
    ----------
    None
    """

    def callable_function(self, output_queue, item) -> int:
        """
        This function will be called from the thread pool in order to execute
        a specific command. The command is provided in the item parameter
        and is application specific. After processing the command, the result
        of the command can be put into the output_queue.

        Parameters
        ----------
        output_queue : queue.Queue
            The queue to put the result of the task.
        item : object
            The data item for the task.

        Returns
        -------
        int
            The return code of the task.
            Return 0 if successful, otherwise any other value.
        """
        raise NotImplementedError


class ThreadPool:
    """
    A thread pool implementation for executing tasks concurrently.

    This class manages a pool of threads that can execute tasks in parallel.
    It provides a convenient way to distribute work across multiple threads
    and process the results asynchronously.

    Attributes:
        thread_pool (list): A list of threads in the thread pool.
        input_queue (Queue): The input queue for receiving tasks.
        output_queue (Queue): The output queue for storing results.

    Args:
        num_of_threads (int): The number of threads in the thread pool.
        input_queue (Queue, optional): The input queue to use. If not provided,
            a new queue will be created.
        output_queue (Queue, optional): The output queue to use. If not
            provided, a new queue will be created.
        callable_function (ThreadPoolFunction, optional): The callable object
            that will be invoked to process tasks. If not provided, a default
            ThreadPoolFunction object will be used.
        timeout (int, optional): The timeout in seconds for the input queue.
            If not provided, a default timeout of 5 seconds will be used.
        num_of_retries (int, optional): The number of retries for the input
            queue. If not provided, a default number of 3 retries will be used.
    Methods:
        stop_threads: Stops all the threads in the thread pool.
        callback: The callback function that is executed by each thread.

    """

    # -------------------------------------------------------------
    # VARIABLE DEFINTIONS
    # -------------------------------------------------------------
    thread_list = []
    input_queue = None
    output_queue = None
    timeout = 5
    num_of_retries = 3
    thread_pool_function = None

    # -------------------------------------------------------------
    # INIT METHOD DEFINITION
    # -------------------------------------------------------------
    def __init__(
        self,
        num_of_threads=5,
        thread_pool_function=None,
        timeout=5,
        num_of_retries=3,
    ):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()

        self.thread_pool_function = (
            thread_pool_function
            if thread_pool_function is not None
            else ThreadPoolFunction()
        )
        self.num_of_threads = (
            num_of_threads if num_of_threads is not None else 5
        )
        self.timeout = timeout if timeout is not None else 5
        self.num_of_retries = (
            num_of_retries if num_of_retries is not None else 3
        )
        # create worker threads
        for i in range(num_of_threads):
            thread = threading.Thread(
                target=self.callback,
                args=(
                    i,
                    self.input_queue,
                    self.output_queue,
                    self.thread_pool_function,
                ),
                daemon=True,
            )
            thread.start()
            self.thread_list.append(thread)
        # register atexit function
        atexit.register(self.stop_threads)

    # -------------------------------------------------------------
    # STOP THREADS METHOD DEFINITION
    # -------------------------------------------------------------
    def stop_threads(self):
        """
        Stops all the threads in the thread pool by putting a stop signal
        in the input queue.
        """
        for _ in range(len(self.thread_list)):
            self.input_queue.put("##STOP##")

    # -------------------------------------------------------------
    # CALLBACK METHOD DEFINITION
    # -------------------------------------------------------------
    def callback(
        self,
        thread_num,
        input_queue,
        output_queue,
        thread_pool_function,
    ):
        """
        Executes the callback function for each item in the input queue.

        Args:
            thread_num (int): The number of the thread.
            input_queue (Queue): The input queue containing the items to
                process.
            output_queue (Queue): The output queue to store the results.
            thread_pool_function (ThreadPoolFunction): The thread pool
                function object.

        Returns:
            None
        """
        for item in iter(input_queue.get, "##STOP##"):
            # init variables
            result = 0
            # retry until successful or max retries reached
            for _ in range(self.num_of_retries):
                with TimerThread(
                    self.timeout, threading.get_ident()
                ):
                    try:
                        result = (
                            thread_pool_function.callable_function(
                                output_queue, item
                            )
                        )
                    except RuntimeError:
                        # Log the timeout message instead of printing
                        print(f"##TIMEOUT## - {thread_num} - {item}")
                        result = 1
                # check if the task was successful
                if result in (None, 0):
                    break

            # if not successful, put an item into the output queue
            if result not in (None, 0):
                # Log the failure message instead of printing
                print(f"##FAILURE## - {item}")
                output_queue.put(("##FAILURE##", item))

            # signal that the task is done
            input_queue.task_done()

    # -------------------------------------------------------------
    # GET INPUT QUEUE METHOD DEFINITION
    # -------------------------------------------------------------
    def get_input_queue(self):
        """
        Returns the input queue of the thread pool.

        Returns:
            The input queue of the thread pool.
        """
        return self.input_queue

    # -------------------------------------------------------------
    # GET OUTPUT QUEUE METHOD DEFINITION
    # -------------------------------------------------------------
    def get_output_queue(self):
        """
        Returns the output queue of the thread pool.

        Returns:
            The output queue of the thread pool.
        """
        return self.output_queue


class TimerThread:
    """
    A class representing a timer thread that raises a RuntimeError in the
    thread with the specified thread_id to terminate it after a specified
    timeout.
    """

    timeout = None
    thread_id = None
    timer = None

    def __init__(self, timeout, thread_id):
        """
        Initializes a TimerThread object with the specified timeout and
        thread_id.

        Args:
            timeout (float): The timeout value in seconds.
            thread_id (int): The ID of the thread to terminate.
        """
        self.timeout = timeout
        self.thread_id = thread_id
        self.timer = threading.Timer(
            interval=self.timeout,
            function=self.timeout_thread,
            args=[],
        )

    def __enter__(self):
        """
        Starts the timer thread.
        """
        self.timer.start()

    def __exit__(self, _type, _value, _traceback):
        """
        Cancels the timer thread.
        """
        self.timer.cancel()

    def timeout_thread(self):
        """
        Raises a RuntimeError in the thread with the specified thread_id to
        terminate it.
        """
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.thread_id),
            ctypes.py_object(RuntimeError),
        )
