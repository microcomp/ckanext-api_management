import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import management


class APIManagementPlugin(plugins.SingletonPlugin):
    ctr = 'ckanext.api_management.management:APIManagementController'
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    def before_map(self, map):
        map.connect('new_api_key', '/API_management/NewAPIKey', action='NewAPIKey', controller=self.ctr)
        return map
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        return {'management_installed': management.is_installed}