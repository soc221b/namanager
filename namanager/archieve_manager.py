import os
import shutil


class ArchieveManager():
    """
    Strategy:
        1. file rename first
        2. deeper first
    """

    def rename(self, path_pairs):
        """rename
        :param path_pairs:
        :type path_pairs: list of tuple, e.g., [(src, dst)]
        """
        file_pairs, dir_pairs = (
            self._separate_file_dir_from_path_pair(path_pairs))
        self.rename_file(file_pairs)
        self.rename_dir(dir_pairs)

    def rename_file(self, file_pairs):
        file_pairs = self._sort_path_pair(file_pairs, reverse=True)
        for src, dst in file_pairs:
            shutil.move(src, dst)

    def rename_dir(self, dir_pairs):
        dir_pairs = self._sort_path_pair(dir_pairs, reverse=True)
        for src, dst in dir_pairs:
            shutil.move(src, dst)

    def _separate_file_dir_from_path_pair(self, path_pairs):
        file_pairs = []
        dir_pairs = []

        for pair in path_pairs:
            if os.path.isfile(pair[0]):
                file_pairs.append(pair)
            elif os.path.isdir(pair[0]):
                dir_pairs.append(pair)

        return file_pairs, dir_pairs

    def _sort_path_pair(self, path_pairs, **kwargs):
        reverse = kwargs.get('reverse', False)

        path_pairs = path_pairs[:]
        counted_path_pairs = []
        for pair in path_pairs:
            counted_path_pairs.append(
                [pair[0], pair[1], len(pair[0].split(os.sep))])
        counted_path_pairs.sort(
            key=lambda p: p[2] if os.path.isdir(p[0]) else p[2] - 1,
            reverse=reverse)

        sorted_ = []
        for pair in counted_path_pairs:
            sorted_.append((pair[0], pair[1]))

        return sorted_
