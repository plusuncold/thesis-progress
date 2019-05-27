# Thesis progress

A simple little script to log progress on the state of parts of a thesis and the page count. The script watches for a thesis PDF and an org file changing and updates the graphs.

![][combined.png]

## State file

This is an org file, which can be edited in a text editor, but was originally intended for org-mode in emacs. An example is included (thesis_plan.org). As you progress you can move each section into a different status from TODO to STARTED through FIRST_DRAFT, SECOND_DRAFT, REVISIONS_DONE and finally COMPLETE. All sections should start off as TODO (red on the graph).

## Running the Program

Edit the `run.sh` file to provide the program with the folders to find the thesis .pdf and the state .org files. These are in the THESIS_FOLDER and LOG_FOLDER paths, respectively. The program to watch the files can then be run with the command `./run.sh`.

Requirements:

- Python3
- pdfinfo
- pdftotext

## Advanced

### Deadline

If you would like to have a deadline on the graph set `PLOT_DEADLINE=True` in `plot_graphs.py` and set the deadline in `DEADLINE` with the format `YYYY-MM-DD-235959`.

### Different Thesis pdf title

If your thesis pdf is not titled `title.pdf` edit `THESIS_PATTERN` in `calc_log.py`.