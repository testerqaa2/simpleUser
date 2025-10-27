from playwright.sync_api import sync_playwright

def high_low_price():
    """Test Sorting on both Chrome and Firefox"""
    browsers = ['chromium', 'firefox']
    
    for browser_type in browsers:
        with sync_playwright() as p:
            if browser_type == 'chromium':
                browser = p.chromium.launch(headless=False)
                browser_name = "Chrome"
            else:
                browser = p.firefox.launch(headless=False)
                browser_name = "Firefox"
                
            context = browser.new_context()
            page = context.new_page()
            
            try:
                print(f"\n=== Testing on {browser_name} ===")
                
                page.goto("https://www.saucedemo.com/")
                print(f"1. Open Web")

                username = ("standard_user")
                password = ("secret_sauce")

                page.fill("#user-name", username)
                print(f"2. Input valid username")
                page.fill("#password",password)
                print(f"3. Input valid password")
                login_btn = page.locator("#login-button")
                login_btn.click()
                print(f"4. Click login button")
                page.wait_for_timeout(1000)
                print(f"✅ User successfully logged into account")

                actual_page = page.locator("[data-test='title']").inner_text().strip()
                expected_page = "Products"

                print(f"5. Verify actual page after login")
                assert actual_page == expected_page, \
                    f"Actual page isn't as expected. Current: '{actual_page}', Expected: '{expected_page}'"
                print(f"💡 Actual page is : '{expected_page}'")

                first_product_name = page.locator("#item_4_title_link").inner_text().strip()
                expected_first_product_name = "Sauce Labs Backpack"

                print(f"6. Verify one product name")
                assert first_product_name == expected_first_product_name, \
                    f"Product name isn't as expected. Current: '{first_product_name}', Expected: '{expected_first_product_name}'"
                print(f"💡 Product name is : '{expected_first_product_name}'")

                price_locator = page.locator("[data-test='inventory-item-price']")

                expected_first_price_before = ("$29.99")
                expected_second_price_before = ("$9.99")
                expected_last_price_before = ("$15.99")

                actual_first_price = price_locator.first.inner_text()
                assert actual_first_price.strip() == expected_first_price_before, \
                f"First price mismatch! Current: '{actual_first_price}', Expected: '{expected_first_price_before}'"
                print(f"7. [Before] First Product price: {actual_first_price}")
         
                actual_second_price = price_locator.nth(1).inner_text()
                assert actual_second_price.strip() == expected_second_price_before, \
                f"Second price mismatch! Current: '{actual_second_price}', Expected: '{expected_second_price_before}'"
                print(f"8. [Before] Second Product price: {actual_second_price}")

                actual_last_price = price_locator.nth(5).inner_text()
                assert actual_last_price.strip() == expected_last_price_before, \
                f"Last price mismatch! Current: '{actual_last_price}', Expected: '{expected_last_price_before}'"
                print(f"9. [Before] Last Product price: {actual_last_price}")

                print("✅ All prices are as expected!")

                print("10. Select from High to Low Price")
                page.select_option(".product_sort_container", "hilo")

                active_option = page.locator(".active_option").inner_text().strip()
                expected_option = ("Price (high to low)") 

                print("11. Verify option selected")

                expected_first_price_after = ("$49.99")
                expected_second_price_after = ("$29.99")
                expected_last_price_after = ("$7.99")

                assert active_option == expected_option, \
                f"Option selected isn't as expected. Current: '{active_option}' , Expected: '{expected_option}'"    
                print(f"💡 Option selected is : '{expected_option}'")

                print("12. Verify result High to Low Price")
                actual_first_price = price_locator.first.inner_text()

                assert actual_first_price.strip() == expected_first_price_after, \
                f"First price mismatch! Current: '{actual_first_price}', Expected: '{expected_first_price_after}'"
                print(f"13. [After] First Product price: {actual_first_price}")
         
                actual_second_price = price_locator.nth(1).inner_text()
                assert actual_second_price.strip() == expected_second_price_after, \
                f"Second price mismatch! Current: '{actual_second_price}', Expected: '{expected_second_price_after}'"
                print(f"14. [After] Second Product price: {actual_second_price}")

                actual_last_price = price_locator.nth(5).inner_text()
                assert actual_last_price.strip() == expected_last_price_after , \
                f"Last price mismatch! Current: '{actual_last_price}', Expected: '{expected_last_price_after}'"
                print(f"15. [After] Last Product price: {actual_last_price}")

            finally:
                browser.close()
                print(f"16. Browser closed")

if __name__ == "__main__":
    high_low_price()