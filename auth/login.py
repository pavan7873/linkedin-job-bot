from playwright.sync_api import sync_playwright


def login():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./auth/browser_data",
            headless=False,
        )

        page = browser.new_page()

        page.goto("https://www.linkedin.com/login")

        print("=" * 60)
        print("Login to LinkedIn manually.")
        print("After LinkedIn home page loads, press ENTER here.")
        print("=" * 60)

        input()

        browser.storage_state(path="./auth/state.json")

        print("Login state saved successfully.")

        browser.close()


if __name__ == "__main__":
    login()