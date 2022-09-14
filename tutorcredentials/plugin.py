from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair, (setting_name, default_value).
        # Prefix your setting names with 'CREDENTIALS_'.
        ("CREDENTIALS_VERSION", __version__),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL", "http://lms:8000/oauth2"),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_KEY", "{{ CREDENTIALS_OAUTH2_KEY }}"),
        ("CREDENTIALS_CATALOG_API_URL", "{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_DOCKER_IMAGE", "{{ DOCKER_REGISTRY }}lpm0073/openedx-credentials:{{ CREDENTIALS_VERSION }}"),
        ("CREDENTIALS_EXTRA_PIP_REQUIREMENTS", []),
        ("CREDENTIALS_FAVICON_URL", "https://edx-cdn.org/v3/default/favicon.ico"),
        ("CREDENTIALS_HOST", "credentials.{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_LMS_HOST", "myopenedxsite.com"),
        ("CREDENTIALS_LMS_URL", "http://{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_LMS_URL_ROOT", "http://{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL", "https://edx-cdn.org/v3/default/logo-trademark.svg"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL_PNG", "https://edx-cdn.org/v3/default/logo-trademark.png"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL_SVG", "https://edx-cdn.org/v3/default/logo-trademark.svg"),
        ("CREDENTIALS_LOGO_URL", "https://edx-cdn.org/v3/default/logo.svg"),
        ("CREDENTIALS_LOGO_URL_PNG", "https://edx-cdn.org/v3/default/logo.png"),
        ("CREDENTIALS_LOGO_URL_SVG", "https://edx-cdn.org/v3/default/logo.svg"),
        ("CREDENTIALS_LOGO_WHITE_URL", "https://edx-cdn.org/v3/default/logo-white.svg"),
        ("CREDENTIALS_LOGO_WHITE_URL_PNG", "https://edx-cdn.org/v3/default/logo-white.png"),
        ("CREDENTIALS_LOGO_WHITE_URL_SVG", "https://edx-cdn.org/v3/default/logo-white.svg"),
        ("CREDENTIALS_MYSQL_DATABASE", "credentials"),
        ("CREDENTIALS_MYSQL_USERNAME", "credentials"),
        ("CREDENTIALS_OAUTH2_KEY", "credentials-backend-service-key"),
        ("CREDENTIALS_PLATFORM_NAME", "{{ OPENEDX_PLATFORM_NAME }}"),
        ("CREDENTIALS_PRIVACY_POLICY_URL", "{{ CREDENTIALS_LMS_HOST }}/privacy-policy"),
        ("CREDENTIALS_SITE_NAME", "{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_SOCIAL_AUTH_REDIRECT_IS_HTTPS", False),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_ISSUER", "https://{{ CREDENTIALS_LMS_HOST }}"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT", "http://lms:8000"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_KEY", "credentials-sso-key"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL", "{{ CREDENTIALS_LMS_HOST }}/logout"),
        ("CREDENTIALS_THEME_NAME", "edx-theme"),
        ("CREDENTIALS_TOS_URL", "{{ CREDENTIALS_LMS_HOST }}/tos"),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance, passwords, secret keys, etc.
        # Each new setting is a pair, (setting_name, unique_generated_value).
        # Prefix your setting names with 'CREDENTIALS_'.
        # For example:
        ("CREDENTIALS_MYSQL_PASSWORD", "{{ 8|random_string }}"),
        ("CREDENTIALS_OAUTH2_SECRET", "{{ 16|random_string }}"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_SECRET", "{{ 16|random_string }}"),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_SECRET", "{{ 16|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair, (setting_name, new_value). For example:
        # ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To run the script from templates/credentials/tasks/myservice/init, add:
hooks.Filters.COMMANDS_INIT.add_item((
        "mysql",
        ("credentials", "tasks", "mysql", "init"),
))
hooks.Filters.COMMANDS_INIT.add_item((
        "lms",
        ("credentials", "tasks", "lms", "init"),
))
hooks.Filters.COMMANDS_INIT.add_item((
        "credentials",
        ("credentials", "tasks", "credentials", "init"),
))
hooks.Filters.IMAGES_BUILD.add_item((
        "credentials",
        ("plugins", "credentials", "build", "credentials"),
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
        (),
))
hooks.Filters.COMMANDS_INIT.add_item((
        "mysql",
        ("credentials", "tasks", "mysql", "sync_users"),
))

########################################
# DOCKER IMAGE MANAGEMENT
########################################

# To build an image with `tutor images build myimage`, add a Dockerfile to templates/credentials/build/myimage and write:
hooks.Filters.IMAGES_BUILD.add_item((
    "credentials",
    ("plugins", "credentials", "build", "credentials"),
    "{{ LICENSE_MANAGER_DOCKER_IMAGE }}",
    (),
))


# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CREDENTIALS_VERSION }}",
# )
# hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CREDENTIALS_VERSION }}",
# )


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorcredentials", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("credentials/build", "plugins"),
        ("credentials/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorcredentials/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorcredentials", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
