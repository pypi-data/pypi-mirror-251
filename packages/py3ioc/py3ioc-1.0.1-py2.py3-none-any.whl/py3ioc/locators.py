# coding=utf-8
"""
Module containing implementation of the service locator.
"""

import inspect
import abc


class KeyToStringConverter:
    @staticmethod
    def generate_key(obj: object) -> str:
        if inspect.isclass(obj):
            return obj.__name__
        elif inspect.isfunction(obj):
            return 'func_%s' % obj.__name__
        else:
            return type(obj).__name__


class UnregisteredKeyError(KeyError):
    def __init__(self, key: str):
        self._key = key

    def __str__(self):
        return 'There is no object registered for the given "%s" key' % self._key

    def __unicode__(self):
        return self.__str__()


class KeyAlreadyRegisteredError(KeyError):
    def __init__(self, key: str):
        self._key = key

    def __str__(self):
        return 'There is already an object registered for the "%s" key' % self._key

    def __unicode__(self):
        return self.__str__()


# @six.add_metaclass(abc.ABCMeta)
class LocatorBase(abc.ABC):
    """
    Abstract Class Base declaring locator interface.
    """

    @abc.abstractmethod
    def register(self, key: str, obj: object):
        pass

    @abc.abstractmethod
    def locate(self, key: str):
        pass

    @abc.abstractmethod
    def get_or_default(self, key: str, default: object):
        pass

    def is_key_registered(self, key: str):
        pass

    def get_keys(self):
        pass


class ObjectLocator(LocatorBase):
    """
    Simple object locator implementation.
    """

    def __init__(self):
        self._objects = {}

    def register(self, key: str, obj: object) -> None:
        """
         Register object in locator under a specified key.

         :param key: Key under which object will be registered.
         :param obj: Object to register.
         """
        if key in self._objects:
            raise KeyAlreadyRegisteredError(key)

        self._set_instance(key, obj)

    def locate(self, key: str) -> object:
        """
        Returns the object registered for a given key.

        :param key: Key under which object was registered.
        :return: Object registered under the given key.
        """
        try:
            instance = self._get_instance(key)
        except KeyError:
            raise UnregisteredKeyError(key)

        return instance

    def get_or_default(self, key: str, default: object) -> object:
        """
        Gets the object for a given key. If the key is not present in the locator, returns value of *default* parameter.

        :param key: Key under which object was registered.
        :param default: Default value, if there is no object registered for a given key.
        :return: Object registered under the given key, or default.
        """
        try:
            instance = self._get_instance(key)
        except KeyError:
            return default

        return instance

    def is_key_registered(self, key: str) -> bool:
        """
        Checks if there is object registered for a given key in the locator.

        :param key: Key to look for.
        :return: True if there is a key in the locator, otherwise False.
        """
        try:
            self._objects[key]
        except KeyError:
            return False
        return True

    def get_keys(self) -> list[str]:
        return list(self._objects.keys())

    def _get_instance(self, key: str) -> object:
        return self._objects[key]

    def _set_instance(self, key: str, value: object) -> None:
        self._objects[key] = value
