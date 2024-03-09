#!/usr/bin/python3
"""Console module"""
import cmd
from models.base_model import BaseModel
from models import storage

classes = {"BaseModel": BaseModel}


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """End of File command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Handle empty line"""
        pass

    def do_create(self, arg):
        """Create command"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        else:
            new_instance = classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Show command"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            all_objs = storage.all()
            if key in all_objs:
                print(all_objs[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy command"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            all_objs = storage.all()
            if key in all_objs:
                del all_objs[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """All command"""
        args = arg.split()
        all_objs = storage.all()
        if len(args) == 0:
            print([str(value) for value in all_objs.values()])
        elif args[0] not in classes:
            print("** class doesn't exist **")
        else:
            print([str(value) for key, value in all_objs.items()
                   if key.startswith(args[0] + '.')])

    def do_update(self, arg):
        """Update command"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            all_objs = storage.all()
            if key not in all_objs:
                print("** no instance found **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                setattr(all_objs[key], args[2], args[3])
                storage.save()

    def do_count(self, arg):
        """Count command"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            count = sum(1 for key in all_objs if key.split('.')[0] == args[0])
            print(count)

    def default(self, arg):
        """Default command"""
        commands = arg.split(".")
        if len(commands) >= 2:
            if commands[1] == "all()":
                self.do_all(commands[0])
            elif commands[1] == "count()":
                self.do_count(commands[0])
            elif commands[1].startswith("show("):
                self.do_show(commands[0] + " " + commands[1][6:-2])
            elif commands[1].startswith("destroy("):
                self.do_destroy(commands[0] + " " + commands[1][9:-2])
            elif commands[1].startswith("update("):
                args = commands[1][7:-2].split(", ")
                if len(args) >= 4:
                    self.do_update(commands[0] + " " + " ".join(args))
                else:
                    print("** argument(s) missing **")
            else:
                print("** command not found **")
        else:
            print("** command not found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
