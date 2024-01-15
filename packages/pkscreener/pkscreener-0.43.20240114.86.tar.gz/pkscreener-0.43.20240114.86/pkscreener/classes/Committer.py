"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
# import argparse
import os
import platform

from PKDevTools.classes import Archiver

# argParser = argparse.ArgumentParser()
# required = False
# argParser.add_argument("-m", "--message", help="Commit message", required=required)
# argParser.add_argument(
#     "-b", "--branch", help="Origin branch name to push to", required=required
# )
# args = argParser.parse_known_args()


def commitTempOutcomes(reportName):
    if "Windows" not in platform.system():
        return
    try:
        if ("BACKTEST_NAME" not in os.environ.keys()) or (
            "RUNNER" not in os.environ.keys()
        ):
            print(
                "This commit does not seem to have been triggered from GitHub Action! Ignoring..."
            )
            return
    except Exception:
        return

    execOSCommand(
        f"copy {os.path.join(Archiver.get_user_outputs_dir(),'PKScreener_*.html')} {os.path.join(os.getcwd(),'Backtest-Reports')}"
    )
    execOSCommand("git config user.name github-actions")
    execOSCommand("git config user.email github-actions@github.com")
    execOSCommand(
        "git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'"
    )
    execOSCommand("git remote update")
    execOSCommand("git fetch")
    execOSCommand("git pull")
    execOSCommand(
        f"git add {os.path.join(os.getcwd(),'Backtest-Reports')}/PKScreener_{reportName}_backtest_result_StockSorted.html --force"
    )
    execOSCommand(
        f"git add {os.path.join(os.getcwd(),'Backtest-Reports')}/PKScreener_{reportName}_Summary_StockSorted.html --force"
    )
    execOSCommand(
        f"git add {os.path.join(os.getcwd(),'Backtest-Reports')}/PKScreener_{reportName}_OneLine_Summary.html --force"
    )
    execOSCommand(
        f"git add {os.path.join(os.getcwd(),'Backtest-Reports')}/PKScreener_{reportName}_Insights_DateSorted.html --force"
    )
    execOSCommand(
        f"git commit -m '[Temp-Commit]GitHub-Action-Workflow-Backtest-Reports-({reportName})'"
    )
    execOSCommand("git pull")
    execOSCommand("git push -v -u origin +gh-pages")


def execOSCommand(command):
    try:
        os.system(command)
    except Exception:
        pass
