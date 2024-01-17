class DataUtils(object):
    @staticmethod
    def convert_keys_to_lowercase(data):
        if isinstance(data, dict):
            converted_data = {}
            for key, value in data.items():
                converted_key = key.lower()
                converted_value = DataUtils.convert_keys_to_lowercase(value)
                converted_data[converted_key] = converted_value
            return converted_data
        elif isinstance(data, list):
            return [DataUtils.convert_keys_to_lowercase(item) for item in data]
        else:
            return data
