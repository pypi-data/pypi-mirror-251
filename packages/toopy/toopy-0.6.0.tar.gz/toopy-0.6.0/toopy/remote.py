import os
import argparse
from fabric import Connection
from helpers.store_file import (
    read_settings, 
    read_config, 
    _insert_username,
    unixify_path
)

settings = read_settings()
passphrase = input("passphrase for private key: ")
client = Connection(
    host=settings["remote_server"], 
    user=settings["username_remote"],
    connect_kwargs=dict(key_filename=[settings["ssh_key"]], passphrase=passphrase)
)

def download_sbi(c, sbi_config):
    conf = read_config(sbi_config)
    remotedir = _insert_username(settings, conf["output_remote"])
    localdir = conf["output_local"]
    download(c, remotedir, localdir, exclude_subdir="sims")
    
def download(c, remote_dir, local_dir, exclude_subdir=""):
    if exclude_subdir == "":
        result = c.run(f"find {remote_dir}")
    else:
        result = c.run(
            f"find {remote_dir} -not -path '{remote_dir}{exclude_subdir}/*'"
        )

    remotefiles = result.stdout.split("\n")

    for rf in remotefiles:
        if rf == "":
            continue

        lf = rf.replace(remote_dir, local_dir)
        isdir = c.run(
            f"""
            if [[ -d {rf} ]]
            then
                echo 1
            else
                echo 0
            fi
            """
        )
        if isdir.stdout.replace("\n", "") == "1":
            os.makedirs(lf, exist_ok=True)

        else:
            res = c.get(rf, lf)

def submit(c, script, array="", script_arguments=""):
    # TODO: implement git status checks if the repo is up to date
    #       implement pull (this could go all together in one function)
    script = unixify_path(script)
    assert os.path.exists(script), "specify a script that locally exists"
    
    proj_dir = unixify_path(settings["remote_project_dir"])

    with c.cd(proj_dir):
        _ = c.run(f"sbatch {script}")

def run_sbi(c, sbi_config, array="1-500", sims_per_array="200", mcmc_arrays="1-20"):
    sbi_runner = unixify_path("scripts/bash/simulate_and_train.sh")
    assert os.path.exists(sbi_runner), "make sure simulate_and_train.sh exists"
    
    proj_dir = unixify_path(settings["remote_project_dir"])
    
    
    with c.cd(proj_dir):
        command = f"source {sbi_runner} {sbi_config} {array} {sims_per_array} {mcmc_arrays}"
        _ = c.run(command)

# download_sbi(client, "config/parameters/sbi/expo_control_mvlognorm_informed.json")
# submit(client, "scripts/bash/run_tests.sh")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog="interface with remote server to submit scripts and download results")
    parser.add_argument("program", help="a program from the available methods")
    parser.add_argument("-o", "--options", nargs="*", type=str,
        help="arguments for the specified program")
    args = parser.parse_args()

    # get the needed program from the methods defined above
    method = locals()[args.program]

    # pass positional agruments from --options flag to the method
    method(client, *args.options)

