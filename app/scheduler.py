import schedule
import time
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class NewsScheduler:
    """Handle scheduling of news updates."""
    
    def __init__(self):
        self.scheduled_jobs = []
    
    def schedule_daily(self, time_str: str, job_func: Callable) -> None:
        """Schedule a job to run daily at specified time.
        
        Args:
            time_str: Time in HH:MM format (24-hour), e.g., "22:00" for 10:00 PM
            job_func: Function to execute
        """
        try:
            schedule.every().day.at(time_str).do(job_func)
            logger.info(f"Scheduled daily job at {time_str}")
        except Exception as e:
            logger.error(f"Error scheduling job: {e}")
            raise
    
    def schedule_every_hours(self, hours: int, job_func: Callable) -> None:
        """Schedule a job to run every N hours."""
        try:
            schedule.every(hours).hours.do(job_func)
            logger.info(f"Scheduled job every {hours} hours")
        except Exception as e:
            logger.error(f"Error scheduling job: {e}")
            raise
    
    def start(self) -> None:
        """Start the scheduler loop."""
        logger.info("Starting scheduler...")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
    
    def run_once(self) -> None:
        """Run all pending jobs immediately (useful for testing)."""
        logger.info("Running all pending jobs...")
        schedule.run_all()


if __name__ == "__main__":
    print("Scheduler module loaded")
