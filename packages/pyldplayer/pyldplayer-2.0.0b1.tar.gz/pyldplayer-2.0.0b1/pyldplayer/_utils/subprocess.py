import subprocess

def subprocess_query(
    path : str, 
    command : str= None, 
    *args, 
    timeout : int = 10,
    no_filter : bool = False,
    leave_raw : bool = False
):
    """
    Executes a query command and returns the parsed output as a list of strings.
    
    Args:
        command (str, optional): The query command to execute. If not provided, the default command will be used. 
        Defaults to None.
        *args: Additional arguments for the query command.
        timeout (int, optional): The maximum time to wait for the query command to complete, in seconds. 
        Defaults to 10.
        no_filter (bool, optional): Whether to filter out empty strings from the parsed output. Defaults to False.
    
    Returns:
        list: The parsed output of the query command as a list of strings.
    """
    try:
        if command is None:
            queryed = [path]
        else:
            queryed = [path, command, *args]

        proc : subprocess.CompletedProcess = subprocess.run(
            queryed,
            capture_output=True,
            timeout=timeout
        )
        comm : bytes = proc.stdout

    except subprocess.TimeoutExpired as e:
        raise e
    except subprocess.CalledProcessError as e:
        raise e
    
    if leave_raw:
        return comm
    
    try:
        parsed = comm.decode("utf-8")
    except: # noqa
        parsed = comm.decode("gbk")
    

    parsed = parsed.strip().split("\r\n")
    # return stripped and splitted
    if no_filter:
        parsed = list(filter(None, parsed))
        parsed = list(map(lambda x: x.strip(), parsed))

    return parsed

def subprocess_exec(path : str, command : str, *args):
    """
    Executes a command with the given arguments.

    Args:
        command (str): The command to be executed.
        *args (tuple): Additional arguments for the command.
    """
    subprocess.Popen( # noqa
        [path, command, *args],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=
            subprocess.DETACHED_PROCESS |
            subprocess.CREATE_NEW_PROCESS_GROUP | 
            subprocess.CREATE_BREAKAWAY_FROM_JOB
    )        