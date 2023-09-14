from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
import time

def links_related_to_my_history(new_word=None): 

    """ If new_word has value:
            search that value in Edge 
            get 3 links for websites related to new_word and add to three_links list
            most_common_links dictionary will contain: 
                key = new_word 
                value = three_links list
        
        else:
            Find 3 links of websites related to each searched result from history
            most_common_links dictionary will contain :
                key = each searched keyword from history 
                value = three_links list of each searched keyword from history
        """
    
    most_common_links = {} 

    driver = Edge() 
    driver.get("https://www.bing.com/#!")
    time.sleep(3) 

    search_bar = driver.find_element(By.ID, "sb_form_q") 
    search_bar.click()
    time.sleep(3)

    if new_word is not None: 
        
        search_bar.send_keys(new_word) 
        search_bar.submit()
        time.sleep(3)

        search_results = driver.find_elements(By.CLASS_NAME, "b_algo")

        three_links = []

        for result in search_results:
            attribution_elements = result.find_elements(By.CLASS_NAME, "b_attribution") 
            for attribution_element in attribution_elements:
                cite_element = attribution_element.find_element(By.TAG_NAME, "cite") # Finding websites routes (<cite>) 
                cite_value = cite_element.text # Converting with .text for better form
                if cite_value and len(three_links) < 3: 
                    three_links.append(cite_value)

        most_common_links[new_word] = three_links # dict with searched keyword and list of three links


    else: 
    
        scroll_content = driver.find_element(By.CLASS_NAME, "sa_nestedList") 

        print("\nYour last search was:")
        print(scroll_content.text)

        history_list = scroll_content.text.split("\n")

        for search_text in history_list:

            search_bar = driver.find_element(By.ID, "sb_form_q")
            search_bar.clear()
            search_bar.send_keys(search_text)
            search_bar.submit()

            time.sleep(3)

            search_results = driver.find_elements(By.CLASS_NAME, "b_algo")

            three_links = []

            for result in search_results:
                attribution_elements = result.find_elements(By.CLASS_NAME, "b_attribution")
                for attribution_element in attribution_elements:
                    cite_element = attribution_element.find_element(By.TAG_NAME, "cite")
                    cite_value = cite_element.text
                    if cite_value and len(three_links) < 3:
                        three_links.append(cite_value)

            most_common_links[search_text] = three_links

    # Presenting content from most_common_links
    for search_text, cites in most_common_links.items():
        print(f"\nTop 3 websites values after searching for '{search_text}':")
        for cite_value in cites:
            print(cite_value)

    # Closing WebDriver
    driver.quit()

print("""
    Enter number 1 for: "Finding 3 recommended links for each keyword in my search history"

    Enter number 2 for: "Adding a new keyword and finding 3 best related links"
""")

option = input("Please select an option: ")

if option in ['1', '2']:
    if option == '1':
        links_related_to_my_history()
    else:
        word_to_search = input("Enter your word: ")
        links_related_to_my_history(new_word=word_to_search) # Replacing default value of new_word in function
