import subprocess
from config import config

from log import log
from utils import send_message, bytes_to_human_readable_size


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
    # send_message(msg)


    
    

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