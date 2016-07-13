from flask import Blueprint, g


class NestableBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        self.parent_entity_key = kwargs.pop('parent_entity_key', None)
        super(NestableBlueprint, self).__init__(*args, **kwargs)

        if self.parent_entity_key:
            def set_entity_id_in_state(_, values):
                v = values.get(self.parent_entity_key, None)
                setattr(g, self.parent_entity_key, v)
                if v:
                    values.pop(self.parent_entity_key)
            self.url_value_preprocessor(set_entity_id_in_state)

    def context_id(self):
        if self.parent_entity_key:
            return getattr(g, self.parent_entity_key, None)
