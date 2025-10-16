from Leafy.LeafySDK.api import App
def inject_params(init_variable_data):
    params = {}
    mapping = {
        "leaf.app": App.get_app()
    }
    for key, api in init_variable_data.items():
        for Mapping_key, Mapping_api in mapping.items():
            if str(api).lower() == Mapping_key:
                params[key] = Mapping_api
    return params

