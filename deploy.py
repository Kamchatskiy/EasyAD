import os
import yaml
import subprocess


def load_config(config_file):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def generate_docker_compose_commands(config):
    commands = []

    for entry_id, entry in config.items():
        env_vars = {
            "TEAM_ID": entry["id"],
            "NAME": entry["name"],
            "TOKEN": entry["token"],
            "PASSWORD": entry["password"],
            "JUDGE_IP": entry["judge_ip"],
        }

        env_var_strings = [f"{var}={value}" for var, value in env_vars.items()]
        command_string = " ".join(env_var_strings) + " docker compose -f docker/team.docker-compose.yml up -d"
        commands.append(command_string)

    return commands


if __name__ == "__main__":
    try:
        config = load_config("config.yml")
        commands = generate_docker_compose_commands(config)

        for command in commands:
            print("Running command:", command)
            subprocess.run(command, shell=True, check=True)

    except FileNotFoundError:
        print("Error: 'config.yml' was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{e.cmd}' failed with exit code {e.returncode}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
