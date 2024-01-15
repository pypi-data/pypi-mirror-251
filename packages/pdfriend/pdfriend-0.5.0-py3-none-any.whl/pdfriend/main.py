import argparse
from pdfriend.classes.config import Config
from pdfriend.classes.platforms import Platform
import pdfriend.classes.cmdparsers as cmdparsers
import pdfriend.classes.exceptions as exceptions
import pdfriend.commands as commands
import pdfriend.utils as utils


def main():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("commands", type=str, nargs="*")

    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")

    parser.add_argument("-o", "--outfile", type=str, default="pdfriend_output")
    parser.add_argument("-i", "--inplace", action="store_true")
    parser.add_argument("-q", "--quality", type=int, default=100)

    parser.add_argument("--get", type=str, default=None)
    parser.add_argument("--set", type=str, default=None)
    parser.add_argument("--pop", type=str, default=None)

    args = parser.parse_args()

    Platform.Init()
    Config.Debug = args.debug

    command = ""
    if len(args.commands) > 0:
        command = args.commands[0]

    cmd_parser = cmdparsers.CmdParser(command, args.commands[1:])

    try:
        if command == "version" or args.version:
            print(commands.version())
        elif command == "help" or args.help:
            command_to_display = cmd_parser.next_str_or(None)
            commands.help(command_to_display)
        elif command == "merge":
            if len(cmd_parser.args) == 0:
                print("You need to specify at least one file or pattern to be merged")
                return

            commands.merge(cmd_parser.args, args.outfile, args.quality)
        elif command == "edit":
            infile = cmd_parser.next_str("filename")
            commands.edit(infile)
        elif command == "invert":
            infile = cmd_parser.next_str("filename")

            if args.inplace:
                args.outfile = infile

            commands.invert(infile, args.outfile)
        elif command == "swap":
            infile = cmd_parser.next_str("filename")
            page_0 = cmd_parser.next_int("page_0")
            page_1 = cmd_parser.next_int("page_1")

            if args.inplace:
                args.outfile = infile

            commands.swap(infile, page_0, page_1, args.outfile)
        elif command == "clear":
            commands.clear()
        elif command == "remove":
            infile = cmd_parser.next_str("filename")
            slice = cmd_parser.next_str("pages")

            if args.inplace:
                args.outfile = infile

            commands.remove(infile, slice, args.outfile)
        elif command == "weave":
            infile_0 = cmd_parser.next_str("filename_0")
            infile_1 = cmd_parser.next_str("filename_1")

            commands.weave(infile_0, infile_1, args.outfile)
        elif command == "split":
            infile = cmd_parser.next_str("filename")
            slice = cmd_parser.next_str("pages")

            commands.split(infile, slice, args.outfile)
        elif command == "encrypt":
            infile = cmd_parser.next_str("filename")

            if args.inplace:
                args.outfile = infile

            commands.encrypt(infile, args.outfile)
        elif command == "decrypt":
            infile = cmd_parser.next_str("filename")

            if args.inplace:
                args.outfile = infile

            commands.decrypt(infile, args.outfile)
        elif command == "metadata":
            infile = cmd_parser.next_str("filename")

            commands.metadata(infile, args.get, args.set, args.pop)
        else:
            print(f"command \"{command}\" not recognized")
            print("use pdfriend help for a list of the available commands")
    except exceptions.ExpectedError as e:
        print(e)
    except Exception as e:
        utils.print_unexpected_exception(e, Config.Debug)
