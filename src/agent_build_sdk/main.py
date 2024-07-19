#!/usr/bin/env python
import sys
from agent_build_sdk.crew import AgentBuildSdkCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    AgentBuildSdkCrew().crew().kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        AgentBuildSdkCrew().crew().train(n_iterations=int(sys.argv[1]))

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
