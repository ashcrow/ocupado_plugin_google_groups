# ocupado_plugin_google_groups
Google Groups plugin for the [ocupado tool](https://github.com/ashcrow/ocupado).

**Note**: This plugin only works for the paid version of Google Apps.

[![Build Status](https://api.travis-ci.org/ashcrow/ocupado_plugin_google_groups.png)](https://travis-ci.org/ashcrow/ocupado_plugin_google_groups/)

## Prerequisites
* [Set up authorization](https://developers.google.com/admin-sdk/directory/v1/guides/authorizing)
* Gain a json authorization service account file

## Usage
Add the plugin to your configuration backend.

### ini
```ini
[plugin]
# ...
ocupado_plugin_google_groups = GoogleGroups

[ocupado_plugin_google_groups]
ouath2_file_location=/full/path/to/config.json
group=mygroup
```
