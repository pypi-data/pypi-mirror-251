from email.utils import parseaddr
import re

from ckan.common import asbool, config
from ckan import logic
import ckan.plugins.toolkit as toolkit

from . import helpers as dcor_helpers
from . import resource_schema_supplements as rss


def dataset_purge(context, data_dict):
    """Only allow deletion of deleted datasets"""
    # original auth function
    # (usually, only sysadmins are allowed to purge, so we test against
    # package_update)
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    pkg_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})
    state = pkg_dict.get('state')
    if state != "deleted":
        return {"success": False,
                "msg": "Only deleted datasets can be purged!"}
    return {"success": True}


def deny(context, data_dict):
    return {'success': False,
            'msg': "Only admins may do so."}


def get_package_id(context, data_dict):
    """Convenience function that extracts the package_id"""
    package = context.get('package')
    if package:
        # web
        package_id = package.id
    else:
        package_id = logic.get_or_bust(data_dict, 'id')
    convert_package_name_or_id_to_id = toolkit.get_converter(
        'convert_package_name_or_id_to_id')
    return convert_package_name_or_id_to_id(package_id, context)


def package_create(context, data_dict):
    # Note that we did not decorate this function with
    # @logic.auth_allow_anonymous_access. This effectively
    # disables dataset creation via the web interface.
    # However, we make sure that the API is used with the following:
    using_api = 'api_version' in context
    if not using_api:
        return {"success": False,
                "msg": "Creating datasets is only possible via the API. "
                       "Please use DCOR-Aid for uploading data!"}

    # original auth function
    ao = logic.auth.create.package_create(context, data_dict)
    if not ao["success"]:
        return ao

    if data_dict:
        # Use our own configuration option to determine whether the
        # admin has disabled public datasets (e.g. for DCOR-med).
        must_be_private = not asbool(config.get(
            "ckanext.dcor_schemas.allow_public_datasets", "true"))
        private_default = must_be_private  # public if not has to be private
        is_private = asbool(data_dict.get('private', private_default))
        if must_be_private and not is_private:
            return {"success": False,
                    "msg": "Creating public datasets has been disabled via "
                           "the configuration option 'ckanext.dcor_schemas."
                           "allow_public_datasets = false'!"}

    return {"success": True}


def package_delete(context, data_dict):
    """Only allow deletion of draft datasets"""
    # original auth function
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    pkg_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})
    state = pkg_dict.get('state')
    if state != "draft":
        return {"success": False,
                "msg": "Only draft datasets can be deleted!"}
    return {"success": True}


def package_update(context, data_dict=None):
    # original auth function
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    if data_dict is None:
        data_dict = {}

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    pkg_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})

    resource_ids = [r["id"] for r in pkg_dict.get("resources", [])]

    # run resource check functions
    for res_dict in data_dict.get("resources", []):
        # Note that on DCOR, you are not allowed to specify the ID
        # during upload.
        curid = res_dict.get("id")
        res_dict["package_id"] = pkg_dict["id"]
        if curid in resource_ids:
            # we are updating a resource
            aorc = resource_update_check(context, res_dict)
            if not aorc["success"]:
                return aorc
        elif curid is None:
            # we are creating a resource
            aorc = resource_create_check(context, res_dict)
            if not aorc["success"]:
                return aorc
        else:
            # Somebody is trying something nasty
            return {'success': False,
                    'msg': f"Invalid resource ID {curid} for dataset "
                           + f"{pkg_dict['id']}!"}

    # do not allow changing things and uploading resources to non-drafts
    if pkg_dict.get('state') != "draft":
        # these things are allowed to be in the data dictionary (see below)
        allowed_keys = [
            "license_id",  # see below, setting less restrictive license
            "private",  # see below, making dataset public
            "state",  # see below, not really important
            ]
        ignored_keys = [
            "pkg_name",  # this is sometimes present in the web interface
        ]
        ignored_empty_keys = [
            # keys that may be present if they are empty
            "tag_string",  # redundant with "tags"
        ]
        for key in data_dict:
            if key in ignored_keys:
                continue
            elif key in ignored_empty_keys and not data_dict[key]:
                # ignore some of the keys
                continue
            elif not data_dict[key] and not pkg_dict.get(key):
                # ignore empty keys that are not in the original dict
                continue
            if data_dict[key] != pkg_dict.get(key) and key not in allowed_keys:
                return {'success': False,
                        'msg': f"Changing '{key}' not allowed for non-draft "
                               + "datasets!"}

    # do not allow switching to a more restrictive license
    if "license_id" in data_dict:
        allowed = dcor_helpers.get_valid_licenses(pkg_dict["license_id"])
        if data_dict["license_id"] not in allowed:
            return {'success': False,
                    'msg': 'Cannot switch to more-restrictive license'}

    # do not allow setting state from "active" to "draft"
    if pkg_dict["state"] != "draft" and data_dict.get("state") == "draft":
        return {'success': False,
                'msg': 'Changing dataset state to draft not allowed'}

    # private dataset?
    must_be_private = not asbool(config.get(
        "ckanext.dcor_schemas.allow_public_datasets", "true"))
    private_default = must_be_private  # public if not has to be private
    is_private = asbool(data_dict.get('private', private_default))
    was_private = pkg_dict["private"]
    assert isinstance(was_private, bool)
    if must_be_private:
        # has to be private
        if not is_private:
            # do not allow setting visibility from private to public if public
            # datasets are not allowed
            return {"success": False,
                    "msg": "Public datasets have been disabled via "
                           "the configuration option 'ckanext."
                           "dcor_schemas.allow_public_datasets = false'!"}
    else:
        # does not have to be private
        if not was_private and is_private:
            # do not allow setting the visibility from public to private
            return {'success': False,
                    'msg': 'Changing visibility to private not allowed'}

    # do not allow changing some of the keys (also for drafts)
    prohibited_keys = ["name"]
    invalid = {}
    for key in data_dict:
        if (key in pkg_dict
            and key in prohibited_keys
                and data_dict[key] != pkg_dict[key]):
            invalid[key] = data_dict[key]
    if invalid:
        return {'success': False,
                'msg': 'Editing not allowed: {}'.format(invalid)}

    return {'success': True}


def resource_create(context, data_dict=None):
    # original auth function
    ao = logic.auth.create.resource_create(context, data_dict)
    if not ao["success"]:
        return ao

    return resource_create_check(context, data_dict)


def resource_create_check(context, new_dict):
    if "package_id" in new_dict:
        pkg_dict = logic.get_action('package_show')(
            dict(context, return_type='dict'),
            {'id': new_dict["package_id"]})

        # do not allow adding resources to non-draft datasets
        if pkg_dict["state"] != "draft":
            return {'success': False,
                    'msg': 'Adding resources to non-draft datasets not '
                           'allowed!'}
        # id must not be set
        if new_dict.get("id", ""):
            return {'success': False,
                    'msg': 'You are not allowed to set the resource ID!'}

        return {'success': True}
    else:
        return {'success': False,
                'msg': 'No package_id specified!'}


def resource_update(context, data_dict=None):
    # original auth function
    # (this also checks against package_update auth)
    ao = logic.auth.update.resource_update(context, data_dict)
    if not ao["success"]:
        return ao

    data_dict["package_id"] = get_package_id(context, data_dict)

    return resource_update_check(context, data_dict)


def resource_update_check(context, new_dict):
    # get the current resource dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    old_dict = logic.get_action('resource_show')(
        show_context,
        {'id': logic.get_or_bust(new_dict, 'id')})

    # only allow updating the description...
    allowed_keys = ["description"]
    # ...and "sp:*" keys
    allowed_keys += rss.get_composite_item_list()

    invalid = []
    for key in new_dict:
        if key in allowed_keys:
            continue
        elif key in old_dict and new_dict[key] == old_dict[key]:
            continue
        else:
            invalid.append(f"{key}={new_dict[key]}")
    if invalid:
        return {'success': False,
                'msg': f'Editing not allowed: {", ".join(invalid)}'}

    return {'success': True}


@logic.auth_allow_anonymous_access
def user_create(context, data_dict=None):
    """Measure against automated registration from gmail addresses

    This function is the first escalation of many more possible
    ways to restrict user registration via bots, e.g.

    - https://github.com/DCOR-dev/ckanext-dcor_schemas/issues/1
    - https://github.com/DCOR-dev/ckanext-dcor_schemas/issues/4
    - https://github.com/DCOR-dev/ckanext-dcor_schemas/issues/14

    Part of this (implementing as auth function) is actually
    security by obscurity. Anyone trying to register with a
    gmail address will just get a "403 Forbidden".

    Implementing this with IUserForm would be much better:
    https://github.com/ckan/ckan/issues/6070
    """
    # original auth function
    ao = logic.auth.create.user_create(context, data_dict)
    if not ao["success"]:
        return ao

    collected_data = {}
    spam_score = 0

    if data_dict is None:
        data_dict = {}

    for name_key in ["fullname", "name", "display_name", "email"]:
        name_val = data_dict.get(name_key, "").lower()
        collected_data[name_key] = name_val
        if name_val.count("xx"):
            # script kiddies
            spam_score += 1

    if "image_url" in data_dict:
        imgu = data_dict.get("image_url", "").lower()
        collected_data["image_url"] = imgu
        if imgu:
            if not re.search(r"\.(png|jpe?g)$", imgu):  # clearly abuse
                spam_score += 1

    if "email" in data_dict:
        # somebody is attempting to create a user
        email = data_dict.get("email", "").strip()
        collected_data["email"] = email
        if not email:
            return {'success': False,
                    'msg': 'No email address provided!'}
        else:
            email = parseaddr(email)[1]
            if (not email
                or "@" not in email
                    or "." not in email.split("@")[1]):
                # not a valid email address
                return {'success': False,
                        'msg': 'Invalid email address provided!'}
            domain = email.split("@")[1]
            # this might be a little harsh
            if domain in ["gmail.com", "mailto.plus"]:
                spam_score += 1

    if spam_score:
        return {'success': False,
                'msg': f'Spam bot{spam_score * "*"} {collected_data}'}

    return {'success': True}
