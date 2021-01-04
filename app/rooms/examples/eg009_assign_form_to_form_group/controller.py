from docusign_rooms import (
    FormGroupsApi,
    FormGroupSummaryList,
    FormLibrariesApi,
    FormGroupFormToAssign,
)
from docusign_rooms import FormSummaryList
from flask import session, request

from app.rooms import create_rooms_api_client


class Eg009Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "form_group_id": request.form.get("form_group_id"),
            "form_id": request.form.get("form_id")
        }

    @staticmethod
    def get_form_groups(args):
        """
        1. Create an API Client with headers
        2. GET Form Groups via FormGroupsAPI
        """

        # Step 1. Create an API with headers with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. GET Form Groups via FormGroupsAPI
        form_groups_api = FormGroupsApi(api_client)
        response = form_groups_api.get_form_groups(
            account_id=args["account_id"])  # type: FormGroupSummaryList

        return response.form_groups

    @staticmethod
    def get_forms(args):
        """
        1. Create an API client with headers
        2. Get first form library id
        3. Get forms
        """

        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get first form library id
        form_libraries_api = FormLibrariesApi(api_client)
        form_libraries = form_libraries_api.get_form_libraries(
            account_id=args["account_id"])

        first_form_library_id = form_libraries.forms_library_summaries[0].forms_library_id

        # Step 3. Get forms
        form_library_forms = form_libraries_api.get_form_library_forms(
            form_library_id=first_form_library_id,
            account_id=args["account_id"]
        )   # type: FormSummaryList

        return form_library_forms.forms

    @staticmethod
    def worker(args):
        """
        1. Create an API Client with headers
        2. Create FormGroupFormToAssign Object
        3. Assign form to a form group via FormGroups API
        """

        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])
        form_groups_api = FormGroupsApi(api_client)

        # Step 2. Create FormGroupFormToAssign Object
        form_group_to_assign = FormGroupFormToAssign(form_id=args["form_id"],
                                                     is_required=True)

        # Step 3. Assign form to a form group via FormGroups API
        response = form_groups_api.assign_form_group_form(
            form_group_id=args["form_group_id"], account_id=args["account_id"],
            body=form_group_to_assign
        )   # type: FormGroupFormToAssign

        return response
