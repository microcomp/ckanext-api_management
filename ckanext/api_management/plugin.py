import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class APIManagementPlugin(plugins.SingletonPlugin):
    ctr = 'ckanext.api_management.management:APIManagementController'
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    def before_map(self, map):
        map.connect('api_management_page', '/API_management', action='APIManagement', controller=self.ctr)
        map.connect('new_api_key', '/API_management/NewAPIKey', action='NewAPIKey', controller=self.ctr)
        return map
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')