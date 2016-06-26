import os
import sys
import ntpath


class Directory(object):

    def __init__(self, path, mode='r'):
        """
            Directory object for interaction with file collections
            :param path: path of directory
            :param mode: mode of interaction with directory
                's' - stat (only access file stats)
                'r' - read (only read files)
                'a' - append (only add files)
                'w' - write (add and remove files)
        """
        if not mode in ('s', 'r', 'a', 'w'):
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
                if mode == 'a':
                    pass
                elif mode == 'w':
                    self.__write_perm = True

        self.path = path if path[-1] == os.sep else path + os.sep
        self.dir = os.listdir(path)

    def full_path(self, file_name):
        return os.path.join(self.path, file_name)

    def head_walk(self):
        return os.walk(self.path).next()

    def to_dict(self, path=None):
        if path is None:
            path = self.path
        _dict = {}
        try:
            current_dir, availible_dirs, availible_files = os.walk(path).next()
        except StopIteration:
            return {path: []}
        _dict[current_dir] = [f for f in availible_files]
        for dir in availible_dirs:
            _dict[current_dir].append(self.to_dict(
                os.path.join(current_dir, dir)))
        return _dict

    def work(self, worker, r=False, args=tuple(), kwargs={}):
        if r is False:
            for f in self.head_walk()[-1]:
                worker(f, *args, **kwargs)
        elif r:
            for _, _, files in os.walk(self.path):
                for f in files:
                    worker(f, *args, **kwargs)

    def clean(self, r=False):
        def remove_if_empty(path):
            empty = os.path.getsize(f) == 0
            if empty:
                os.remove(f)
        self.work(remove_if_empty, r)

    def count(self, classifier, r=False, args=tuple(), kwargs={}):
        if r is False:
            return sum(1 for f in self.dir if classifier(f, *args, **kwargs))
        elif r:
            c = 0
            for _, _, files in os.walk(self.path):
                for f in files:
                    if classifier(f, *args, **kwargs):
                        c += 1
            return c

    def sort(self, classifier, r=False):
        pass

    def remove(self, path, r=False):
        if self.__write_perm == False:
            raise OSError("EPERM",
                          "There is not write permissions for {}".format(path
                                                                         ))

        head, tail = ntpath.split(path)
        if tail:
            self.dir.remove(tail)
        elif head:
            self.dir.remove(head)
            if r == False:
                raise ValueError(
                    "{} is a directory and must denote recursion".format(path))
        if r:
            os.rmdir(path)
        else:
            os.remove(path)

    def tree(self):
        pass

    def size_stdev(self):
        mean = self.average_size()
        distance_total = sum((os.path.getsize(f) - mean) ** 2 for f in self)
        return (distance_total / len(self)) ** .5

    def average_size(self):
        return self.__sizeof__() / len(self)

    def find(self, needle):
        """
            Recursively find a file.
            :param needle: file name to find
            :return: return path if file is found else False
        """
        for current_dir, availible_dirs, availible_files in os.walk(self.path):
            if needle in availible_files:
                return os.path.join(current_dir, needle)
            if needle in availible_dirs:
                return os.path.join(current_dir, needle)

        return False

    def __contains__(self, needle):
        """
            Recursively find a file. Use file_name in self.dir for lowest dir
            :param needle: file name to find
            :return: return True if file is found else False
        """

        return self.find(needle)  # automatically converted to bool

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
    print(dir.to_dict())
    print(dir.find("1000-primes.txt"))
    print(dir.find("1001-primes.txt"))
    print(dir.find("bruno.txt"))
    print(dir.find("even-more-files"))
    print(dir.find("more-files"))
    print(dir.find("fake-folder"))
