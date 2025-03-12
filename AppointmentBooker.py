from imports import *


class AppointmentBooker:
    def __init__(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
    def navigate_to_booking_page(self):
        """Navigate through the initial booking steps"""
        self.page.goto(BOOKER_URL)
        
        # Initial page interactions
        self.page.locator(RESIDENT_PERMIT_FAMILY).click()
        sleep(2)
        
        # Select number of people
        self.page.locator(COUNTER_PLUS).nth(0).click()
        sleep(2)
        
        # Proceed through booking steps
        self.page.locator(CONTINUE_BUTTON).click()
        self.page.wait_for_selector(SLOT1)
        self.page.locator(SLOT1).click()
        sleep(2)

    def fill_personal_details(self, person):
        """Fill in personal information section"""
        self.page.locator("select#Salutation").select_option(person["title"])
        self._fill_field("input#FirstName", person["firstname"])
        self._fill_field("input#LastName", person["lastname"])
        self._fill_field("input#Birthday", person["birthdate"])
        self.page.locator("select#City").select_option(person["city"])

    def fill_contact_info(self, person):
        """Fill contact information including phone country code"""
        self._select_phone_country_code()
        self._fill_field("input#Phone", str(person["phone"]))
        self._fill_field("input#Email", person["email"])
        sleep(2)

    def _fill_field(self, selector, value):
        """Helper method to fill form fields"""
        self.page.locator(selector).fill(value)
        sleep(2)

    def _select_phone_country_code(self):
        """Handle phone country code selection"""
        self.page.locator("div.iti__selected-flag").click()
        self.page.locator("span.iti__country-name").nth(0).click() #Germany
        sleep(2)

    def close(self):
        """Clean up resources"""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    

    def run(self, person):
        """Execute the full booking flow"""
        try:
            self.navigate_to_booking_page()
            self.fill_personal_details(person)
            self.fill_contact_info(person)
        except Exception as e:
            print(f"Error during booking: {str(e)}")
        finally:
            self.close()
    
    @staticmethod
    def load_profile(rank):
        df = pd.read_csv(PROFILES)
        profile = df.iloc[rank].to_dict()
        return (profile)

# if __name__ == "__main__":
#     df = pd.read_csv("profiles.csv")
#     profile = df.iloc[0].to_dict()
#     print(profile)
#     booker = AppointmentBooker(headless=False)
#     booker.run(profile)