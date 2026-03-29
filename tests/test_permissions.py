import pytest
from models.role import Role
from models.user import User
from services.user_service import UserService


class DummyRoleStore:
    def __init__(self, roles):
        self.roles = roles

    def get_role(self, role_id):
        return self.roles.get(role_id)


# Test 1
def test_deny_overrides_allow():
    viewer = Role(1, "Viewer")
    viewer.add_permission("read")

    editor = Role(2, "Editor")
    editor.add_permission("write")
    editor.add_parent_role(1)

    admin = Role(3, "Admin")
    admin.add_parent_role(2)
    admin.add_deny_permission("write")

    roles = {
        1: viewer,
        2: editor,
        3: admin
    }

    role_store = DummyRoleStore(roles)

    user = User(1, "test_user")
    user.role_ids = {3}

    user_service = UserService(role_store)

    assert user_service.user_has_permission(user, "read") is True
    assert user_service.user_has_permission(user, "write") is False


# Test 2
def test_multiple_roles_conflict():
    role_allow = Role(1, "AllowRole")
    role_allow.add_permission("write")

    role_deny = Role(2, "DenyRole")
    role_deny.add_deny_permission("write")

    roles = {
        1: role_allow,
        2: role_deny
    }

    role_store = DummyRoleStore(roles)

    user = User(1, "test_user")
    user.role_ids = {1, 2}

    user_service = UserService(role_store)

    assert user_service.user_has_permission(user, "write") is False


# Test 3
def test_inheritance_chain():
    base = Role(1, "Base")
    base.add_permission("read")

    mid = Role(2, "Mid")
    mid.add_parent_role(1)

    top = Role(3, "Top")
    top.add_parent_role(2)

    roles = {
        1: base,
        2: mid,
        3: top
    }

    role_store = DummyRoleStore(roles)

    user = User(1, "test_user")
    user.role_ids = {3}

    user_service = UserService(role_store)

    assert user_service.user_has_permission(user, "read") is True


# Test 4
def test_cache_usage():
    role = Role(1, "Viewer")
    role.add_permission("read")

    roles = {1: role}
    role_store = DummyRoleStore(roles)

    user = User(1, "test_user")
    user.role_ids = {1}

    user_service = UserService(role_store)

    result1 = user_service.user_has_permission(user, "read")

    assert result1 is True
    assert user.user_id in user_service.user_permission_cache

    result2 = user_service.user_has_permission(user, "read")

    assert result2 is True

# Test 5
def test_user_with_no_roles_has_no_permissions():
    role_store = DummyRoleStore({})

    user = User(1, "test_user")
    user.role_ids = set()

    user_service = UserService(role_store)

    assert user_service.user_has_permission(user, "read") is False
    assert user_service.user_has_permission(user, "write") is False

# Test 6
def test_remove_role_from_user_clears_cache():
    role = Role(1, "Viewer")
    role.add_permission("read")

    roles = {1: role}
    role_store = DummyRoleStore(roles)

    user = User(1, "test_user")
    user.role_ids = {1}

    user_service = UserService(role_store)

    # build cache
    assert user_service.user_has_permission(user, "read") is True
    assert user.user_id in user_service.user_permission_cache

    removed = user_service.remove_role_from_user(user, 1)

    assert removed is True
    assert user.user_id not in user_service.user_permission_cache
    assert 1 not in user.role_ids

# Test 7
def test_cycle_detection_raises_value_error(tmp_path):
    from storage.role_store import RoleStore

    file_path = tmp_path / "roles.json"
    file_path.write_text("[]")

    role_store = RoleStore(str(file_path))

    role1 = Role(1, "Role1")
    role2 = Role(2, "Role2")

    role_store.add_role(role1)
    role_store.add_role(role2)

    role_store.add_parent_to_role(2, 1)

    with pytest.raises(ValueError):
        role_store.add_parent_to_role(1, 2)