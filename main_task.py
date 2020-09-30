"""各種タスクを実行するメインタスク

Usage:
  main_task.py <channel-list-file-path> [--task=<task-name> | --all-reset]
  main_task.py (-h | --help)

Options:
  -h --help     Show this screen.
  --reset       Reset all data.

"""
from docopt import docopt
import pathlib
import shutil
from colorama import Fore, Style
import settings
import tasks.init_task as init_task
import tasks.channel_statistics_task as channel_statistics_task
import tasks.video_listup_task as video_listup_task
import tasks.video_statistics_task as video_statistics_task
import tasks.convert_json_to_csv_task as convert_json_to_csv_task

RESULT_FILE_PATH = "./task_result.txt"


def _init():
    """
    プロセス管理用の初期化処理を行う
    """
    fp = pathlib.Path(RESULT_FILE_PATH)
    fp.touch()


def _reset_all_data():
    """
    プロセス管理のファイルを削除し、タスクを全て再実行するようにする
    """
    print(f"Reset all data.")
    shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)

    fp = pathlib.Path(RESULT_FILE_PATH)
    fp.unlink(missing_ok=True)


def _task_executor(task, *args):
    """
    指定タスクの関数を実行する
    実行した際に例外が発生したら、その時点で終了する
    完了したらプロセス管理ファイルに追記され、再度タスク実行した際にはスキップされる
    Parameters
    ----------
    task : Function
    """
    task_name = task.__module__
    fp = pathlib.Path(RESULT_FILE_PATH)
    completed_tasks = fp.read_text().split("\n")

    if completed_tasks.count(task_name) > 0:
        print(f"{Fore.MAGENTA}[SKIP] {task_name} is completed.{Style.RESET_ALL}")
        return

    try:
        print(f"{Fore.GREEN}[EXEC] {task_name} is started.{Style.RESET_ALL}")
        task(*args)
    except Exception as e:
        print(f"{Fore.RED}[FAIL] {task_name} is failed.{Style.RESET_ALL}")
        print(e)
        exit()
    else:
        print(f"{Fore.CYAN}[SUCCESS] {task_name} is completed.{Style.RESET_ALL}")
        with fp.open(mode="a") as f:
            f.write(f"{task_name}\n")


def _force_task_executor(task, *args):
    try:
        print(f"{Fore.GREEN}[EXEC] {task_name} is started.{Style.RESET_ALL}")
        task(*args)
    except Exception as e:
        print(f"{Fore.RED}[FAIL] {task_name} is failed.{Style.RESET_ALL}")
        print(e)
        exit()
    else:
        print(f"{Fore.CYAN}[SUCCESS] {task_name} is completed.{Style.RESET_ALL}")


if __name__ == "__main__":
    arguments = docopt(__doc__)

    channel_list_file_path = arguments["<channel-list-file-path>"]

    if arguments["--all-reset"]:
        _reset_all_data()

    if arguments["--task"]:
        task_name = arguments["--task"]
        _force_task_executor(locals()[f"{task_name}"].main, channel_list_file_path)
        exit()

    _init()

    _task_executor(init_task.main)
    _task_executor(channel_statistics_task.main, channel_list_file_path)
    _task_executor(video_listup_task.main, channel_list_file_path)
    _task_executor(video_statistics_task.main, channel_list_file_path)
    _task_executor(convert_json_to_csv_task.main, channel_list_file_path)
