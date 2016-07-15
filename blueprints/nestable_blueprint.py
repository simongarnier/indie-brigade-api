from flask import Blueprint


class NestableBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        self.parent_keys = kwargs.pop('parent_keys', None)
        self.parent_ids = {}
        super(NestableBlueprint, self).__init__(*args, **kwargs)

        if self.parent_keys:
            def set_context_id_in_state(_, values):
                for parent_entity_key in self.parent_keys:
                    v = values.get(parent_entity_key, None)
                    self.parent_ids[parent_entity_key] = v
                    if v:
                        values.pop(parent_entity_key)
            self.url_value_preprocessor(set_context_id_in_state)
