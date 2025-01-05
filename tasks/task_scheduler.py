# task_scheduler.py
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from collections import defaultdict
from .task_base import TaskBase, TaskResult

class TaskScheduler:
    """Advanced task scheduler with monitoring and management capabilities"""
    
    def __init__(self):
        self.logger = logging.getLogger("TaskScheduler")
        self.scheduled_tasks: Dict[str, Dict[str, Any]] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_results: Dict[str, List[TaskResult]] = defaultdict(list)
        self.is_running = False
        self._schedule_lock = asyncio.Lock()
        
    async def schedule_task(
        self,
        task: TaskBase,
        interval: int,
        start_delay: Optional[int] = None,
        max_runs: Optional[int] = None,
        dependencies: Optional[List[str]] = None
    ) -> None:
        """
        Schedule a task with advanced options.
        
        :param task: Task instance to schedule
        :param interval: Interval between executions in seconds
        :param start_delay: Optional delay before first execution
        :param max_runs: Optional maximum number of executions
        :param dependencies: Optional list of task names that must complete before this task
        """
        async with self._schedule_lock:
            if task.name in self.scheduled_tasks:
                raise ValueError(f"Task {task.name} is already scheduled")
            
            self.scheduled_tasks[task.name] = {
                'task': task,
                'interval': interval,
                'last_run': None,
                'next_run': datetime.now() + timedelta(seconds=start_delay or 0),
                'runs_completed': 0,
                'max_runs': max_runs,
                'dependencies': dependencies or [],
                'status': 'scheduled'
            }
            
            self.logger.info(f"Scheduled task {task.name} with interval {interval}s")
            
            if self.is_running:
                await self._start_task(task.name)

    async def start(self) -> None:
        """Start the task scheduler"""
        self.is_running = True
        self.logger.info("Task scheduler started")
        
        try:
            await self._run_scheduler()
        except Exception as e:
            self.logger.error(f"Scheduler error: {str(e)}", exc_info=True)
            raise
        finally:
            self.is_running = False

    async def stop(self) -> None:
        """Stop the task scheduler and all running tasks"""
        self.is_running = False
        self.logger.info("Stopping task scheduler...")
        
        # Cancel all running tasks
        for task_name, task in self.running_tasks.items():
            self.logger.info(f"Cancelling task: {task_name}")
            task.cancel()
            
        # Wait for tasks to complete
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks.values(), return_exceptions=True)
        
        self.running_tasks.clear()
        self.logger.info("Task scheduler stopped")

    async def _run_scheduler(self) -> None:
        """Main scheduler loop"""
        while self.is_running:
            current_time = datetime.now()
            
            # Check and start due tasks
            for task_name, task_info in self.scheduled_tasks.items():
                if task_info['status'] == 'scheduled' and current_time >= task_info['next_run']:
                    if await self._can_run_task(task_name):
                        await self._start_task(task_name)
            
            await asyncio.sleep(1)  # Check every second

    async def _can_run_task(self, task_name: str) -> bool:
        """Check if a task can run based on its dependencies"""
        task_info = self.scheduled_tasks[task_name]
        
        # Check dependencies
        for dep_name in task_info['dependencies']:
            dep_info = self.scheduled_tasks.get(dep_name)
            if not dep_info or dep_info['status'] != 'completed':
                return False
        
        # Check max runs
        if task_info['max_runs'] and task_info['runs_completed'] >= task_info['max_runs']:
            return False
            
        return True

    async def _start_task(self, task_name: str) -> None:
        """Start a task execution"""
        task_info = self.scheduled_tasks[task_name]
        task = task_info['task']
        
        # Create and start task
        run_task = asyncio.create_task(self._run_task(task_name))
        self.running_tasks[task_name] = run_task
        
        # Update task info
        task_info['status'] = 'running'
        task_info['last_run'] = datetime.now()
        task_info['next_run'] = datetime.now() + timedelta(seconds=task_info['interval'])

    async def _run_task(self, task_name: str) -> None:
        """Execute a task and handle its completion"""
        task_info = self.scheduled_tasks[task_name]
        task = task_info['task']
        
        try:
            result = await task.run()
            self.task_results[task_name].append(result)
            
            # Update task info
            task_info['runs_completed'] += 1
            task_info['status'] = 'completed'
            
            if result.success:
                self.logger.info(f"Task {task_name} completed successfully")
            else:
                self.logger.warning(f"Task {task_name} completed with errors: {result.message}")
                
        except Exception as e:
            self.logger.error(f"Error running task {task_name}: {str(e)}", exc_info=True)
            task_info['status'] = 'failed'
        
        finally:
            self.running_tasks.pop(task_name, None)

    def get_task_status(self, task_name: str) -> Dict[str, Any]:
        """Get detailed status of a task"""
        if task_name not in self.scheduled_tasks:
            raise ValueError(f"Task {task_name} not found")
            
        task_info = self.scheduled_tasks[task_name]
        results = self.task_results[task_name]
        
        return {
            'name': task_name,
            'status': task_info['status'],
            'last_run': task_info['last_run'],
            'next_run': task_info['next_run'],
            'runs_completed': task_info['runs_completed'],
            'success_rate': len([r for r in results if r.success]) / len(results) if results else 0,
            'average_execution_time': sum(r.execution_time for r in results) / len(results) if results else 0,
            'dependencies': task_info['dependencies']
        }

    def get_all_task_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all tasks"""
        return {
            task_name: self.get_task_status(task_name)
            for task_name in self.scheduled_tasks
        }
