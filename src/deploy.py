import subprocess
from config import Config
from log import log
from utils import bytes_to_human_readable_size

RSYNC_CMD_BASE = "rsync -az --progress --stats --delete"

SERVER = "ress@newfold"
SRC = Config.BASE_DIR
DST = Config.APP_NAME


def upload_sources():
    log("monitoress - starting deploy")

    cmd = f'{RSYNC_CMD_BASE} {SRC}/ {SERVER}:{DST}/ | grep "Total bytes sent\|files transferred"'

    success, output = run_command(cmd)
    if not success:
        log("deploy failed")
        return

    def get_num_from_output_line(s, line_n):
        return int(s.split("\n")[line_n].split(" ")[-1].replace(",", ""))

    files_counter = get_num_from_output_line(output, 0)
    bandwith_counter = get_num_from_output_line(output, 1)
    msg = f"uploaded, {bytes_to_human_readable_size(bandwith_counter)} for {files_counter} files"
    log(msg)
    if success:
        restart_script_in_remote_tmux()


def restart_script_in_remote_tmux():
    cmd = f"ssh {SERVER} -t 'tmux send-keys -t {Config.APP_NAME} C-C C-U \"~/.local/bin/poetry run python {config.ENTRYPOINT}\" Enter'"
    success, output = run_command(cmd)
    if not success:
        log("restart remote tmux failed")
        return


def run_command(cmd: str) -> str:
    log(f"run command {cmd}")
    try:
        output = subprocess.check_output(cmd, shell=True)
    except Exception as ex:
        print("exception")
        print(ex)
        return False, str(ex)
    return True, output.decode("utf-8")


if __name__ == "__main__":
    upload_sources()


"""

ssh ress@fold -t 'tmux a -t 1 \; send-keys C-U ls Enter'

ssh ress@fold -t 'tmux send-keys -t 1 C-C C-U "poetry run python src/main.py" Enter'


"""
