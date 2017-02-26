from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class CohortInstructorOrMemberAuthorization(DjangoAuthorization):
    def update_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if self.user_instructor_member(obj, bundle):
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        if super(CohortInstructorOrMemberAuthorization, self).update_detail(object_list, bundle):
            return self.user_instructor_member(bundle.obj, bundle)
        else:
            print("super call failed " + bundle.request.user.username)
            raise Unauthorized("You are not allowed to update that resource.")

    def delete_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if self.user_instructor_member(obj, bundle):
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        if super(CohortInstructorOrMemberAuthorization, self).delete_detail(object_list, bundle):
            return self.user_instructor_member(bundle.obj, bundle)
        else:
            print("super call failed " + bundle.request.user.username)
            raise Unauthorized("You are not allowed to delete that resource.")

    @staticmethod
    def user_instructor_member(obj, bundle):
        if hasattr(obj, 'user') and obj.user == bundle.request.user:
            print("obj.user is OK: " + bundle.request.user.username)
            return True
        elif hasattr(obj, 'instructor') and obj.instructor == bundle.request.user:
            print("obj.instructor is OK: " + bundle.request.user.username)
            return True
        elif hasattr(obj, 'cohort') and hasattr(
                obj.cohort, 'instructor') and obj.cohort.instructor == bundle.request.user:
            print("obj.cohort.instructor is OK: " + bundle.request.user.username)
            return True
        elif hasattr(obj, 'member') and obj.member == bundle.request.user:
            print("obj.member is OK: " + bundle.request.user.username)
            return True
        else:
            print("None of these match: " + bundle.request.user.username)
            return False


class UpdateUserObjectsOnlyAuthorization(DjangoAuthorization):
    def create_detail(self, object_list, bundle):
        print("create_detail " + object_list + " " + bundle)
        if super(UpdateUserObjectsOnlyAuthorization, self).create_detail(object_list, bundle):
            return bundle.obj.user == bundle.request.user
        else:
            raise Unauthorized("You are not allowed to create a resource that is not assigned to yourself.")

    def update_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        print("update_list " + object_list + " " + bundle + " " + allowed)
        return allowed

    def update_detail(self, object_list, bundle):
        print("update_detail " + object_list + " " + bundle)
        if super(UpdateUserObjectsOnlyAuthorization, self).update_detail(object_list, bundle):
            return bundle.obj.user == bundle.request.user
        else:
            raise Unauthorized("You are not allowed to update that resource.")

    def delete_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        print("delete_list " + object_list + " " + bundle + " " + allowed)
        return allowed

    def delete_detail(self, object_list, bundle):
        print("delete_detail " + object_list + " " + bundle)
        if super(UpdateUserObjectsOnlyAuthorization, self).delete_detail(object_list, bundle):
            return bundle.obj.user == bundle.request.user
        else:
            raise Unauthorized("You are not allowed to delete that resource.")


class UserObjectsOnlyAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        print("create_list " + object_list + " " + bundle)
        return False

    def read_list(self, object_list, bundle):
        print("read_list " + object_list + " " + bundle)
        return object_list

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        print("read_detail " + object_list + " " + bundle)
        return bundle.obj.user == bundle.request.user

    # def create_list(self, object_list, bundle):
    # 	# Assuming they're auto-assigned to ``user``.
    # 	print("create_list " + object_list + " " + bundle)
    # 	return object_list

    def create_detail(self, object_list, bundle):
        print("create_detail " + object_list + " " + bundle)
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        print("update_list " + object_list + " " + bundle)
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
