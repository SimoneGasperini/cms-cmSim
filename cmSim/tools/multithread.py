from threading import Thread
from queue import Queue
from time import sleep


class Worker(Thread):

    def __init__(self, tasks_queue, max_attempts=3):
        super().__init__()
        self.tasks_queue = tasks_queue
        self.max_attempts = max_attempts
        self.results_dict = {}
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, arg = self.tasks_queue.get()
            for attempt in range(self.max_attempts):
                try:
                    res = func(arg)
                    if res:
                        self.results_dict[arg] = res
                    self.tasks_queue.task_done()
                    break
                except Exception as exception:
                    if attempt == self.max_attempts-1:
                        print(exception)
                        self.tasks_queue.task_done()
                    else:
                        sleep((attempt + 1) * 3)


class ThreadPool:

    def __init__(self, num_threads):
        self.tasks_queue = Queue(num_threads)
        self.workers = []
        for _ in range(num_threads):
            worker = Worker(self.tasks_queue)
            self.workers.append(worker)

    def map(self, func, sequence):
        for arg in sequence:
            self.tasks_queue.put((func, arg))

    def get_result(self):
        self.tasks_queue.join()
        result = {}
        for worker in self.workers:
            result = {**result, **worker.results_dict}
        return result


if __name__ == '__main__':

    from time import time
    import pandas as pd
    from cmSim.tools.mcm_rest import McM

    def run_sequential(datasets_names):
        mcm = McM()
        result = {}
        for dataset_name in datasets_names:
            data = mcm.get_by_dataset_name(dataset_name)
            if data:
                result[dataset_name] = data
        return result

    def run_multithread(datasets_names, num_threads=4):
        mcm = McM()
        thread_pool = ThreadPool(num_threads=num_threads)
        thread_pool.map(func=mcm.get_by_dataset_name,
                        sequence=datasets_names)
        result = thread_pool.get_result()
        return result

    num = 100
    df = pd.read_parquet('./../../data/dataset_size_info.parquet')[-num:]
    datasets_names = df['d_dataset'].tolist()

    print('\n1) SEQUENTIAL REQUESTS TO MCM...')
    start1 = time()
    result1 = run_sequential(datasets_names)
    end1 = time()
    print(f'Elapsed time for {num} queries: {end1 - start1} secs')

    num_threads = 4
    print(f'\n2) MULTITHREAD REQUESTS TO MCM ({num_threads} threads)...')
    start2 = time()
    result2 = run_multithread(datasets_names, num_threads=num_threads)
    end2 = time()
    print(f'Elapsed time for {num} queries: {end2 - start2} secs')

    print(f'\nresult1 == result2: {result1 == result2}')
