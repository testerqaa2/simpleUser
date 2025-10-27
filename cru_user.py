from playwright.sync_api import sync_playwright
import time

def create_user():
    print("1. Create User")

    BASE_URL = "https://gorest.co.in"
    TOKEN = "5211b2442902e3088bf857d89f9575b3c7b28c2c81896d29ecd13d3e342ff534"
    
    with sync_playwright() as p:
        request_create = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
        )

        timestamp = int(time.time())
        user_data = {
            "name": f"Test User {timestamp}",
            "email": f"testuser{timestamp}@example.com", 
            "gender": "female",
            "status": "active"
        }
        
        print(f"Creating user with data: {user_data}")
        
        try:
            create_response = request_create.post("/public/v2/users", data=user_data)
            
            if create_response.status == 201:
                user_info = create_response.json()
                print(f"✅ SUCCESS - User created")
                print(f"   ID    : {user_info['id']}")
                print(f"   Name  : {user_info['name']}")
                print(f"   Email : {user_info['email']}")
                print(f"   Gender: {user_info['gender']}")
                print(f"   Status: {user_info['status']}")
                return user_info['id']
            else:
                print(f"❌ FAILED! Status code: {create_response.status}")
                print(f"   Response: {create_response.text()}")
                return None
                
        except Exception as e:
            print(f"ERROR: {e}")
            return None
        
        finally:
            request_create.dispose()

def get_user_details(user_id):
    print("\nGet User Details")
    
    BASE_URL = "https://gorest.co.in"
    TOKEN = "5211b2442902e3088bf857d89f9575b3c7b28c2c81896d29ecd13d3e342ff534"
    
    with sync_playwright() as p:
        request_detail = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"Getting user details from user ID: {user_id}")
        
        try:
            get_response = request_detail.get(f"/public/v2/users/{user_id}")

            if get_response.status == 200:
                user_info = get_response.json()
                print(f"✅ SUCCESS - User details")
                print(f"   ID    : {user_info['id']}")
                print(f"   Name  : {user_info['name']}")
                print(f"   Email : {user_info['email']}")
                print(f"   Gender: {user_info['gender']}")
                print(f"   Status: {user_info['status']}")
                return user_info
            else:
                print(f"❌ FAILED! Status code: {get_response.status}")
                print(f"   Response: {get_response.text()}")
                return None
                
        except Exception as e:
            print(f"ERROR: {e}")
            return None
        
        finally:
            request_detail.dispose()

def update_user(user_id):
    print("\n3. Update User Data")
    
    BASE_URL = "https://gorest.co.in"
    TOKEN = "5211b2442902e3088bf857d89f9575b3c7b28c2c81896d29ecd13d3e342ff534"
    
    with sync_playwright() as p:
        request_update = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
        )
        
        update_data = {
            "name": f"Updated User {int(time.time())}",
            "email": f"updateduser{int(time.time())}@example.com",
            "status": "inactive"
        }
        
        print(f"Updating user ID {user_id} with data: {update_data}")
        
        try:
            update_response = request_update.patch(f"/public/v2/users/{user_id}", data=update_data)
            
            if update_response.status == 200:
                updated_user = update_response.json()
                print(f"✅ SUCCESS - User updated")
                print(f"   ID    : {updated_user['id']}")
                print(f"   Name  : {updated_user['name']} (updated)")
                print(f"   Email : {updated_user['email']} (updated)")
                print(f"   Gender: {updated_user['gender']} (unchanged)")
                print(f"   Status: {updated_user['status']} (updated)")
                return updated_user
            else:
                print(f"❌ FAILED! Status code: {update_response.status}")
                print(f"   Response: {update_response.text()}")
                return None
                
        except Exception as e:
            print(f"ERROR: {e}")
            return None
        
        finally:
            request_update.dispose()

if __name__ == "__main__":

    user_id = create_user()
    if user_id:
        print(f"\nSuccessfully created a new user with User ID: {user_id}")
        
        print("\nUser information before update:")
        original_user = get_user_details(user_id)
        
        if original_user:
            updated_user = update_user(user_id)
            
            if updated_user:
                print("\nUser information after updated:")
                final_user = get_user_details(user_id)
                
                if final_user:
                    print("\nUser successfully created, updated, and verified")
                    
                    print("\nUser Information before and after:")
                    print(f"Name   : '{original_user['name']}'  → '{final_user['name']}'")
                    print(f"Email  : '{original_user['email']}' → '{final_user['email']}'")
                    print(f"Status : '{original_user['status']}'→ '{final_user['status']}'")
                else:
                    print(f"\nUser updated but failed to get final details")
            else:
                print(f"\nFailed to update user")
        else:
            print(f"\nUser created but failed to get initial details")
    else:
        print(f"\nFailed to create user")