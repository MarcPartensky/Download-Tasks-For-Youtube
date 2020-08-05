from downloader import VideoTasksDownloader
import options
import sys
import os

class Command:
    def __init__(self, f, argv, aliases:list=[], subcommands:list=[]):
        """Define a command using the function to execute f,
        its command name, its aliases, and its subcommands."""
        self.f = f
        self.argv = argv
        if len(self.argv)==0: self.argv = (f.__name__, )
        self.aliases = aliases
        self.subcommands = subcommands

    def help(self):
        """Return the doc of the command for a helper message."""
        return self.f.__doc__

    def match(self, argv):
        """Check if the sys.argv matches the command."""
        if self.argv == tuple(argv[:len(self.argv)]):
            return True
        # print(self.aliases, self.argv, argv)
        for alias in self.aliases:
            if alias == argv[0]:
                return True
        return False

    def __call__(self, cli, argv):
        """Call the command using a reference to the cli and its parameters by parsing sys.argv."""
        if len(argv[len(self.argv):]) > 0:
            if self.subcommands:
                for subcommand in self.subcommands:
                    if subcommand.match(argv[len(self.argv):]):
                        return subcommand(cli, argv[len(self.argv):])
            return self.f(cli, *argv[len(self.argv):])
        else:
            return self.f(cli)

    def command(self, *argv, aliases:list=[]):
        """Define a subcommand using its name and aliases."""
        obj = self
        def decorator(f):
            # print(obj, obj.subcommands)
            obj.subcommands.append(Command(f, argv, aliases=aliases))
            # print("printing self:", self.argv, self.subcommands)
            # print(f)
            return f
        return decorator

    def __str__(self):
        """Return the string representation of the command."""
        string = f"{' '.join(self.argv)}"
        if self.aliases:
            string += f"[{'|'.join(self.aliases)}]"
        string += f": {self.help()}"
        # print(self.argv)
        # print(self.subcommands)
        # # print(id(self))
        # if len(self.subcommands) > 0:
        #     for subcommand in self.subcommands:
        #         # print(subcommand)
        #         string += "\n   "+str(subcommand)
        # print(self.argv, self.subcommands)
        return string

class Commander:
    """Creator of commands."""
    def __init__(self, *argv, aliases:list=[]):
        """Take the parameters argv and aliases of the command."""
        self.argv = argv
        self.aliases = aliases

    def __call__(self, f):
        """Return the command."""
        if len(self.argv)==0: self.argv = (f.__name__, )
        return Command(f, self.argv, aliases=self.aliases)

command = Commander

class BaseCommandLineInterface:
    def __init__(self, commands:list=[]):
        """Define the list of commands."""
        self.commands = commands
        self.update()

    def update(self):
        """Use the command line to use the downloader."""
        self.commands = []
        for attr in dir(self):
            value = getattr(self, attr)
            if isinstance(value, Command):
                # print('update:', value)
                self.commands.append(value)

    def main(self):
        """Check if there is a matching command and executes it if so."""
        for command in self.commands:
            if command.match(sys.argv[1:]):
                return command(self, sys.argv[1:])
        print(
            f"No command named \'{' '.join(sys.argv[1:])}\'."
            f"\nUse the 'help' command to see available commands."
        )

class CommandLineInterface(BaseCommandLineInterface):
    """Command Line Interface to use the downloader of videos from the terminal."""
    def __init__(self,
        downloader:VideoTasksDownloader = VideoTasksDownloader(options.options, options.videos_filename),
        commands:list = [],
    ):
        """Create a downloader."""
        super().__init__(commands)
        self.downloader = downloader

    @command()
    def download(self):
        """Download the videos."""
        self.downloader.download()
    
    @download.command()
    def terminal(self):
        """Download the videos using the terminal technique."""
        self.downloader.download_terminal()

    @command()
    def test(self, n=2):
        """Prints n."""
        print(n)

    @command('commands')
    def all_commands(self):
        """Print all commands."""
        print("Commands:")
        for command in sorted(self.commands, key=lambda command:command.argv):
            print(f"* {command}")

    @command()
    def help(self, *argv):
        """Print help for some commands."""
        if not argv:
            print("You must precise the command you need help with.")
        def find_the_one(commands, argv):
            for command in commands:
                if command.match(argv):
                    if len(argv) > len(command.argv):
                        found_command = find_the_one(command.subcommands, argv[len(command.argv):])
                        if found_command: return found_command
                    return command
        command = find_the_one(self.commands, argv)
        if not command:
            print(f"The command {' '.join(argv)} does not exist.")
        else:
            print(f"{' '.join(argv)}:", command.help())

    @command()
    def options(self):
        """Print the options for youtube-dl when downloading the videos."""
        print("Options:")
        for k,v in self.downloader.options.items():
            print(f"* {k}: {v}")

    @command()
    def videos(self):
        """Print all the videos tasks url to download."""
        print("Videos:")
        for file in os.listdir(self.downloader.videos_folder):
            print(f"* {file}")

    @videos.command()
    def filename(self):
        """Print videos file name."""
        print(self.downloader.videos_filename)

    @videos.command('parsed')
    def parsed(self):
        """Print all the parsed videos tasks urls to download."""
        print("Parsed videos:")
        for i, video in enumerate(self.downloader.parsed_videos):
            print(f"* {i}: {video}")

    @videos.command()
    def clear(self):
        """Remove all the files in the videos folder."""
        for file in os.listdir(self.downloader.videos_folder):
            path = os.path.join(self.downloader.videos_folder, file)
            os.remove(path)

    @videos.command()
    def clean(self):
        """Remove all the caches or files that are not videos or musics in the videos folder."""
        for file in os.listdir(self.downloader.videos_folder):
            if not file.endswith('mp3') and not file.endswith('mp4'):
                path = os.path.join(self.downloader.videos_folder, file)
                os.remove(path)

    @command()
    def task(self):
        """Group of task commands."""
        print("Tasks:")
        for i, video in enumerate(self.downloader.videos):
            print(f"* {i}: {video}")

    @task.command()
    def add(self, *videos:str):
        """Add some tasks."""
        self.downloader.videos = self.downloader.videos + list(videos)

    @task.command(aliases=['rm'])
    def remove(self, *numbers:int):
        """Remove some tasks given their numbers."""
        for number in sorted(map(int, numbers), reverse=True):
            videos = self.downloader.videos
            del videos[number]
            self.downloader.videos = videos

    @task.command()
    def clear(self):
        """Clear the videos tasks of the downloader."""
        del self.downloader.videos

    @task.command()
    def number(self):
        """Print the number of videos to be downloaded."""
        print(len(self.downloader.videos))