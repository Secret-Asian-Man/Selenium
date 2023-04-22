#https://www.youtube.com/playlist?list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ
import winsound
import time
import random

import smtplib, ssl # for sending email

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC

TARGET_DATE = ""
WEBSITE = r""

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
emailSender = ""  # Enter your address
emailRecievers = [""]
password = ""
message = """\
Archery tickets are available! GOGOGOGOGO!!!/"""

PATH = r".\chromedriver.exe"
driver = webdriver.Chrome(PATH)
cardsClassName = "card-outer"
cardClassName = "new-cards-content"
selectedCard = None

driver.get(WEBSITE)

try:
  while (selectedCard == None): # while the card is not found
    REFRESH_RATE = random.randint(3,9) # check every 3 to 9 seconds

    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, cardsClassName)) # get all cards
    )

    # Search for the card with the target date
    cards = main.find_elements(By.CLASS_NAME, cardClassName)
    for card in cards:
      if (card.text.find(TARGET_DATE) != -1):
        selectedCard = card

    # If a card was found, click the button
    if (selectedCard):
      # Reserve the tickets (TODO: Need example of webpage with available tickets)
      selectedCard.find_element(By.CLASS_NAME, "btn").click()

      # Send email alerts
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(emailSender, password)
        for reciever in emailRecievers:
          server.sendmail(emailSender, reciever, message)

      # Alert the user
      while (selectedCard):
        winsound.Beep(random.randint(500,3000), 500)
    else:
      # Refresh the page. Keep searching
      driver.refresh()
      time.sleep(REFRESH_RATE)
finally:
    driver.quit()