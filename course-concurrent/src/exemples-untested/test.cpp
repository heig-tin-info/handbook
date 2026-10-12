void work(std::atomic<int>& a) {
  for(int i = 0; i < 100000; ++i) {
    a++;
  }
}


void singleThread() {
  // Create a single atomic integer
  std::atomic<int> a;
  a = 0;

  // Call the work function 4 times
  work(a);
  work(a);
  work(a);
  work(a);
}

struct alignas(64) AlignedType {
  AlignedType() { val = 0; }
  std::atomic<int> val;
};

void noSharing() {
  AlignedType a{};
  AlignedType b{};
  AlignedType c{};
  AlignedType d{};

  // Launch the four threads now using our aligned data
  std::thread t1([&]() { work(a.val); });
  std::thread t2([&]() { work(b.val); });
  std::thread t3([&]() { work(c.val); });
  std::thread t4([&]() { work(d.val); });

  // Join the threads
  t1.join();
  t2.join();
  t3.join();
  t4.join();
}

void directSharing() {
  // Create a single atomic integer
  std::atomic<int> a;
  a = 0;

  // Four threads all sharing one atomic<int>
  std::thread t1([&]() {work(a)});
  std::thread t2([&]() {work(a)});
  std::thread t3([&]() {work(a)});
  std::thread t4([&]() {work(a)});

  // Join the 4 threads
  t1.join();
  t2.join();
  t3.join();
  t4.join();
}

void falseSharing() {
  // Create a single atomic integer
  std::atomic<int> a;
  a = 0;
  std::atomic<int> b;
  b = 0;
  std::atomic<int> c;
  c = 0;
  std::atomic<int> d;
  d = 0;

  // Four threads each with their own atomic<int>
  std::thread t1([&]() {work(a)});
  std::thread t2([&]() {work(b)});
  std::thread t3([&]() {work(c)});
  std::thread t4([&]() {work(d)});

  // Join the 4 threads
  t1.join();
  t2.join();
  t3.join();
  t4.join();
}

void print() {
  std::atomic<int> a;
  std::atomic<int> b;
  std::atomic<int> c;
  std::atomic<int> d;

  // Print out the addresses
  std::cout << "Address of atomic<int> a - " << &a << '\n';
  std::cout << "Address of atomic<int> b - " << &b << '\n';
  std::cout << "Address of atomic<int> c - " << &c << '\n';
  std::cout << "Address of atomic<int> d - " << &d << '\n';
}