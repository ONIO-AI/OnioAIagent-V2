# task_base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass, field

@dataclass
class TaskResult:
    """Data class for storing task execution results"""
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Exception] = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class TaskBase(ABC):
    """Base class for all tasks with enhanced functionality"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"Task.{name}")
        self.execution_history: List[TaskResult] = []
        self.last_execution: Optional[TaskResult] = None
        self.retry_count = 0
        self.max_retries = self.config.get('max_retries', 3)
        self.is_running = False
        
    @abstractmethod
    async def execute(self) -> TaskResult:
        """
        Abstract method that must be implemented by concrete task classes.
        :return: TaskResult containing execution results
        """
        raise NotImplementedError("Subclasses must implement execute()")

    async def run(self) -> TaskResult:
        """
        Main task execution method with error handling and metrics collection.
        :return: TaskResult containing execution results
        """
        if self.is_running:
            return TaskResult(
                success=False,
                message=f"Task {self.name} is already running",
                error=RuntimeError("Task already running")
            )

        start_time = datetime.now()
        self.is_running = True
        
        try:
            self.logger.info(f"Starting task: {self.name}")
            result = await self.execute()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result.execution_time = execution_time
            result.timestamp = datetime.now()
            
            self._update_history(result)
            self.logger.info(f"Task {self.name} completed in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in task {self.name}: {str(e)}", exc_info=True)
            result = TaskResult(
                success=False,
                message=f"Task failed: {str(e)}",
                error=e,
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            self._update_history(result)
            
            if await self._handle_retry():
                return await self.run()
            return result
            
        finally:
            self.is_running = False

    async def _handle_retry(self) -> bool:
        """Handle task retry logic"""
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.logger.info(f"Retrying task {self.name} ({self.retry_count}/{self.max_retries})")
            await self._wait_before_retry()
            return True
        return False

    async def _wait_before_retry(self) -> None:
        """Calculate and wait before retry with exponential backoff"""
        import asyncio
        wait_time = min(300, 2 ** (self.retry_count - 1) * 5)  # Max 5 minutes
        self.logger.info(f"Waiting {wait_time}s before retry")
        await asyncio.sleep(wait_time)

    def _update_history(self, result: TaskResult) -> None:
        """Update task execution history"""
        self.last_execution = result
        self.execution_history.append(result)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get task execution metrics"""
        successful_runs = len([r for r in self.execution_history if r.success])
        total_runs = len(self.execution_history)
        
        return {
            'name': self.name,
            'total_executions': total_runs,
            'successful_executions': successful_runs,
            'success_rate': successful_runs / total_runs if total_runs > 0 else 0,
            'average_execution_time': sum(r.execution_time for r in self.execution_history) / total_runs if total_runs > 0 else 0,
            'last_execution': self.last_execution.timestamp if self.last_execution else None,
            'is_running': self.is_running,
            'retry_count': self.retry_count
        }

    def reset_metrics(self) -> None:
        """Reset task metrics and history"""
        self.execution_history.clear()
        self.last_execution = None
        self.retry_count = 0

    def validate_config(self) -> bool:
        """
        Validate task configuration.
        Override in subclasses for specific validation.
        """
        return True
