#!/usr/bin/python3
"""
Contains the entry point of the command interpreter.
"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class.
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF to exit the program"""
        print("")
        return True

    def emptyline(self):
        """Empty line should do nothing"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id.
        Usage: create <class name>
        """
        if arg == "":
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except Exception:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id (save the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        del(storage.all()[key])
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the class name.
        Usage: all [<class name>]
        """
        if arg == "":
            print([str(value) for value in storage.all().values()])
            return
        if arg not in storage.classes():
            print("** class doesn't exist **")
            return
        print([str(value) for key, value in storage.all().items() if arg in key])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or updating attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        if len(args) > 4:
            print("** Too many arguments **")
            return
        try:
            attr_value = eval(args[3])
        except Exception:
            attr_value = args[3]
        setattr(storage.all()[key], args[2], attr_value)
        storage.save()

    def default(self, arg):
        """
        Method called on an input line when the command prefix is not recognized.
        """
        args = arg.split(".")
        if len(args) >= 2:
            if args[1] == "all()":
                self.do_all(args[0])
                return
            elif args[1] == "count()":
                print(sum([1 for key in storage.all().keys() if args[0] in key]))
                return
            elif args[1][:5] == "show(":
                idx = args[1].find('"')
                self.do_show(args[0] + " " + args[1][idx:])
                return
            elif args[1][:8] == "destroy(":
                idx = args[1].find('"')
                self.do_destroy(args[0] + " " + args[1][idx:])
                return
            elif args[1][:7] == "update(":
                idx1 = args[1].find('"')
                idx2 = args[1].find('"', idx1 + 1)
                idx3 = args[1].find('"', idx2 + 1)
                idx4 = args[1].find('"', idx3 + 1)
                arg_update = args[0] + " " + args[1][idx1:idx4 + 1]
                self.do_update(arg_update)
                return
        print("*** Unknown syntax: {}".format(arg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
