import concurrent.futures
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from swarms.structs.base import BaseStructure
from swarms.structs.task import Task


@dataclass
class ConcurrentWorkflow(BaseStructure):
    """
    ConcurrentWorkflow class for running a set of tasks concurrently using N number of autonomous agents.

    Args:
        max_workers (int): The maximum number of workers to use for the ThreadPoolExecutor.
        autosave (bool): Whether to save the state of the workflow to a file. Default is False.
        saved_state_filepath (str): The filepath to save the state of the workflow to. Default is "runs/concurrent_workflow.json".
        print_results (bool): Whether to print the results of each task. Default is False.
        return_results (bool): Whether to return the results of each task. Default is False.
        use_processes (bool): Whether to use processes instead of threads. Default is False.

    Examples:
    >>> from swarms.models import OpenAIChat
    >>> from swarms.structs import ConcurrentWorkflow
    >>> llm = OpenAIChat(openai_api_key="")
    >>> workflow = ConcurrentWorkflow(max_workers=5)
    >>> workflow.add("What's the weather in miami", llm)
    >>> workflow.add("Create a report on these metrics", llm)
    >>> workflow.run()
    >>> workflow.tasks
    """

    task_pool: List[Dict] = field(default_factory=list)
    max_workers: int = 5
    autosave: bool = False
    saved_state_filepath: Optional[str] = (
        "runs/concurrent_workflow.json"
    )
    print_results: bool = False
    return_results: bool = False
    use_processes: bool = False

    def add(self, task: Task = None, tasks: List[Task] = None):
        """Adds a task to the workflow.

        Args:
            task (Task): _description_
            tasks (List[Task]): _description_
        """
        try:
            if tasks:
                for task in tasks:
                    self.task_pool.append(task)
            else:
                if task:
                    self.task_pool.append(task)
        except Exception as error:
            print(f"[ERROR][ConcurrentWorkflow] {error}")
            raise error

    def run(self):
        """
        Executes the tasks in parallel using a ThreadPoolExecutor.

        Args:
            print_results (bool): Whether to print the results of each task. Default is False.
            return_results (bool): Whether to return the results of each task. Default is False.

        Returns:
            List[Any]: A list of the results of each task, if return_results is True. Otherwise, returns None.
        """
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {
                executor.submit(task.execute): task
                for task in self.task_pool
            }
            results = []

            for future in concurrent.futures.as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    if self.print_results:
                        print(f"Task {task}: {result}")
                    if self.return_results:
                        results.append(result)
                except Exception as e:
                    print(f"Task {task} generated an exception: {e}")

        return results if self.return_results else None
