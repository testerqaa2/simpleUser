from playwright.sync_api import sync_playwright, expect

def order():
    """Test Order on both Chrome and Firefox"""
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
                print(f"✅  User successfully logged into account")

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
            
                print("7. Add products to cart")
                button_text = "Add to cart"
                product_backpack = page.locator("#add-to-cart-sauce-labs-backpack")
                product_tshirt = page.locator("#add-to-cart-sauce-labs-bolt-t-shirt")
                expect(product_backpack).to_be_visible()
                expect(product_tshirt).to_be_visible()
                expect(product_backpack).to_have_text(button_text)
                expect(product_tshirt).to_have_text(button_text)
                product_backpack.click()
                product_tshirt.click()
                print("✅ Products are added to cart")

                cart_badge_value = page.locator(".shopping_cart_badge")
                expect(cart_badge_value).to_be_visible()
                expect(cart_badge_value).to_have_text("2")
                print("✅ Cart badge value = 2")
            
                print("8. Open cart page")
                cart_icon = page.locator("[data-test='shopping-cart-link']")
                cart_icon.click()
                title_cart = ("Your Cart")
                title_cart_page = page.locator("text=Your Cart")
                expect(title_cart_page).to_be_visible()
                expect(title_cart_page).to_have_text(title_cart)
                
                product_name_backpack = "Sauce Labs Backpack"
                expect(page.locator("#item_4_title_link")).to_have_text(product_name_backpack)

                product_name_tshirt = "Sauce Labs Bolt T-Shirt"
                expect(page.locator("#item_1_title_link")).to_have_text(product_name_tshirt)
                print("✅ Cart page loaded with correct products name")
            
                print("9. Click Checkout button")
                title_btn = ("Checkout")
                checkout_button = page.locator("#checkout")
                expect(checkout_button).to_be_visible()
                expect(checkout_button).to_have_text(title_btn)
                checkout_button.click()

                print("10. Input user information")
                first_name = ("Frisca")
                last_name = ("Arianja")
                postal_code = ("17133")
                page.fill("#first-name", first_name)
                page.fill("#last-name", last_name)
                page.fill("#postal-code", postal_code)
                print("✅ Checkout form filled")

                print("11. Click Checkout button")
                continue_btn = page.locator("#continue")
                continue_btn.click()

                title_Checkout_page = page.locator('.title[data-test="title"]').inner_text().strip()
                expected_title = ("Checkout: Overview")

                print(f"12. Verify title Checkout page")
                assert title_Checkout_page == expected_title, \
                    f"Title text isn't as expected. Current: '{title_Checkout_page}', Expected: '{expected_title}'"
                print(f"💡 Title Checkout page is : '{expected_title}'")

                print(f"13. Verify Product List")
                product_name_backpack = "Sauce Labs Backpack"
                expect(page.locator("#item_4_title_link")).to_have_text(product_name_backpack)
                product_name_tshirt = "Sauce Labs Bolt T-Shirt"
                expect(page.locator("#item_1_title_link")).to_have_text(product_name_tshirt)
                print("✅ Checkout page loaded with correct products name")

                print("14. Click Finish")
                finish_button = page.locator("#finish")
                finish_button.click()

                complete_title= page.locator("[data-test='complete-header']").inner_text().strip()
                complete_text = ("Thank you for your order!")
                assert complete_title == complete_text, \
                    f"Text isn't as expected. Current: '{complete_title}', Expected: '{complete_text}'"
                print(f"💡 Title order completed is : '{complete_text}'")

                complete_desc = page.locator("[data-test='complete-text']").inner_text().strip()
                complete_desc_text = ("Your order has been dispatched, and will arrive just as fast as the pony can get there!")
                assert complete_desc == complete_desc_text, \
                    f"Description text isn't as expected. Current: '{complete_desc}', Expected: '{complete_desc_text}'"
                print(f"💡 Order Description text is : '{complete_desc_text}'")
                print("✅ Order completed successfully")
            
                print("15. Back to main page")
                back_home = page.locator("#back-to-products")
                back_home.click()

            finally:
                browser.close()
                print(f"16. Browser closed")

if __name__ == "__main__":
    order()