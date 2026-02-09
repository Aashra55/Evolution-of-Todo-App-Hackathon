import asyncio
import json
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional
import uuid
import logging

# Mock Dapr Client for local development/testing
class MockDaprClient:
    def __init__(self):
        self.pubsub = self.MockPubSub()

    class MockPubSub:
        async def publish(self, pubsub_name, topic_name, data):
            logger.info(f"MockDaprClient: Publishing to topic '{topic_name}' on pubsub '{pubsub_name}' with data: {data[:100]}...")
            await asyncio.sleep(0.01)

dapr_client = MockDaprClient()

# --- Mock Database/Storage Access ---
# In a real application, this would interact with a database (e.g., PostgreSQL)
# to fetch recurring task definitions and create new task instances.
MOCK_RECURRING_TASKS_DB = {
    "task_def_1": {
        "id": "task_def_1",
        "title": "Weekly Report",
        "description": "Generate weekly status report.",
        "recurrencePattern": {"type": "weekly", "interval": 1, "daysOfWeek": ["MON"], "endDate": None},
        "userId": "mock-user-123",
        # nextOccurrence should be a datetime string in ISO format
        "nextOccurrence": (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z" 
    },
    "task_def_2": {
        "id": "task_def_2",
        "title": "Monthly Billing",
        "description": "Process monthly invoices.",
        "recurrencePattern": {"type": "monthly", "dayOfMonth": 15, "interval": 1},
        "userId": "mock-user-456",
        # Ensure nextOccurrence is a string for consistency
        "nextOccurrence": datetime(datetime.utcnow().year, datetime.utcnow().month, 15, 9, 0, 0).isoformat() + "Z" if datetime.utcnow().day <= 15 else datetime(datetime.utcnow().year, datetime.utcnow().month + 1 if datetime.utcnow().month < 12 else 1, 15, 9, 0, 0).isoformat() + "Z"
    },
    "task_def_3": {
        "id": "task_def_3",
        "title": "Daily Standup Prep",
        "recurrencePattern": {"type": "daily", "interval": 1},
        "userId": "mock-user-123",
        "nextOccurrence": (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    },
    "task_def_4": {
        "id": "task_def_4",
        "title": "Yearly Review",
        "recurrencePattern": {"type": "yearly", "month": 7, "dayOfMonth": 1, "interval": 1}, # Example: July 1st every year
        "userId": "mock-user-789",
        "nextOccurrence": datetime(datetime.utcnow().year + 1, 7, 1).isoformat() + "Z" # Next year's July 1st
    }
}

async def get_recurring_task_definitions():
    """Simulates fetching all recurring task definitions from storage."""
    logger.info("MockDB: Fetching all recurring task definitions.")
    return list(MOCK_RECURRING_TASKS_DB.values())

async def create_new_task_instance(task_data: Dict[str, Any]):
    """Simulates creating a new task instance in the database from a recurring pattern."""
    task_id = str(uuid.uuid4())
    # Ensure complex types are JSON serialized if stored as JSON in DB
    if 'reminderSettings' in task_data and isinstance(task_data['reminderSettings'], dict):
        task_data['reminderSettings'] = json.dumps(task_data['reminderSettings'])
    if 'recurrencePattern' in task_data and isinstance(task_data['recurrencePattern'], dict):
        task_data['recurrencePattern'] = json.dumps(task_data['recurrencePattern'])

    new_task_instance = {
        "id": task_id,
        "title": task_data.get('title', 'Generated Recurring Task'),
        "description": task_data.get('description', 'Generated from recurring task definition'),
        "status": "pending",
        "priority": task_data.get('priority', 'medium'),
        "tags": task_data.get('tags'),
        "dueDate": task_data.get('dueDate'),
        "reminderSettings": task_data.get('reminderSettings'),
        "recurrencePattern": task_data.get('recurrencePattern'),
        "userId": task_data.get('userId'),
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "updatedAt": datetime.utcnow().isoformat() + "Z",
        "generatedFromRecurringTaskId": task_data.get("recurringTaskId") 
    }
    logger.info(f"MockDB: Created task instance: {new_task_instance['title']} (ID: {task_id})")
    return new_task_instance

async def update_recurring_task_occurrence(task_def_id: str, new_next_occurrence: datetime):
    """Simulates updating the next occurrence date for a recurring task definition."""
    if task_def_id in MOCK_RECURRING_TASKS_DB:
        MOCK_RECURRING_TASKS_DB[task_def_id]["nextOccurrence"] = new_next_occurrence.isoformat() + "Z"
        logger.info(f"MockDB: Updated next occurrence for {task_def_id} to {new_next_occurrence.isoformat()}")
    else:
        logger.warning(f"MockDB Warning: Recurring task definition {task_def_id} not found for update.")


# --- Recurrence Calculation Logic ---

def calculate_next_occurrence(pattern: Dict[str, Any], current_date: datetime) -> Optional[datetime]:
    """
    Calculates the next occurrence date based on the recurrence pattern.
    Handles daily, weekly, monthly, yearly types.
    """
    rtype = pattern.get("type")
    interval = pattern.get("interval", 1)
    
    next_date = current_date 
    
    if rtype == "daily":
        next_date += timedelta(days=interval)
    elif rtype == "weekly":
        days_of_week = pattern.get("daysOfWeek", ["MON"]) # Default to Monday if not specified
        # Find the next desired day of week within the next interval weeks
        for i in range(interval * 7): # Check up to interval weeks ahead
            potential_date = current_date + timedelta(days=i)
            if potential_date.strftime('%a').upper() in days_of_week:
                next_date = potential_date
                break
        # Ensure we advance by the correct interval if multiple days fall within the first week
        if next_date <= current_date: # If the calculated day was today or in the past, advance by interval
            next_date += timedelta(weeks=interval)
    elif rtype == "monthly":
        day_of_month = pattern.get("dayOfMonth", current_date.day)
        try:
            year = current_date.year
            month = current_date.month + interval
            if month > 12:
                month -= 12
                year += 1
            
            # Ensure the day exists in the target month
            next_date = datetime(year, month, day_of_month, current_date.hour, current_date.minute, current_date.second)
        except ValueError: # Handle cases like day 31 in February or invalid days
            logger.warning(f"Could not set day {day_of_month} for month {month}/{year}. Adjusting month.")
            # Fallback: Advance by interval and try to use the original day, clamp to last day of month if invalid
            month = current_date.month + interval
            year = current_date.year
            if month > 12:
                month -= 12
                year += 1
            
            # Try to find the last day of the month if the original day is invalid
            last_day_of_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else (datetime(year + 1, 1, 1) - timedelta(days=1)).day
            actual_day = min(day_of_month, last_day_of_month)
            next_date = datetime(year, month, actual_day, current_date.hour, current_date.minute, current_date.second)

    elif rtype == "yearly":
        month = pattern.get("month", current_date.month)
        day_of_month = pattern.get("dayOfMonth", current_date.day)
        year = current_date.year + interval
        try:
            next_date = datetime(year, month, day_of_month, current_date.hour, current_date.minute, current_date.second)
        except ValueError:
            logger.warning(f"Could not set date {month}/{day_of_month}/{year}. Adjusting.")
            # Fallback for yearly dates (e.g., Feb 29 in non-leap year)
            last_day_of_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else (datetime(year + 1, 1, 1) - timedelta(days=1)).day
            actual_day = min(day_of_month, last_day_of_month)
            next_date = datetime(year, month, actual_day, current_date.hour, current_date.minute, current_date.second)

    else:
        logger.warning(f"Unsupported recurrence type: {rtype}")
        return None

    # Check against endDate
    end_date_str = pattern.get("endDate")
    if end_date_str:
        try:
            # Ensure end_date is timezone-aware if next_date is, or parse carefully
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            if next_date > end_date:
                return None # Recurrence has ended

        except ValueError:
            logger.error(f"Invalid endDate format: {end_date_str}")

    return next_date

async def generate_recurring_tasks_job():
    """
    Job to find recurring tasks and generate new instances.
    This function is intended to be triggered periodically (e.g., by Dapr Scheduled Jobs).
    """
    logger.info("Running job to generate recurring tasks...")
    
    recurring_tasks = await get_recurring_task_definitions()
    now = datetime.utcnow()
    generated_count = 0

    for task_def in recurring_tasks:
        task_def_id = task_def["id"]
        pattern = task_def.get("recurrencePattern")
        if not pattern:
            logger.warning(f"Skipping task definition {task_def_id}: No recurrence pattern found.")
            continue

        next_occurrence_str = task_def.get("nextOccurrence")
        
        reference_date = now
        if next_occurrence_str:
            try:
                # Parse the next occurrence date, ensuring it's timezone-aware for comparisons
                reference_date = datetime.fromisoformat(next_occurrence_str.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid nextOccurrence format for {task_def_id}: {next_occurrence_str}")
                continue

        calculated_next_occurrence = calculate_next_occurrence(pattern, reference_date)
        
        # Generate if the next occurrence is today or in the near future (e.g., within next 24 hours)
        # to ensure timely task creation. Adjust window as needed.
        if calculated_next_occurrence and calculated_next_occurrence <= now + timedelta(days=1): 
            logger.info(f"Found recurring task '{task_def.get('title')}' ({task_def_id}) due for generation around {calculated_next_occurrence.isoformat()}")
            
            try:
                new_task_data = {
                    "title": task_def["title"],
                    "description": task_def.get("description"),
                    "priority": task_def.get("priority"),
                    "tags": task_def.get("tags"),
                    "dueDate": calculated_next_occurrence, # Set due date based on next occurrence
                    "userId": task_def["userId"],
                    "recurrencePattern": pattern # Include pattern for potential future processing
                }
                
                # Simulate creating a new task instance in the database
                # In reality, this would call an actual service function like create_task_in_db
                new_task_instance = await create_new_task_instance(new_task_data)
                logger.info(f"Generated task instance: {new_task_instance['title']} (ID: {new_task_instance['id']})")

                # Publish an event indicating a new task was generated
                event_payload = {
                    "eventType": "RecurringTaskGenerated",
                    "sourceService": "recurring-task-service",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "userId": task_def["userId"],
                    "payload": new_task_instance, # Include data of the generated task
                    "correlationId": str(uuid.uuid4())
                }
                await dapr_client.pubsub.publish(
                    pubsub_name="pubsub",
                    topic_name="task-events", # Publish to task-events topic
                    data=json.dumps(event_payload)
                )
                logger.info(f"Published event: RecurringTaskGenerated for '{task_def['title']}'")
                
                # Calculate the *next* next occurrence date for this recurring task definition
                next_next_occurrence = calculate_next_occurrence(pattern, calculated_next_occurrence)
                if next_next_occurrence:
                    await update_recurring_task_occurrence(task_def_id, next_next_occurrence)
                else:
                    logger.info(f"Recurrence for task definition {task_def_id} has ended.")
                    # Optionally, mark the task definition as inactive or remove it

                generated_count += 1
                
            except Exception as e:
                logger.error(f"Error generating task for recurring task '{task_def.get('title')}': {e}", exc_info=True)
                # Implement retry logic or error handling as needed

    logger.info(f"Recurring Task Job finished. Generated {generated_count} new task instances.")

async def check_and_generate_tasks():
    """
    This function would be called by Dapr Scheduled Jobs or periodically.
    It orchestrates the process of checking recurring tasks and generating new ones.
    """
    logger.info("Initiating check_and_generate_tasks...")
    await generate_recurring_tasks_job()
    logger.info("check_and_generate_tasks completed.")

# --- Main application setup ---
# This FastAPI app will primarily expose endpoints for Dapr to call for scheduled jobs.
# Actual job scheduling is managed by Dapr's Dapr Scheduled Jobs component.

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001)) # Use a different port
    logger.info(f"Starting Recurring Task Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)