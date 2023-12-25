import re
import threading

class SearchResult:
    def __init__(self, line_number, sentence):
        self.line_number = line_number
        self.sentence = sentence

class ParallelGrep:
    def __init__(self, file_path, query, num_threads=2):
        self.file_path = file_path
        self.query = query
        self.num_threads = num_threads

    def run_parallel_grep(self):
        file_content = self.read_file()
        partitions = self.partition_file(file_content, self.num_threads)

        threads = []
        results = []

        for i in range(self.num_threads):
            thread = threading.Thread(target=self.search_in_partition, args=(partitions[i], i + 1, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def read_file(self):
        with open(self.file_path, 'r') as file:
            return file.readlines()

    def partition_file(self, content, num_partitions):
        total_len = len(content)
        part_len = total_len // num_partitions
        return [content[i:i + part_len] for i in range(0, total_len, part_len)]

    def search_in_partition(self, partition, thread_number, results):
        for i, line in enumerate(partition, start=1):
            matches = re.finditer(self.query, line)
            for match in matches:
                result = SearchResult(line_number=(i + (thread_number - 1) * len(partition)), sentence=line)
                results.append(result)

if __name__ == '__main__':
    file_path = input("Enter file path: ")
    query = input("Enter search query: ")

    parallel_grep = ParallelGrep(file_path, query)
    search_results = parallel_grep.run_parallel_grep()

    print("Search Results:")
    for result in search_results:
        print(f"Found '{query}' at line {result.line_number}: {result.sentence.strip()}")
