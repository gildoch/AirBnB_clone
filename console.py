#!/usr/bin/python3
"""
This is the console base for the airbnb
"""

import cmd
from models import storage
import shlex
import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Holberton command prompt to access models data"""

    prompt = "(hbnb) "

    CLASSES = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def emptyline(self):
        """Overrides default emptyline method"""
        pass

    def do_EOF(self, arg):
        """Close Interpreter and saves data, [CTR + D]"""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """
        Creates a new instance of the specified class, saves it
        to the JSON file, and prints the id.

        Args:
            class_name (str): The name of the class for which
            an instance will be created.

        Example:
            $ create BaseModel
        """
        argv = shlex.split(arg)

        if not arg:
            print("** class name missing **")
            return

        if len(argv) > 1:
            print("Please provider one class Only (Ex: $ create <Class>)")
            return

        if argv[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
            return

        new_object = HBNBCommand.CLASSES[argv[0]]()
        new_object.save()
        print(new_object.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on
        the class name and id.

        Args:
            arg (str): A string containing the class name
            and id of the instance.
            The format should be: "show <class_name> <instance_id>".

        Example:
            $ show BaseModel 1234-1234-1234
        """
        argv = shlex.split(arg)

        if not arg:
            print("** class name missing **")
            return

        if argv[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
            return

        if len(argv) <= 1:
            print("** instance id missing **")
            return

        storage.reload()
        objects = storage.all()
        key = argv[0] + "." + argv[1]

        if key in objects:
            print(str(objects[key]))
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id and saves the changes into the JSON file.

        Args:
            arg (str): A string containing the class
            name and id of the instance to be deleted.
            The format should be: "destroy <class_name> <instance_id>".

        Example:
            $ destroy BaseModel 1234-1234-1234
        """
        argv = shlex.split(arg)
        if not arg:
            print("** class name missing **")
            return

        if len(argv) >= 1 and argv[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
            return

        if len(argv) <= 1:
            print("** instance id missing **")
            return

        storage.reload()
        objects = storage.all()

        key = argv[0] + "." + argv[1]

        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints string representations of all instances based on the class
        name or all instances if no class name is provided.

        Args:
            arg (str, optional): A string containing the class name. If
            provided, prints string representations of all instances of
            that class. If not provided, prints string representations
            of all instances of all classes.

        Example:
            $ all BaseModel
            $ all
        """
        argv = shlex.split(arg)
        storage.reload()
        objects = storage.all()
        obj_list = []

        if not arg:
            for key in objects.keys():
                obj_list.append(str(objects[key]))
            print(json.dumps(obj_list))
            return

        if len(argv) >= 1 and argv[0] in HBNBCommand.CLASSES:
            for key in objects.keys():
                cls = key.split(".")
                if argv[0] == cls[0]:
                    obj_list.append(str(objects[key]))
            print(json.dumps(obj_list))
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating an attribute, and saves the changes
        into the JSON file.

        Args:
            arg (str): A string containing the class name,
            instance id, attribute name, and attribute value.
        Example:
            $ update BaseModel 1234-1234-1234 email "airbnb@mail.com"
        """

        argv = shlex.split(arg)

        if not arg:
            print("** class name missing **")
            return

        if argv[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
            return

        if len(argv) == 1:
            print("** instance id missing **")
            return

        storage.reload()
        objects = storage.all()

        key = argv[0] + "." + argv[1]

        if key not in objects:
            print("** no instance found **")
            return

        if len(argv) == 2:
            print("** attribute name missing **")
            return

        if len(argv) == 3:
            print("**  value missing **")
            return

        my_obj = objects[key]

        if hasattr(my_obj, argv[2]):
            data_type = type(getattr(my_obj, argv[2]))
            setattr(my_obj, argv[2], data_type(argv[3]))
        else:
            setattr(my_obj, argv[2], argv[3])

        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
