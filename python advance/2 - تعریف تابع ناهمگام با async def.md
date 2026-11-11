
تابع معمولی (`def`) و تابع ناهمگام (`async def`) در پایتون یک تفاوت بنیادین در نحوه اجرا دارند: **تابع معمولی با فراخوانی بلافاصله اجرا می‌شود، اما تابع `async def` با فراخوانی اجرا نمی‌شود؛ فقط بسته‌بندی می‌شود.**

  

### ۱. مقایسه رفتار در عمل

کد زیر را بررسی کنید تا تفاوت رفتار را ببینید:


``` python
# ۱. تابع معمولی (همگام / Synchronous)
def normal_func():
    print("تابع معمولی اجرا شد!")
    return 10

# ۲. تابع ناهمگام (Coroutine Function)
async def async_func():
    print("تابع ناهمگام اجرا شد!")
    return 20
```

حالا بیایید هر دو را مثل هم صدا بزنیم:

  


``` python
res1 = normal_func()
# خروجی در ترمینال: "تابع معمولی اجرا شد!"
print("نوع res1:", type(res1), "مقدار:", res1)
# خروجی: نوع res1: <class 'int'> مقدار: 10

print("-" * 30)

res2 = async_func()
# خروجی در ترمینال: هیچی چاپ نمی‌شود! متن داخل تابع اجرا نشد.
print("نوع res2:", type(res2), "مقدار:", res2)
# خروجی: نوع res2: <class 'coroutine'> مقدار: <coroutine object async_func at 0x...>
```

> **پیام هشدار پایتون:** اگر `res2 = async_func()` را بنویسید و رها کنید، پایتون اخطار می‌دهد:
> 
> `RuntimeWarning: coroutine 'async_func' was never awaited`
> 
> یعنی: «شما این کار را ساختید ولی هیچ‌وقت دستوری برای اجرای آن ندادید!»
> 
>   

### ۲. مفهوم کوروتین (Coroutine) چیست؟

وقتی کلمه `async` را پشت `def` می‌گذارید:

  

1. پایتون تابع شما را به یک **Coroutine Function** تبدیل می‌کند.
    
      
    
2. وقتی آن را فراخوانی می‌کنید (`()async_func`)، پایتون بدنه تابع را اجرا نمی‌کند، بلکه یک شیء **Coroutine Object** می‌سازد.
    
      
    
3. این شیء مثل یک «برگه مأموریت» یا «دستور کار مهروموم‌شده» است. تا زمانی که آن را با کلمه کلیدی `await` باز نکنید یا به Event Loop تحویل ندهید، حتی خط اول آن هم اجرا نخواهد شد.
    
      
    

### ۳. بررسی پشت صحنه با ماژول `inspect`

می‌توانید مستقیماً بررسی کنید که پایتون چطور نوع این توابع را تشخیص می‌دهد:

  


``` python
import inspect

def func_a():
    pass

async def func_b():
    pass

print(inspect.iscoroutinefunction(func_a))  # False
print(inspect.iscoroutinefunction(func_b))  # True

coro = func_b()
print(inspect.iscoroutine(coro))            # True
```

### ۴. چطور محتوای `async def` را وادار به اجرا کنیم؟

برای اینکه کد داخل یک کوروتین واقعاً خط‌به‌خط اجرا شود، باید به Event Loop اعلام شود. دو حالت وجود دارد:

  

**حالت الف: در فایل اسکریپت معمولی (`.py`) با دستور `asyncio.run`**

  



```Python
import asyncio

async def greet(name):
    print(f"سلام {name}!")
    return f"انجام شد برای {name}"

async def main():
    result = await greet("احسان")
    print(result)

# نقطه ورود برنامه
asyncio.run(main())
```

**حالت ب: در سلول ژوپیتر نوت‌بوک (بدون نیاز به `asyncio.run`)**

  

```python
# داخل سلول نوت‌بوک مستقیماً بنویسید:
result = await greet("احسان")
print(result)
```

### جمع‌بندی یک‌خطی

 پس `async def` کدی است که می‌گوید: **«من کاری هستم که ممکن است در طول اجرا متوقف شوم و منتظر بمانم، پس من را مستقیم اجرا نکن؛ بلکه یک شیء کوروتین بساز تا Event Loop زمان اجرای من را مدیریت کند.»**
