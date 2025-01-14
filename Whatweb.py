from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_contacts():
    print("\n=== Contact Input ===")
    print("Enter contacts one per line. Press Enter twice to finish.")
    contacts = []
    while True:
        contact = input()
        if contact == "":
            break
        contacts.append(contact)
    return contacts

def get_message():
    print("\n=== Message Input ===")
    return input("Enter your message: ")

def send_whatsapp(contacts, message):
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    
    print("\nScan QR code now!")
    input("Press Enter after scanning...")
    
    successful = []
    failed = []

    for contact in contacts:
        try:
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)

            msg_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            msg_box.send_keys(message)
            msg_box.send_keys(Keys.ENTER)
            
            msg_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(2)
            
            successful.append(contact)
            print(f"✓ Sent to {contact}")
            
        except Exception as e:
            failed.append(contact)
            print(f"✗ Failed to send to {contact}")
            
        time.sleep(5)

    print(f"\nSuccessful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    with open("enviados.txt", "w") as f:
        f.write("\n".join(successful))
    with open("no_enviados.txt", "w") as f:
        f.write("\n".join(failed))
        
    driver.quit()

def main():
    print("WhatsApp Automation")
    print("==================")
    
    contacts = get_contacts()
    message = get_message()
    
    print(f"\nReady to send to {len(contacts)} contacts")
    input("Press Enter to start...")
    
    send_whatsapp(contacts, message)

if __name__ == "__main__":
    main()