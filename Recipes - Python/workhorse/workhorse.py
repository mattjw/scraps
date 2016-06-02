"""

Workhorse:
python script.py --workhorse=1/3

Haystack of individual tasks. Same can task applied by any worker.

Worker completes multiple tasks.

Worker sets out to completes a subjob.
Job consists of subjobs.

Decompose job into subjobs.

Partitions the workload. Derives an id from anything hashable; e.g., list of
args.

Note: assumes that hashable equivalent constructed by this function is
uniformably distriuted in the hashspace. If not, then workload is not balanced.


kwarg only at the moment!

useful things:
grab the job_id after parsing, so you can crate your genfunc
to use this id (e.g., for multiple independent databases)
"""


import sys
import types
import argparse
import collections


def to_hashable(args):
    """
    Notes: The ordering of an OrderedDict will be ignored when obtaining
    its hash.
    """

    def rec(a):
        try:
            hash(a)
            return a  # case 0: `a` is already hashable
        except TypeError:
            pass

        if isinstance(a, types.DictType):
            # case 1: `a` is a dict
            seq = tuple((key, rec(a[key])) for key in sorted(a.iterkeys()))
            return seq
        else:
            try:
                it = iter(a)
            except TypeError:
                # case 2: `a` is a non-dictionary and not iterable
                return a

            # case 3: `a` is a non-dictionary iterable
            seq = tuple(map(rec, a))
            return seq

    ret = rec(args)
    return ret


class WorkSpec(object):
    
    def __init__(self, subjob_id, num_subjobs):
        """

        """
        if not (1 <= subjob_id <= num_subjobs):
            raise ValueError("job_id and num_jobs out of range")
        self.__subjob_id = subjob_id
        self.__num_subjobs = num_subjobs

    def get_subjob_id(self):
        return self.__subjob_id
        # consider @property?

    def get_num_subjobs(self):
        return self.__num_subjobs
        # consider @property?

    def do_task(self, **task_kwargs):
        """
        Returns True if the task, described by the input arguments, should
        be completed by this worker. The arguments should be immutable and
        hashable. This function will attempt to convert dictionaries and
        lists to equivalent hashable objects.
        """
        h = hash(to_hashable(task_kwargs))
        return (h % self.__num_subjobs) == (self.__subjob_id - 1)

    def run(self, taskgenfunc, execfunc):
        """
        Returns...
        job_tasks: Num tasks
        subjob_tasks: Num

        Optional use case.
        taskgenfunc: Generate (args, kwargs) pairs.
        execfunc: Executes a task.
        """
        job_tasks = 0
        subjob_tasks = 0

        for kwargs in taskgenfunc():
            job_tasks += 1

            if not isinstance(kwargs, collections.Mapping):
                raise ValueError("Expected `kwargs` to be mappable")

            if self.do_task(**kwargs):
                execfunc(**kwargs)
                subjob_tasks += 1

        return subjob_tasks, job_tasks

    def __str__(self):
        return "<WorkSpec: %s/%s>" % (self.__subjob_id, self.__num_subjobs)

    @staticmethod
    def from_argparse(args=None):
        """
        args: Use these as the input arguments for parsing. If None, use
        command-line args.
        Returns:
            Workspec
            unused atgs
        """
        parser = argparse.ArgumentParser(description="Handle arguments for Workhorse.")
        parser.add_argument('--workhorse', type=str,
                            default='1/1',
                            help='a subjob specification (e.g., 1/3)')
        namespace, unused = parser.parse_known_args(args)
        spec_str = namespace.workhorse

        p1, p2 = spec_str.strip().split('/')
        subjob_id = int(p1)
        num_subjobs = int(p2)

        workspec = WorkSpec(subjob_id, num_subjobs)
        return workspec, unused


def main():
    workspec, unused_args = WorkSpec.from_argparse()

    def genfunc():
        import itertools
        vocab = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn',
                 'uranus', 'neptune']
        for planets in itertools.permutations(vocab, 3):
            kwargs = {'planets': planets}
            yield kwargs
    
    def execfunc(planets):
        print planets

    print workspec.run(genfunc, execfunc)
    

def test():
    def test_make_hashable(args):
        as_hashable = to_hashable(args)
        print "orig = ", args
        print "\tas hashable =", as_hashable
        print "\thash        =", hash(as_hashable)
    test_make_hashable({'key1': [1, 2, 3]})
    test_make_hashable([{'key1': [1, 2, [3]]}, {'key2': {'key3': 8}}])
    test_make_hashable({})
    test_make_hashable((('mercury', 'venus', 'earth'), {}))



if __name__ == "__main__":
    #test()
    main()