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
        for alias in self.aliases:
            if alias == argv[0]:
                return True
        return False

    def __call__(self, cli, argv):
        """Call the command using a reference to the cli and its parameters by parsing sys.argv."""
        if len(argv[len(self.argv):]) > 0:
            return self.f(cli, *argv[len(self.argv):])
        else:
            return self.f(cli)

    def command(self, *argv, aliases:list=[]):
        def decorator(f):
            self.subcommands.append(Command(f, argv, aliases=aliases))
            return f
        return decorator

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

class CommandLineInterface:
    """Command Line Interface to use the downloader of videos from the terminal."""
    def __init__(self,
        downloader:VideoTasksDownloader = VideoTasksDownloader(options.options, options.videos_filename),
        commands:list = [],
    ):
        """Create a downloader."""
        self.downloader = downloader
        self.commands = commands
        self.update()


    def update(self):
        """Use the command line to use the downloader."""
        self.commands = []
        for attr in dir(self):
            value = getattr(self, attr)
            if isinstance(value, Command):
                self.commands.append(value)

    def main(self):
        """Check if there is a matching command and executes it if so."""
        def f(commands):
            for command in commands:
                if command.match(sys.argv[1:]):
                    command(self, sys.argv[1:])
                    return
                f(command.subcommands)
        f(self.commands)
        print(
            f"No command named \'{' '.join(sys.argv[1:])}\'."
            f"\nUse the 'help' command to see available commands."
        )

    @command()
    def download(self):
        """Download the videos."""
        self.downloader.download()

    @command()
    def test(self, n=2):
        """Prints n."""
        print(n)

    @command('commands', aliases=['help'])
    def list_commands(self):
        """Print all commands."""
        print("Commands:")
        for command in sorted(self.commands, key=lambda command:command.full_argv):
            print(f"* {command}")

    @command('videos', 'filename')
    def videos_filename(self):
        """Print videos file name."""
        print(self.downloader.videos_filename)

    @command()
    def number(self):
        """Print the number of videos to be downloaded."""
        print(len(self.downloader.videos))

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
        for i, video in enumerate(self.downloader.videos):
            print(f"* {i}: {video}")

    @command('parsed')
    def parsed(self):
        """Print all the parsed videos tasks urls to download."""
        print("Parsed videos:")
        for i, video in enumerate(self.downloader.parsed_videos):
            print(f"* {i}: {video}")

    @command('clear', 'tasks')
    def clear_tasks(self):
        """Clear the videos tasks of the downloader."""
        del self.downloader.videos

    @command('clear', 'videos')
    def clear_videos(self):
        """Remove all the files in the videos folder."""
        for file in os.listdir(self.downloader.videos_folder):
            os.remove(file)

    @command('clean', 'videos')
    def clean_videos(self):
        """Remove all the caches or files that are not videos or musics in the videos folder."""
        raise NotImplemented
        # for file in os.listdir(self.downloader.videos_folder):

        #     os.remove(file)


    @command()
    def task(self):
        """Group of task commands."""
        print("tasks")

    @task.command()
    def add(self, video):
        """Add a task."""
        self.downloader.videos = self.downloader.videos + [video]

    @task.command(aliases=['rm'])
    def remove(self, *numbers):
        """Remove some tasks given their numbers."""
        for number in sorted(numbers, reverse=True):
            pass




        



        

        # elif sys.argv[1] == "filename":
        #     if len(sys.argv) == 3:
        #         self.downloader.videos_filename = sys.argv[2]
        #     else:
        #         print(self.downloader.videos_filename)

