import heapq

def calculate_service_time(n, k, t):
    queue = []
    time = 0

    for i in range(k):
        heapq.heappush(queue, (0, i))

    for i in range(n):
        service_time, cash_register = heapq.heappop(queue)
        service_time += t[i]
        time = max(time, service_time)
        heapq.heappush(queue, (service_time, cash_register))

    return time



n, k = map(int, input().split())
t = list(map(int, input().split()))


result = calculate_service_time(n, k, t)
print(result)
