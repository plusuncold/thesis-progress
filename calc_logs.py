import time
import subprocess
import sys
import plot_graphs as pg
from datetime import datetime
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler  
from threading import Thread

PAGE_COUNT_LOG_FILE_NAME="page_count.csv"
STATUS_LOG_FILE_NAME="state.csv"
THESIS_PATTERN='*/thesis.pdf'
STATE_FILE_PATTERN='*/thesis_plan.org'
DELTA_TIMES_NEW_ENTRY=65
SLEEP_TIME_FROM_MODIFY=15

# Org csv line output style
# YYYY-MM-DD-HHMM,TODO,STARTED,FIRST_DRAFT,SECOND_DRAFT,REVISIONS_DONE,COMPLETE
# TODO: Yet to be started, STARTED: The first draft not yet complete, FIRST_DRAFT: First draft complete
# SECOND_DRAFT: Second draft complete, REVISIONS_DONE: Revisions made and accepted, COMPLETE: Proofreading, etc complete
STATUSES = [ "TODO", "STARTED", "FIRST_DRAFT", "SECOND_DRAFT", "REVISIONS_DONE", "COMPLETE" ]

# Globals
previous_time = ''

class PDFChangeWatcher(PatternMatchingEventHandler):
    patterns = [THESIS_PATTERN]

    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        print("Inited PDF watcher to log out to " + output_path)
    
    def handleChange(self, event):
        # Only log out if this is a different time from the previous time (export
        # triggers multiple modification calls) and page_count is not empty
        current_time = getCurrentTime()
        global previous_time
        if deltaTimes(current_time, previous_time) > DELTA_TIMES_NEW_ENTRY:
            Thread(target=delayed_call_to_write_pdf_file_log, args=(event.src_path, self.output_path)).start()
            previous_time = current_time
        

    def on_modified(self, event):
        self.handleChange(event)

    def on_created(self, event):
        self.handleChange(event)

class OrgFileChangeWatcher(PatternMatchingEventHandler):
    patterns = [STATE_FILE_PATTERN]

    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path
        print("Inited Org file watcher to log out to " + output_path)
        
    def handleChange(self, event):
        write_org_file_log(event.src_path, self.output_path)

    def on_modified(self, event):
        self.handleChange(event)

    def on_created(self, event):
        self.handleChange(event)
        
def delayed_call_to_write_pdf_file_log(watched_file_page: str, log_path: str):
    current_time = getCurrentTime()
    time.sleep(SLEEP_TIME_FROM_MODIFY)
    try:
        write_pdf_file_log(watched_file_page, log_path, current_time)
    except:
        pass

# on change:
#     get timestamp
#     get page count
#     add timestamp and page count to a csv
def write_pdf_file_log(watched_file_path: str, log_path: str, current_time):
    page_count = get_page_count(watched_file_path)
    word_count = get_word_count(watched_file_path)

    if page_count and word_count:
        print("\nThesis pdf has changed")
        write_information_to_log_file(current_time,page_count,word_count,log_path)
        replot_count_graphs()
    
def write_org_file_log(watched_file_path: str, log_path: str):
    print("\nOrg file has changed")
    wholeFile = ''
    line = getCurrentTime()

    with open(watched_file_path,'r') as input:
        wholeFile = input.read()

    # for each status, count the occurances in file
    for status in STATUSES:
        occurances = wholeFile.count(status)
        normal_occurances = 1
        if status == "TODO":
            normal_occurances += 1
        # add that count to the line to output
        line += "," + str((occurances - normal_occurances))

    print ("Time and status counts " + line)
        
    # Add a newline
    line += '\n'
    
    with open(log_path,'a') as output:
        output.write(line)

    replot_status_graphs()

def deltaTimes(current_time : str, previous_time : str) -> int:
    if not previous_time:
        return DELTA_TIMES_NEW_ENTRY * 2
    current = datetime.strptime(current_time, "%Y-%m-%d-%H%M%S")
    previous = datetime.strptime(previous_time, "%Y-%m-%d-%H%M%S")
    delta = current - previous
    return delta.total_seconds()
        
def getCurrentTime():
    ts = time.gmtime()
    return time.strftime("%Y-%m-%d-%H%M%S",ts)

def get_page_count(pdf_file_path: str) -> str:
    sys_call = "pdfinfo " + pdf_file_path + " | grep Pages | awk '{print $2}'"
    # Get output from shell, decode from bytes and strip new line
    page_count = subprocess.check_output(sys_call, shell=True).decode("utf-8").rstrip()
    return page_count

def get_word_count(pdf_file_path: str) -> str:
    sys_call = "pdftotext " + pdf_file_path + " - | tr -d '.' | wc -w"
    word_count = subprocess.check_output(sys_call, shell=True).decode("utf-8").rstrip()
    return word_count

def write_information_to_log_file(current_time, page_count, word_count, path):
    print ("Current time " + current_time)
    print ("Page count " + page_count)
    print ("Word count " + word_count)
    line = current_time + "," + page_count + "," + word_count + "\n"
    with open(path,'a') as output:
        output.write(line)

def replot_count_graphs():
    try:
        pg.plot_combined_with_default_args()
        pg.plot_simple_line_with_default_args()
    except:
        print('Failed to plot graphs')
    
def replot_status_graphs():
    try:
        pg.plot_combined_with_default_args()
        pg.plot_stacked_regions_with_default_args()
    except:
        print('Failed to plot graphs')
    
        
# Use watchdog to watch for changes to thesis PDF
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 3:
        print("Format: python3 calc_logs.py pdf_directory org_file_directory log_file_directory")
        quit()
    pdf_directory = args[0]
    org_file_directory = args[1]
    pdf_log_file = args[2] + '/' + PAGE_COUNT_LOG_FILE_NAME
    org_file_log_file = args[2] + '/' + STATUS_LOG_FILE_NAME
    observer = Observer()
    print("Watching pdf directory " + pdf_directory)
    observer.schedule(PDFChangeWatcher(pdf_log_file), path=pdf_directory)

    print("Watching org file directory " + org_file_directory)
    observer.schedule(OrgFileChangeWatcher(org_file_log_file), path=org_file_directory)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
