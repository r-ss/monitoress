import subprocess
from config import config

from log import log
from utils import bytes_to_human_readable_size


RSYNC_CMD_BASE = 'rsync -az --progress --stats --delete'

files_counter: int = 0
bandwith_counter: int = 0  # in bytes

def upload_sources():
    log('monitoress - starting deploy')
    global bandwith_counter, files_counter

    SERVER = 'ress@fold'
    SRC = config.BASE_DIR
    DST = config.APP_NAME

    cmd = f'{RSYNC_CMD_BASE} {SRC}/ {SERVER}:{DST}/ | grep "Total bytes sent\|files transferred"'

    success, output = run_command(cmd)
        
    if not success:
        log('deploy failed')
        return

    

    files_counter += int(output.split('\n')[0].split(' ')[-1].replace(',',''))
    bandwith_counter += int(output.split('\n')[1].split(' ')[-1].replace(',',''))

    msg = f'uploaded, {bytes_to_human_readable_size(bandwith_counter)} for {files_counter} files'

    log(msg)

    if success:
        restart_script_in_remote_tmux()

    
def restart_script_in_remote_tmux():
    cmd = "ssh ress@fold -t 'tmux send-keys -t 1 C-C C-U \"poetry run python src/main.py\" Enter'"
    success, output = run_command(cmd)

    if not success:
        log('restart remote tmux failed')
        return





def run_command(cmd: str) -> str:
    log(f'run command {cmd}')
    try:
        output = subprocess.check_output(cmd, shell=True)
    except Exception as ex:
        print('exception')
        print(ex)
        return False, str(ex)
    return True, output.decode('utf-8')


if __name__ == '__main__':
    upload_sources()



"""

ssh ress@fold -t 'tmux a -t 1 \; send-keys C-U ls Enter'

ssh ress@fold -t 'tmux send-keys -t 1 C-C C-U "poetry run python src/main.py" Enter'


"""