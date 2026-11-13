
در **مورد ۵**، تفاوت میان `asyncio.sleep()` و `time.sleep()` را بررسی می‌کنیم. درک این تفاوت بسیار حیاتی است، چون استفاده اشتباه از `time.sleep()` درون یک تابع `async` می‌تواند کل مزایای برنامه‌نویسی ناهمگام را از بین ببرد.

  

### تفاوت اصلی در یک نگاه

- یک **`time.sleep(seconds)` (Blocking / مسدودکننده):** مستقیماً به سیستم‌عامل می‌گوید کل **Thread (رشته اجرایی)** فعلی را برای چند ثانیه متوقف کند. در این مدت، **Event Loop کاملاً قفل می‌شود** و هیچ تسک دیگری حتی اگر آماده اجرا باشد، فرصت اجرا پیدا نمی‌کند.
    
      
    
- دو  **`asyncio.sleep(seconds)` (Non-blocking / غیرمسدودکننده):** یک شیء Awaitable می‌سازد که به Event Loop می‌گوید: _«من تا $n$ ثانیه دیگر کاری ندارم؛ تو در این فاصله برو سراغ تسک‌های دیگر و وقتی زمانم تمام شد دوباره من را بیدار کن.»_
    
      
    

### آزمایش عملی: مقایسه دو حالت در کد

در کد زیر، هر دو تابع با `asyncio.create_task` به صورت همزمان ثبت شده‌اند، اما به دلیل استفاده از `time.sleep(3)` در تابع اول، تابع دوم هم مجبور به صبر می‌شود:

  



```python
import asyncio
import time

async def blocking_task():
    print("[BLOCKING] Started (using time.sleep)...")
    time.sleep(3)  # Freezes the entire Event Loop for 3 seconds!
    print("[BLOCKING] Finished!")

async def fast_task():
    print("[FAST] Started (using asyncio.sleep)...")
    await asyncio.sleep(1)
    print("[FAST] Finished!")

async def main():
    start_time = time.time()

    # Schedule both tasks concurrently
    t1 = asyncio.create_task(blocking_task())
    t2 = asyncio.create_task(fast_task())

    await t1
    await t2

    print(f"Total elapsed time: {time.time() - start_time:.2f}s")

# Run in Jupyter Notebook:
await main()
```

**خروجی و تحلیل:**

  

1. یک `[BLOCKING] Started...`چاپ می‌شود و بلافاصله `time.sleep(3)` کل حلقه رویداد را منجمد می‌کند.
    
      
    
2. تابع `fast_task` حتی نمی‌تواند پیام شروع خود را چاپ کند تا زمانی که ۳ ثانیه تمام شود!
    
      
    
3. کل زمان اجرای برنامه به جای ۳ ثانیه، حدود **۴ ثانیه** ($3 + 1$) می‌شود.
    
      
    

### تمرین‌های عملی مورد ۵

این دو تمرین را کدنویسی کن تا رفتار هر دو دستور را در عمل ببینی:

  

#### Exercise 1: Fix the Frozen Event Loop

کد آزمایش بالا را در نوت‌بوک خودت کپی کن و تغییر بده:

  

1. داخل `blocking_task`، دستور `time.sleep(3)` را با `await asyncio.sleep(3)` جایگزین کن (نام تابع را هم به `non_blocking_task` تغییر بده).
    
      
    
2. کد را اجرا کن و ببین چطور `fast_task` در ثانیه اول تمام می‌شود و زمان کل برنامه از ۴ ثانیه به **۳.۰۰ ثانیه** کاهش پیدا می‌کند.
    
      
    

#### Exercise 2: Clock vs. Heavy Freeze (ساعت زنده در برابر فریز شدن)

یک برنامه با دو تسک همزمان بنویس:

  

1. تابع `live_clock(ticks)`: یک حلقه بساز که به تعداد `ticks` (مثلاً ۵ بار)، هر `0.5` ثانیه (`await asyncio.sleep(0.5)`) پیام `f"Clock tick {i}"` را چاپ کند.
    
      
    
2. تابع `api_request()`: یک بار با `time.sleep(2)` و یک بار با `await asyncio.sleep(2)` شبیه‌سازی کن که درخواست شبکه ۲ ثانیه طول می‌کشد.
    
      
    
3. هر دو تسک را با `asyncio.create_task` در `main()` اجرا کن و ببین در هر دو حالت چه بلایی سر تیک‌های ساعت می‌آید.
    
      
    

کد تمرین‌ها را بنویس و بفرست تا بررسی کنیم.

در **مورد ۵**، تفاوت میان `asyncio.sleep()` و `time.sleep()` را بررسی می‌کنیم. درک این تفاوت بسیار حیاتی است، چون استفاده اشتباه از `time.sleep()` درون یک تابع `async` می‌تواند کل مزایای برنامه‌نویسی ناهمگام را از بین ببرد.

  

### تفاوت اصلی در یک نگاه

- اینکه **`time.sleep(seconds)` (Blocking / مسدودکننده):** مستقیماً به سیستم‌عامل می‌گوید کل **Thread (رشته اجرایی)** فعلی را برای چند ثانیه متوقف کند. در این مدت، **Event Loop کاملاً قفل می‌شود** و هیچ تسک دیگری حتی اگر آماده اجرا باشد، فرصت اجرا پیدا نمی‌کند.
    
      
    
- اینکه **`asyncio.sleep(seconds)` (Non-blocking / غیرمسدودکننده):** یک شیء Awaitable می‌سازد که به Event Loop می‌گوید: _«من تا $n$ ثانیه دیگر کاری ندارم؛ تو در این فاصله برو سراغ تسک‌های دیگر و وقتی زمانم تمام شد دوباره من را بیدار کن.»_
    
      
    

### آزمایش عملی: مقایسه دو حالت در کد

در کد زیر، هر دو تابع با `asyncio.create_task` به صورت همزمان ثبت شده‌اند، اما به دلیل استفاده از `time.sleep(3)` در تابع اول، تابع دوم هم مجبور به صبر می‌شود:

  



```Python
import asyncio
import time

async def blocking_task():
    print("[BLOCKING] Started (using time.sleep)...")
    time.sleep(3)  # Freezes the entire Event Loop for 3 seconds!
    print("[BLOCKING] Finished!")

async def fast_task():
    print("[FAST] Started (using asyncio.sleep)...")
    await asyncio.sleep(1)
    print("[FAST] Finished!")

async def main():
    start_time = time.time()

    # Schedule both tasks concurrently
    t1 = asyncio.create_task(blocking_task())
    t2 = asyncio.create_task(fast_task())

    await t1
    await t2

    print(f"Total elapsed time: {time.time() - start_time:.2f}s")

# Run in Jupyter Notebook:
await main()
```

**خروجی و تحلیل:**

  

1. ا `[BLOCKING] Started...` چاپ می‌شود و بلافاصله `time.sleep(3)` کل حلقه رویداد را منجمد می‌کند.
    
      
    
2. تابع `fast_task` حتی نمی‌تواند پیام شروع خود را چاپ کند تا زمانی که ۳ ثانیه تمام شود!
    
      
    
3. کل زمان اجرای برنامه به جای ۳ ثانیه، حدود **۴ ثانیه** ($3 + 1$) می‌شود.
    
      
    



