# The native types str and int are used too


class ImmediateValue:
    def __init__(self, value_deferred):
        self.value_deferred = value_deferred

    def __repr__(self):
        return f"#{self.value_deferred!r}"


class DeferredAddressing:
    def __init__(self, inner_deferred, operator_style: bool):
        self.inner_deferred = inner_deferred
        self.operator_style: bool = operator_style

    def __repr__(self):
        if self.operator_style:
            return f"@{self.inner_deferred!r}"
        else:
            return f"({self.inner_deferred!r})"


class Register:
    def __init__(self, index_deferred, operator_style: bool):
        self.index_deferred = index_deferred
        self.operator_style: bool = operator_style

    def __repr__(self):
        if self.operator_style:
            return f"%{self.index_deferred!r}"
        else:
            return f"r{self.index_deferred!r}"


class AutoIncrementAddressing:
    def __init__(self, register: Register):
        self.register: Register = register

    def __repr__(self):
        return f"({self.register!r})+"


class AutoDecrementAddressing:
    def __init__(self, register: Register):
        self.register: Register = register

    def __repr__(self):
        return f"-({self.register!r})"


class IndexAddressing:
    def __init__(self, index_deferred, register: Register):
        self.index_deferred = index_deferred
        self.register: Register = register

    def __repr__(self):
        return f"{self.index_deferred or ''}({self.register!r})"
