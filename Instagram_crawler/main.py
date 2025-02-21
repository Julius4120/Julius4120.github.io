from my_bot import InstaFollower
import time

Insta_bot = InstaFollower()

time.sleep(3)
Insta_bot.login()

time.sleep(10)
Insta_bot.find_followers()
print(Insta_bot.followers_number)


time.sleep(15)
Insta_bot.follow()



time.sleep(2)
Insta_bot.driver.quit()