import os
from dotenv import load_dotenv
from preprocessing import process_resumes_data
from apscheduler.schedulers.background import BackgroundScheduler 

# Load environment variables from the .env file in the current directory
load_dotenv()

# Get values of environment variables and assign them to respective variables
username: str = os.environ['USERNAME']
password: str = os.environ['USER_PASSWORD']
sharepoint_url: str = os.environ['SHAREPOINT_URL']

# Create an instance of the BackgroundScheduler
scheduler = BackgroundScheduler()

# Add a job to the scheduler with the process_resumes_data function and its arguments
# The job will be triggered at regular intervals (every 1 day in this case)
scheduler.add_job(process_resumes_data,'interval', days=1, args=(username, password, sharepoint_url))

# Start the scheduler when the script is executed
if __name__ == '__main__':
    scheduler.start()

    try:
        # Keep the script running so the scheduled jobs can execute in the background
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Shut down the scheduler gracefully if the script is interrupted or exited
        scheduler.shutdown()
