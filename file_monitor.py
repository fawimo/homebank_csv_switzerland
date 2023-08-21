# This is the main file for the creation of HomeBank (http://homebank.free.fr) CSV compatible file from Swiss Bank Statements 

# Import libraries
from shared import *

# File processing

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Only handle files, not directories
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            if "kto_ausz" in file_name:
                subprocess.run([sys.executable, 'bas.py'])
            elif "account_statements" in file_name:
                subprocess.run([sys.executable, 'neon.py'])
            elif "statement_1815638" in file_name:
                subprocess.run([sys.executable, 'wise.py'])
            elif "Sumup" in file_name:
                subprocess.run([sys.executable, 'sumup.py'])
            elif "Transaction" in file_name:
                subprocess.run([sys.executable, 'reka.py'])
            elif "AccountStatement" in file_name:
                subprocess.run([sys.executable, 'yuh.py'])
            elif "Account" in file_name:
                subprocess.run([sys.executable, 'degiro.py'])



if __name__ == "__main__":
    # Replace '/home/fabien/Statements' with the path to the folder you want to monitor
    folder_path = '/home/fabien/Statements'
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()