import subprocess
import sys
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def run_bot():
    while True:
        logging.debug("Starting bot process")
        process = subprocess.Popen([sys.executable, 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        custom_exit_code = None
        
        while True:
            try:
                output = process.stdout.readline()
                if output == b'' and process.poll() is not None:
                    break
                if output:
                    log_line = output.strip().decode('utf-8')
                    logging.debug(log_line)
                    if "Force exiting with code 42" in log_line:
                        custom_exit_code = 42
                    elif "Force exiting with code 0" in log_line:
                        custom_exit_code = 0
            except Exception as e:
                logging.error(f"Error reading subprocess output: {e}")
        
        stderr = process.stderr.read().decode('utf-8')
        if stderr:
            logging.debug(f"STDERR: {stderr}")
        
        return_code = custom_exit_code if custom_exit_code is not None else process.poll()
        logging.debug(f"Bot process exited with code {return_code}")
        
        if return_code == 0:
            logging.info("Bot stopped deliberately. Exiting...")
            break
        elif return_code == 42:
            logging.info("Bot restarting...")
            time.sleep(5)  # Wait for 5 seconds before restarting
        else:
            logging.warning(f"Bot exited with unexpected code {return_code}. Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    logging.debug("Starting disbot.py")
    run_bot()
    logging.debug("disbot.py exiting")