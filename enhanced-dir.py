import os
import sys


class Directory(object):

    def __init__(self, path, mode='r'):
        """
            Directory object for interaction with file collections
            :param path: path of directory
            :param mode: mode of interaction with directory
                's' - stat (ony access file stats)
                'r' - read (only read files)
                'a' - append (only add files)
                'w' - write (add and remove files)
        """
        if not mode in ('r', 'a', 'w'):
            raise ValueError("Mode {} is not applicable".format(mode))
        self.mode = mode
        self.__read_perm = False
        self.__append_perm = False
        self.__write_perm = False
        if mode == 's':
            pass
        else:
            self.__read_perm = True
            if mode == 'r':
                pass
            else:
                self.__append_perm = True
                elif mode == 'a':
                    pass
                elif mode == 'w':
                    self.__write_perm = True

        self.path = path if path[-1] == '/' else path + '/'
        self.dir = os.listdir(path)

    def full_path(self, file_name):
        return self.path + file_name

    def to_json(self):
        pass

    def work(self, r=False):
        pass

    def sort(self, classifier):
        pass

    def remove(self):
        pass

    def clean(self, r=False):
        pass

    def tree(self):
        pass

    def count(self, classifier, r=False):
        pass

    def size_stdev(self):
        mean = self.average_size()
        distance_total = sum((os.path.getsize(f) - mean) ** 2 for f in self)
        return (distance_total / len(self)) ** .5

    def average_size(self):
        return self.__sizeof__() / len(self)

    def __contains__(self, needle):
        """
            Recursively find a file. Use file_name in self.dir for lowest dir
            :param needle: file name to find
            :return: return path if file is found else False
        """
        pass

    def __add__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __iter__(self):
        for f in self.dir:
            yield(self.full_path(f))

    def __len__(self):
        return len(self.dir)

    def __sizeof__(self):
        return sum(os.path.getsize(f) for f in self)


if __name__ == '__main__':
    dir = Directory("test-dir", 'r')
    print(dir.path)
    print(dir.size_stdev())
