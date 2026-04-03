from django.contrib.auth import get_user_model

User = get_user_model()


def get_emails(groups=None, positions=None, extra_emails=None):
    """
    Returns a list of unique emails filtered by groups and/or positions.
    """

    users = User.objects.filter(is_active=True)

    if groups:
        users = users.filter(groups__name__in=groups)

    if positions:
        users = users.filter(profile__position__name__in=positions)

    emails = list(users.values_list("email", flat=True))

    if extra_emails:
        emails.extend(extra_emails)

    # remove duplicates + empty emails
    emails = list(set([e for e in emails if e]))

    return emails