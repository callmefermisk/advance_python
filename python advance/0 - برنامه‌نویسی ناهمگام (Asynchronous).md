
برنامه‌نویسی ناهمگام (Asynchronous) ابزاری برای مدیریت عملیات‌هایی است که منتظر پاسخ می‌مانند، بدون اینکه کل برنامه متوقف (بلاک) شود.


### ۱. کارهای I/O-bound در برابر CPU-bound

قبل از نوشتن کد، باید بدانیم `asyncio` چه مشکلی را حل می‌کند:

- درگیری **CPU-bound:** کارهایی که پردازنده را به شدت درگیر محاسبات می‌کنند (مانند رمزنگاری، فشرده‌سازی ویدیو، ضرب ماتریس‌ها). راهکار این کارها `Multiprocessing` است، نه `asyncio`.
    
- درگیری **I/O-bound:** کارهایی که پردازنده کاری انجام نمی‌دهد و فقط منتظر ورودی/خروجی بیرونی است (مانند درخواست HTTP، خواندن فایل، کوئری دیتابیس). راهکار ایده‌آل این کارها `asyncio` است.

پس برای کارهای مولتی پروسسینگ نباید از asyncio استفاده کرد.

[[2 - تعریف تابع ناهمگام با async def]]

قرار دادن کلمه `async` قبل از `def` تابعی می‌سازد که به آن **Coroutine** (کوروتین) گفته می‌شود. اجرای مستقیم این تابع کد داخل آن را اجرا نمی‌کند، بلکه فقط یک شیء کوروتین برمی‌گرداند.
``` python
async def fetch_user():
    print("شروع دریافت کاربر...")
    return {"id": 1, "name": "Ali"}

# فراخوانی مستقیم:
result = fetch_user()
print(result)  # خروجی: <coroutine object fetch_user at 0x...>
```



### ۳. مدیریت برنامه با Event Loop و `asyncio.run()` 
باید بدانید که **Event Loop** مثل یک مدیر کارگاه است؛ کارها را زیر نظر می‌گیرد و هر زمان کاری وارد حالت انتظار شد، پردازش را به کار بعدی می‌دهد.

تابع `asyncio.run()` حلقه رویداد (Event Loop) را می‌سازد، کوروتین اصلی را تا پایان اجرا می‌کند و سپس حلقه را تمیز می‌بندد:

```python 
import asyncio

async def main():
    print("سلام از دنیای Async!")

# اجرای رسمی کوروتین:
asyncio.run(main())
```

### ۴. انتظار غیرمسدودکننده با `await`

کلمه کلیدی `await` فقط داخل توابع `async def` کار می‌کند. معنی آن این است: _«صبر کن تا این عملیات تمام شود، اما تا آن زمان کنترل را به Event Loop بده تا کارهای دیگر را پیش ببرد.»_

Python

``` python
import asyncio

async def get_data():
    return "اطلاعات دریافت شد"

async def main():
    # بدون await مقدار واقعی را نمی‌گیرید
    data = await get_data()
    print(data)

asyncio.run(main())
```

### ۵. تفاوت `asyncio.sleep()` و `time.sleep()`

- یک `time.sleep(n)` کل رشته اجرایی (Thread) و پردازنده را قفل می‌کند؛ هیچ کد دیگری در حلقه اجرا نمی‌شود.
    
-  دو `asyncio.sleep(n)` یک وقفه ناهمگام است؛ به Event Loop می‌گوید به مدت $n$ ثانیه به کارهای دیگر رسیدگی کند.
    
```python
import asyncio
import time

async def worker_blocking(num):
    print(f"شروع مسدودکننده {num}")
    time.sleep(1)  # کل برنامه را ۱ ثانیه فریز می‌کند
    print(f"پایان مسدودکننده {num}")

async def worker_non_blocking(num):
    print(f"شروع غیرمسدودکننده {num}")
    await asyncio.sleep(1)  # کنترل را واگذار می‌کند
    print(f"پایان غیرمسدودکننده {num}")
```

### ۶ و ۷. اجرای همزمان با `asyncio.gather()`

اگر چند کوروتین را تک‌به‌تک `await` کنید، به صورت ترتیبی اجرا می‌شوند. برای اجرای موازی و همزمان آن‌ها روی همان یک رشته، از `asyncio.gather()` استفاده می‌شود.

کد زیر مقایسه اجرای ترتیبی در برابر همزمان با `gather` را نشان می‌دهد:



```Python
import asyncio
import time

async def download_file(file_id, delay):
    print(f"[شروع] دانلود فایل {file_id}...")
    await asyncio.sleep(delay)  # شبیه‌سازی دانلود اینترنتی
    print(f"[اتمام] دانلود فایل {file_id}!")
    return f"محتوای فایل {file_id}"

async def main():
    start_time = time.time()

    # ارسال همزمان سه کار به Event Loop
    results = await asyncio.gather(
        download_file("A", 2),
        download_file("B", 3),
        download_file("C", 1)
    )

    elapsed = time.time() - start_time
    print(f"\nهمه دانلودها در {elapsed:.2f} ثانیه تمام شدند.")
    print("خروجی‌ها:", results)

asyncio.run(main())
```

**نحوه رفتار در خروجی:**

1. هر ۳ دانلود بلافاصله شروع می‌شوند.
    
2. بعد از ۱ ثانیه، فایل C تمام می‌شود.
    
3. بعد از ۲ ثانیه، فایل A تمام می‌شود.
    
4. بعد از ۳ ثانیه، فایل B تمام می‌شود.
    
5. کل زمان اجرای برنامه به جای $1 + 2 + 3 = 6$ ثانیه، حدود **۳ ثانیه** (طولانی‌ترین تسک) خواهد بود.