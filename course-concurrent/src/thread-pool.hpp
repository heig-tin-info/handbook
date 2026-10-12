#pragma once

#include <atomic>
#include <condition_variable>
#include <functional>
#include <future>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

class ThreadPool
{
   public:
    ThreadPool(size_t numThreads) : stop(false), stopImmediately(false)
    {
        resize(numThreads);
    }

    ~ThreadPool() { shutdown(); }

    template <class F, class... Args>
    auto enqueue(int priority, F&& f, Args&&... args)
        -> std::future<typename std::result_of<F(Args...)>::type>
    {
        using returnType = typename std::result_of<F(Args...)>::type;

        auto task = std::make_shared<std::packaged_task<returnType()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...));

        std::future<returnType> result = task->get_future();
        {
            std::unique_lock<std::mutex> lock(queueMutex);

            if (stop || stopImmediately) {
                throw std::runtime_error("enqueue on stopped ThreadPool");
            }

            tasks.emplace(priority, [task]() { (*task)(); });
        }
        condition.notify_one();
        return result;
    }

    void shutdown()
    {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            stop = true;
        }

        condition.notify_all();

        for (std::thread& worker : workers) {
            worker.join();
        }
        workers.clear();
    }

    void shutdownNow()
    {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            stopImmediately = true;
        }

        condition.notify_all();

        for (std::thread& worker : workers) {
            worker.detach();
        }
        workers.clear();
    }

    void resize(size_t numThreads)
    {
        shutdown();
        stop = false;
        stopImmediately = false;
        for (size_t i = 0; i < numThreads; ++i) {
            workers.emplace_back(&ThreadPool::workerThread, this);
        }
    }

   private:
    struct Task {
        int priority;
        std::function<void()> func;

        Task(int p, std::function<void()> f) : priority(p), func(f) {}

        bool operator<(const Task& other) const
        {
            return priority < other.priority;
        }
    };

    std::vector<std::thread> workers;
    std::priority_queue<Task> tasks;

    std::mutex queueMutex;
    std::condition_variable condition;
    std::atomic<bool> stop;
    std::atomic<bool> stopImmediately;

    void workerThread()
    {
        while (true) {
            Task task(0, [] {});
            {
                std::unique_lock<std::mutex> lock(queueMutex);

                condition.wait(lock, [this]() {
                    return stopImmediately || stop || !tasks.empty();
                });

                if ((stop && tasks.empty()) || stopImmediately) {
                    return;
                }

                task = std::move(tasks.top());
                tasks.pop();
            }

            task.func();
        }
    }
};
