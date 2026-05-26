import concurrent.futures
import logging

logger = logging.getLogger(__name__)

# Initialize a ThreadPoolExecutor with 4 worker threads to handle background operations
# (e.g. SMTP email sending,Twilio SMS api requests, and Web Push notifications)
# in parallel without blocking the main Django request-response execution.
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def delay_task(func, *args, **kwargs):
    """
    Submits a function to be executed asynchronously in the background thread pool.
    This mimics a background task queue (like Celery/Huey) in-memory without blocking
    the main HTTP thread.
    """
    try:
        _executor.submit(func, *args, **kwargs)
    except Exception as e:
        logger.error(f"Failed to submit background task to thread pool: {e}", exc_info=True)
