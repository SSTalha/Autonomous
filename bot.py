import json
import logging
from datetime import datetime, timezone
from facebook_actions import FacebookBot
import config
import os
import time

def process_tasks(tasks_file: str = 'tasks.json'):
    """Process tasks from JSON file"""
    # Initialize Facebook Bot
    bot = FacebookBot()
    
    try:
        # Login to Facebook
        bot.login(config.FB_USERNAME, config.FB_PASSWORD)
        time.sleep(5)

        # Check if the file exists
        if not os.path.exists(tasks_file):
            bot.logger.error(f"File not found: {tasks_file}")
            return

        # Read tasks from JSON file
        with open(tasks_file, 'r') as f:
            tasks = json.load(f)

        # Process each task
        for task in tasks:
            try:
                # Validate platform
                if task['platform'] != 'facebook':
                    bot.logger.warning(f"Skipping non-Facebook task: {task['message_id']}")
                    continue

                # Navigate to the post
                #Construct post url here using post_id
                bot.navigate_to_post(task['target']['page_url'])

                # Perform action based on type
                if task['action_type'] == 'comment':
                    bot.comment_on_post(task['content']['text'])
                    time.sleep(2)
                
                elif task['action_type'] == 'reply':
                    # Perform reply
                    # Construct XPath based on parent_comment_id
                    bot.reply_to_comment(
                        task['content']['text'], 
                        task['target']['parent_comment_id']
                    )
                    time.sleep(2)

                # Log successful task completion
                bot.logger.info(f"Successfully processed task: {task['message_id']}")
                time.sleep(5)

            except Exception as task_error:
                bot.logger.error(f"Error processing task {task['message_id']}: {task_error}")

    except Exception as e:
        bot.logger.error(f"Bot execution failed: {e}")
    finally:
        # Always close the browser
        bot.close()

def main():
    # Configure logging
    logging.basicConfig(
        filename=config.LOG_FILE, 
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

    # Process tasks from JSON file
    process_tasks()

if __name__ == "__main__":
    main()
