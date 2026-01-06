"""
Utilities - Parallelism.

This module provides utilities for parallel execution of tasks.
"""

from collections.abc import Callable
from concurrent.futures import (
    Executor,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
)


def do_tasks_in_parallel(
    task_func: Callable,
    task_pool: list,
    max_threads: int = 5,
    type_of: str = "thread",
) -> list:
    """
    Execute a list of tasks in parallel using multithreading or multiprocessing.

    This function aims to provide a simple interface for executing tasks concurrently,
    improving performance for I/O-bound operations.

    ---

    Args:
        task_pool (list): A list of tasks to be executed.
        task_func (Callable): The function to be executed for each task.
        max_threads (int): The maximum number of threads to use.
        type_of (str): The type of parallel execution to use ("thread" or "process").

    Returns:
        list: A list of results from the executed tasks.

    """

    if type_of not in ["thread", "process"]:
        raise ValueError("Invalid type_of. Expected 'thread' or 'process'.")

    # Select the parallel execution strategy
    parallel_executor: type[Executor] = ThreadPoolExecutor

    if type_of == "process":
        parallel_executor = ProcessPoolExecutor

    # Execute the tasks in parallel
    with parallel_executor(max_workers=max_threads) as executor:  # type: ignore[call-arg]
        futures = []

        for sample in task_pool:
            if isinstance(sample, tuple | list):
                futures.append(executor.submit(task_func, *sample))

            elif isinstance(sample, dict):
                futures.append(executor.submit(task_func, **sample))

            else:
                futures.append(executor.submit(task_func, sample))

        return [future.result() for future in as_completed(futures)]
