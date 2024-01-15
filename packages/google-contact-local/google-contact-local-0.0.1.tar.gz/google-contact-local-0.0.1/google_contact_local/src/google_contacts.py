# Standard libraries
import os
import json

# Libraries for Google API and authentication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account  # noqa: F401
import google.auth  # noqa: F401

# Local imports
from dotenv import load_dotenv
from user_external_local.external_user import ExternalUser
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from user_context_remote.user_context import UserContext
from contact_local.src.contact_local import ContactsLocal
from database_mysql_local.generic_crud import GenericCRUD
# from contact_group_local.contact_group import ContactGroup
load_dotenv()

# Static token details
SCOPES = ["https://www.googleapis.com/auth/userinfo.email",
          "https://www.googleapis.com/auth/contacts.readonly",
          "openid"]  # both scopes must be allowed within the project!
# What other scopes can we use?

# Logger setup
GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 188
GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'google-contact-local-python-package/google-contacts.py'
DEVELOPER_EMAIL = 'valeria.e@circ.zone'
obj = {
  'component_id': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
  'component_name': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
  'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
  'developer_email': 'valeria.e@circ.zone'
}
logger = Logger.create_logger(object=obj)

PORT = 54219  # TODO: Change to env variable


class GoogleContacts(GenericCRUD):
    # Specific id for people api with google contacts
    GOOGLE_CONTACT_SYSTEM_ID = 6

    def __init__(self, is_test_data: bool):
        user_context = UserContext.login_using_user_identification_and_password()
        self.contacts_local = ContactsLocal(is_test_data=is_test_data)
        self.profile_id = user_context.get_real_profile_id()
        self.creds = None
        self.email = None
        self.is_test_data = is_test_data
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        self.port = int(os.getenv("PORT"))
        # Change those to consts
        self.redirect_uris = os.getenv("GOOGLE_REDIRECT_URIS")
        self.auth_uri = os.getenv("GOOGLE_AUTH_URI")
        self.token_uri = os.getenv("GOOGLE_TOKEN_URI")

    def authenticate(self):  # note, missing check for token/email if user already authenticated.
        # usure how to check at the moment.

        logger.start("Getting user authentication")

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                client_config = {
                    "installed": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uris": self.redirect_uris,
                        "auth_uri": self.auth_uri,
                        "token_uri": self.token_uri,
                    }
                }
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                # old: self.creds = flow.run_local_server(port=0)
                # if GOOGLE_REDIRECT_URIS is localhost it must be
                # GOOGLE_REDIRECT_URIS=http://localhost:54415/
                # if the port number is 54415 and we must also pass that port
                # to the run_local_server function
                # and also add EXACTLY http://localhost:54415/
                # to Authorised redirect URIs in the 
                # OAuth 2.0 Client IDs in Google Cloud Platform
                self.creds = flow.run_local_server(port=self.port)

            # Fetch the user's email for profile_id in our DB
            service = build('oauth2', 'v2', credentials=self.creds)
            user_info = service.userinfo().get().execute()
            self.email = user_info.get("email")
            # TODO: What else can we get from user_info?

            # Deserialize the token_data into a Python dictionary
            token_data_dict = json.loads(self.creds.to_json())
            # TODO: What other data we can get from token_data_dict?

            # Extract the access_token, expires_in, and refresh_token to insert into our DB
            access_token = token_data_dict.get("token", None)
            expires_in = token_data_dict.get("expiry", None)
            refresh_token = token_data_dict.get("refresh_token", None)

            if access_token:
                ExternalUser.insert_or_update_user_external_access_token(
                    self.email,
                    self.profile_id,
                    self.GOOGLE_CONTACT_SYSTEM_ID,
                    access_token,
                    expires_in,
                    refresh_token
                )
            else:
                logger.error("Access token not found in token_data.")
                # TODO: Shall we raise exception?

        logger.end("Authentication request finished")

    @staticmethod
    # TODO: def create_contact_object( google_contact_connection : ...) -> int
    def create_str_representation(contact):

        # TODO: our_contact Contact;
        # Extracting relevant details from contact
        # TODO: Extract ALL data from contact, if needed we'll add more columns in our database
        first_names = [name.get('givenName', None) for name in contact.get('names', [])]
        family_names = [name.get('familyName', None) for name in contact.get('names', [])]
        phones = [phone.get('value', None) for phone in contact.get('phoneNumbers', [])]
        emails = [email.get('value', None) for email in contact.get('emailAddresses', [])]
        birthdays = [bday.get('text', None) for bday in contact.get('birthdays', [])]
        addresses = [addr.get('formattedValue', None) for addr in contact.get('addresses', [])]
        job_titles = [job.get('title', None) for job in contact.get('organizations', [])]
        organizations = [org.get('name', None) for org in contact.get('organizations', [])]

        # Create a string representation
        str_representation = []
        max_len = max(len(first_names), len(family_names), len(phones), len(emails), len(birthdays), len(addresses),
                      len(job_titles), len(organizations))

        for i in range(max_len):  # This part creates extra lines for multiple phone/email/etc for the same contact.
            # Will be removed once I manage to place these values in phone1/phone2/etc rather than create an extra line.
            first_name = first_names[i] if i < len(first_names) else first_names[-1] if first_names else None
            family_name = family_names[i] if i < len(family_names) else family_names[-1] if family_names else None
            phone = phones[i] if i < len(phones) else None
            email = emails[i] if i < len(emails) else None
            birthday = birthdays[i] if i < len(birthdays) else birthdays[-1] if birthdays else None
            address = addresses[i] if i < len(addresses) else addresses[-1] if addresses else None
            job_title = job_titles[i] if i < len(job_titles) else job_titles[-1] if job_titles else None
            organization = organizations[i] if i < len(organizations) else organizations[-1] if organizations else None

            # I don't think this is the right approach, we should create Contact object
            str_representation.append(
                f"{first_name}, {family_name}, {phone}, {birthday}, {email}, {address}, {job_title}, {organization}"
            )

        return str_representation

    def pull_people_api(self):
        logger.start("Pulling Details")
        try:
            service = build('people', 'v1', credentials=self.creds)
            # TODO: Shall we use v2? https://gist.github.com/avaidyam/acd66c26bc68bf6b89e70374bdc5a5d4
            logger.info('Listing all connection names along with their emails and phone numbers')

            # Start with an empty token
            page_token = None
            while True:
                results = service.people().connections().list(
                    resourceName='people/me',
                    pageSize=2000,  # Scrolls further in the GoogleContacts sheet, otherwise stops at around 10 contacts.
                    pageToken=page_token,
                    personFields='names,emailAddresses,phoneNumbers,birthdays,addresses,organizations,occupations').execute()

                # TODO: google_connections
                connections = results.get('connections', [])

                # TODO: for google_contact_connection in google_connetions
                for contact in connections:
                    print(f"Type of contact: {type(contact)}")
                    print(f"Contents of contact: {contact}")
                    # self._display_contact_details(contact)

                    # Create string representation for the contact
                    str_representation = GoogleContacts.create_str_representation(contact)
                    # TODO: The number of contacts in the database should be identical to the number of
                    # contacts in the Phone/Google Contacts
                    contact_dict = {}
                    for index, str_repr in enumerate(str_representation):
                        # Split the string by commas and strip each piece to remove leading/trailing white spaces
                        fields = [field.strip() for field in str_repr.split(",")]

                        # Replace the string 'None' with actual None objects
                        fields = [None if field == 'None' else field for field in fields]
                        if index == 0:
                            # Map the fields to named arguments for the insert method
                            contact_dict = {
                                "first_name": fields[0],
                                "last_name": fields[1],
                                "phone1": fields[2],
                                "birthday": fields[3],
                                "email1": fields[4],
                                "location": fields[5],
                                "job_title": fields[6],
                                "organization": fields[7]
                            }
                        else:
                            email_key = f"email{index + 1}"
                            phone_key = f"phone{index + 1}"
                            contact_dict[email_key] = fields[4]
                            contact_dict[phone_key] = fields[2]
                    contact_id = self.contacts_local.insert_update_contact(contact_dict)

                    # Add and link group
                    # contact_group = ContactGroup()
                    mapping_info = {
                        'default_entity_name1': 'contact_table',
                        'default_entity_name2': 'group_table',
                        'default_schema_name': 'contact_group',
                        'default_id_column_name': 'contact_group_id',
                        'default_table_name': 'contact_group_table',
                        'default_view_table_name': 'contact_group_table'
                    }

                    # TODO: Shall we also add the arguments is_interest, parent_group_id and title_lang_code?
                    '''
                    contact_group.add_update_group_and_link_to_contact(entity_name=contact_dict["organization"],
                                                                        contact_id=contact_id,
                                                                        mapping_info=mapping_info,
                                                                        title=contact_dict["job_title"],
                                                                        is_test_data=self.is_test_data)
                    '''

                # TODO: Add contact_person directly or using ContactPersonsLocal.insert() from GenericCRUD

                # Break after processing one contact - for debugging without running over all contacts heh
                # break

                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            logger.end("Finished Pulling Details")

        except HttpError as err:
            logger.exception("Error while retrieving contacts from Google using People API and inserting the contact", err)
            logger.end()

    # def _display_contact_details(self, contact):  # for debugging, can delete later
    #     def display_with_names(header, values):
    #         if not values:
    #             print(f"{header}: None")
    #             return
    #         for value in values:
    #             first_name = contact['names'][0].get('givenName', None) if 'names' in contact else None
    #             last_name = contact['names'][0].get('familyName', None) if 'names' in contact else None
    #             print(f"{header} for {first_name} {last_name}: {value}")

    #     # Display names
    #     if 'names' in contact:
    #         names = contact['names']
    #         if names:
    #             first_name = names[0].get('givenName', None)
    #             last_name = names[0].get('familyName', None)
    #             print(f"Name: {first_name} {last_name}")
    #         else:
    #             print("Name: None")
    #     else:
    #         print("Name: None")

    #     # Display emails
    #     emails = [email.get('value', None) for email in contact.get('emailAddresses', [])]
    #     display_with_names("Email", emails)

    #     # Display phone numbers
    #     phone_numbers = [phone.get('value', None) for phone in contact.get('phoneNumbers', [])]
    #     display_with_names("Phone Number", phone_numbers)

    #     # Display birthdays
    #     birthdays = [birthday.get('text', None) for birthday in contact.get('birthdays', [])]
    #     display_with_names("Birthday", birthdays)

    #     # Display addresses
    #     addresses = [address.get('formattedValue', None) for address in contact.get('addresses', [])]
    #     display_with_names("Address", addresses)

    #     # Display organizations
    #     organizations = [org.get('name', None) for org in contact.get('organizations', [])]
    #     display_with_names("Organization", organizations)

    #     # Display occupations
    #     occupations = [occ.get('value', None) for occ in contact.get('occupations', [])]
    #     display_with_names("Occupation", occupations)

    def pull_contacts_with_stored_token(self, email):
        logger.start("Pulling Details From Existing User")
        if not email:
            logger.error("Email cannot be null.")
            return

        token_data = ExternalUser.get_auth_details(email, self.GOOGLE_CONTACT_SYSTEM_ID, self.profile_id)

        # Unpack the token_data tuple into its constituent parts
        access_token, refresh_token, expiry = token_data

        # Update the token_info dictionary with the unpacked values
        token_info = {
            'token': access_token,
            'refresh_token': refresh_token,
            'token_uri': self.token_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scopes': SCOPES,
            'expiry': expiry  # Already in string format, no need to convert
        }

        # Create a Credentials object from the stored token
        try:
            self.creds = Credentials.from_authorized_user_info(token_info)

            # Print all attributes of self.creds for debugging
            for attr in dir(self.creds):
                if not attr.startswith("__"):
                    print(f"{attr}: {getattr(self.creds, attr)}")

            if not self.creds.valid:
                logger.error("Stored credentials are not valid.")
                logger.error(f"Token info: {token_info}")
                return
        except Exception as e:
            logger.error(f"Exception while creating credentials: {e}")
            logger.end()
            return

        # Now, pull the contacts using the People API
        self.pull_people_api()
        logger.end("Finished Pulling From Existing User")

    # TODO: move this to ContactPersonsLocal
    # TODO: Shall we add a new person if it doesn't exist?
    '''
    def _insert_to_contact_person(self, contact_id: int, person_id: int):
        logger.start(object={"contact_id": contact_id, "person_id": person_id})
        groups_remote = GroupsRemote()
        # TODO: Shall we create constants for "contact_table" and "person_table"?
        is_mapping_exist = groups_remote.is_mapping_exist("contact_table", "person_table", contact_id, person_id)
        if is_mapping_exist:
            data_json = {
                "contact_id": contact_id,
                "person_id": person_id
            }
            self.insert("contact_person_table", data_json=data_json)
        logger.end()
    '''

    # TODO: move this to ContactNotesLocal
    def _insert_to_contact_note(self, contact_id: int, note: str):
        logger.start(object={"contact_id": contact_id, "note": note})
        data_json = {
            "contact_id": contact_id,
            "note": note
        }
        self.insert("contact_note_table", data_json=data_json)
        logger.end()

    # TODO: move this to ContactImporterLocal
    # TODO: Shall we add a new importer if it doesn't exist?
    '''
    def _insert_to_contact_importer(self, contact_id: int, importer_id: int):
        logger.start(object={"contact_id": contact_id, "importer_id": importer_id})
        groups_remote = GroupsRemote()
        is_mapping_exist = groups_remote.is_mapping_exist("contact_table", "importer_table", contact_id, importer_id)
        if is_mapping_exist:
            data_json = {
                "contact_id": contact_id,
                "importer_id": importer_id
            }
            self.insert("contact_importer_table", data_json=data_json)
        logger.end()
    '''

    # TODO: move this to ContactGroupsLocal
    # TODO: Shall we add a new group if it doesn't exist?
    # TODO: The group is the contact's organization?
    '''
    def _insert_to_contact_group(self, contact_id: int, group_id: int):
        logger.start(object={"contact_id": contact_id, "group_id": group_id})
        groups_remote = GroupsRemote()
        is_mapping_exist = groups_remote.is_mapping_exist("contact_table", "group_table", contact_id, group_id)
        if is_mapping_exist:
            data_json = {
                "contact_id": contact_id,
                "group_id": group_id
            }
            self.insert("contact_group_table", data_json=data_json)
        logger.end()

    def _insert_group(self, group_name: str):
        logger.start(object={"group_name": group_name})
        groups_remote = GroupsRemote()
        group_id = groups_remote.get_group_id(group_name)
        if group_id is None:
            group_id = groups_remote.insert_group(group_name)
        logger.end()
        return group_id
    '''


if __name__ == '__main__':
    fetcher = GoogleContacts()
    fetcher.authenticate()
    fetcher.pull_people_api()
    fetcher.pull_contacts_with_stored_token("valerka.prov@gmail.com")  # "example@example.com"
