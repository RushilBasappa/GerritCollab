import click
from subprocess import call, Popen,PIPE, STDOUT, check_output
import subprocess
import os

USERNAME=""

@click.group()
def cli():
    """A CLI wrapper for gerrit"""
    if subprocess.call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
        print("Not a git repository!!")
        exit()
    if "GERRITCOLLABNAME" in os.environ:
        global USERNAME
        USERNAME=os.environ['GERRITCOLLABNAME']
    else:
        click.echo("Set ENV variable GERRITCOLLABNAME with your gerrit username")
        click.echo("export GERRITCOLLABNAME=<NAME>")
        exit()

    pass

@cli.command()
@click.argument('cl')
def pull_and_checkout(cl):
    COMMAND = "git ls-remote gerrit | awk '{{print $2}}' | grep -E '{CL_2}/{CL}/[0-9]{{1,3}}' | sort -V | tail -1".format(CL=cl,CL_2=cl[-2:])
    ref_path = run_cmd(COMMAND)
    print(ref_path)
    _,_,XX,YYYY,PP = ref_path.split('/')

    COMMAND = "git fetch \"https://{USERNAME}@gerrit.p.sojern.net/a/sojern/python\" refs/changes/{XX}/{YYYY}/{PP} && git checkout FETCH_HEAD && git checkout -b {YYYY}_{PP}".format(XX=XX,YYYY=YYYY,PP=PP,USERNAME=USERNAME)
    print(COMMAND)
    output = run_cmd(COMMAND)
    click.echo(output)

@cli.command()
@click.argument('cl')
def list_patchsets(cl):
    COMMAND = "git ls-remote gerrit | awk '{{print $2}}' | grep -E '{CL_2}/{CL}/[0-9]{{1,3}}' | sort -V".format(CL=cl,CL_2=cl[-2:])
    patchsets = run_cmd(COMMAND)
    print(patchsets)

def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=PIPE)
    output, err = process.communicate()
    if err:
        print('The process raised an error:', err.decode())
        exit()
    return output.strip().decode("utf-8")

