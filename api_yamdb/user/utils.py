from user.constants import CHOICES


def max_length_role():
    max_lenth = 0
    for role in CHOICES:
        if len(role[0]) > max_lenth:
            max_lenth = len(role[0])
        return max_lenth
