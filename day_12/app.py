import asyncio
async def prepare_system():
    print("you are in the prepare_system")
    return "System Ready"

async def main():
    status = await prepare_system()
    print("Status : ",status)

async def check_loop_status():
    loop = asyncio.get_running_loop()

    start_time = loop.time()
    print("start time is:",start_time)

    print("await time in 1.5 second")
    await asyncio.sleep(1.5)
    
    end_time =loop.time()
    print("end time is :",end_time)

    elapsed = end_time - start_time
    print("time passed is :", elapsed)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(check_loop_status())
    

   