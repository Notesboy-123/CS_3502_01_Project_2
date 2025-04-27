import random
class Process:
    def __init__(self, id, arrival_time, burst_time):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def srtf(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    busy_time = 0

    while completed < n:
        runnable = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        if runnable:
            process = min(runnable, key=lambda x: x.remaining_time)
            process.remaining_time -= 1
            current_time += 1
            busy_time += 1

            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                completed += 1
        else:
            current_time += 1

    total_time = current_time
    cpu_utilization = (busy_time / total_time) * 100 if total_time > 0 else 0
    throughput = n / total_time if total_time > 0 else 0

    return cpu_utilization, throughput


def hrrn(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    busy_time = 0

    while completed < n:
        runnable = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        if runnable:
            for p in runnable:
                p.response_ratio = (current_time - p.arrival_time + p.burst_time) / p.burst_time

            process = max(runnable, key=lambda x: x.response_ratio)
            busy_time += process.burst_time
            current_time += process.burst_time
            process.remaining_time = 0
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed += 1
        else:
            current_time += 1

    total_time = current_time
    cpu_utilization = (busy_time / total_time) * 100 if total_time > 0 else 0
    throughput = n / total_time if total_time > 0 else 0

    return cpu_utilization, throughput


def print_results(processes, cpu_utilization, throughput, algorithm):
    total_wt = total_tat = 0
    print(f"\nResults for {algorithm}:")
    print("Process | CT  | WT  | TAT")
    for p in sorted(processes, key=lambda x: x.id):
        total_wt += p.waiting_time
        total_tat += p.turnaround_time
        print(f"P{p.id:4}   | {p.completion_time:3} | {p.waiting_time:3} | {p.turnaround_time:3}")
    #print(len(processes))
    print(f"\nAverage Waiting Time: {total_wt / len(processes):.2f}")
    print(f"Average Turnaround Time: {total_tat / len(processes):.2f}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Throughput: {throughput:.4f} processes per unit time")


def main():
    try:
        n = random.randint(1,20)

        processes = []
        for i in range(n):
            arrival = random.randint(0,0)
            burst = random.randint(1,1000)
            processes.append(Process(i + 1, arrival, burst))
        processes2 = processes[:]
        processes_srtf = [Process(p.id, p.arrival_time, p.burst_time) for p in processes]
        processes_hrrn = [Process(p.id, p.arrival_time, p.burst_time) for p in processes2]

        print("\n=== SRTF Scheduling ===")
        cpu_utilization_srtf, throughput_srtf = srtf(processes_srtf)
        print_results(processes_srtf, cpu_utilization_srtf, throughput_srtf, "SRTF")

        print("\n=== HRRN Scheduling ===")
        cpu_utilization_hrrn, throughput_hrrn = hrrn(processes_hrrn)
        print_results(processes_hrrn, cpu_utilization_hrrn, throughput_hrrn, "HRRN")
    except ValueError:
        print("Invalid input. Please enter integers only.")


if __name__ == "__main__":
    main()
